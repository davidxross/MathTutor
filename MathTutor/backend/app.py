from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from database.db import init_db, get_db, close_db
from models.user import User
from models.progress import Progress
from generators import get_generator, get_all_topics
from themes.theme_engine import ThemeEngine
from services.scoring import ScoringService
from services.achievements import AchievementService, ACHIEVEMENTS

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_db()

# In-memory session storage (in production, use Redis or similar)
sessions = {}


def get_session(user_id: int) -> dict:
    """Get or create a session for a user."""
    if user_id not in sessions:
        sessions[user_id] = {
            "scoring": ScoringService(),
            "current_problem": None,
            "attempts": 0,
            "session_points": 0,
            "session_problems": 0,
            "session_correct": 0,
            "session_first_try": 0,
            "topics_practiced": [],
            "themes_used": []
        }
    return sessions[user_id]


# ============ User Endpoints ============

@app.route('/api/user', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.json or {}
    name = data.get('name', 'Student')
    settings = data.get('settings')

    user = User.create(name, settings)
    return jsonify(user.to_dict()), 201


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID."""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users."""
    users = User.get_all()
    return jsonify([u.to_dict() for u in users])


@app.route('/api/settings/<int:user_id>', methods=['PUT'])
def update_settings(user_id):
    """Update user settings."""
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json or {}
    user.update_settings(data)
    return jsonify(user.to_dict())


# ============ Problem Endpoints ============

@app.route('/api/problem', methods=['GET'])
def get_problem():
    """Generate a new problem.

    Query params:
        - topic: Topic category (number_sense, measurement, etc.)
        - difficulty: easy, medium, hard
        - theme: classic, stranger_things, puppy
        - user_id: User ID for session tracking
    """
    topic = request.args.get('topic', 'number_sense')
    difficulty = request.args.get('difficulty', 'easy')
    theme_id = request.args.get('theme', 'classic')
    user_id = request.args.get('user_id', type=int)

    try:
        generator = get_generator(topic)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Generate problem
    problem = generator.generate(difficulty=difficulty)

    # Apply theme
    theme_engine = ThemeEngine(theme_id)
    themed_problem = theme_engine.apply_theme(problem)

    # Store in session
    if user_id:
        session = get_session(user_id)
        session['current_problem'] = themed_problem
        session['attempts'] = 0
        if topic not in session['topics_practiced']:
            session['topics_practiced'].append(topic)
        if theme_id not in session['themes_used']:
            session['themes_used'].append(theme_id)

    # Don't send the answer to the client
    response = {
        "question": themed_problem['question'],
        "difficulty": themed_problem['difficulty'],
        "topic": themed_problem['topic'],
        "problem_type": themed_problem['problem_type'],
        "theme": themed_problem['theme'],
        "theme_name": themed_problem['theme_name']
    }

    return jsonify(response)


@app.route('/api/answer', methods=['POST'])
def submit_answer():
    """Submit an answer to the current problem.

    Body:
        - user_id: User ID
        - answer: User's answer
    """
    data = request.json or {}
    user_id = data.get('user_id')
    user_answer = str(data.get('answer', '')).strip()

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    session = get_session(user_id)
    problem = session.get('current_problem')

    if not problem:
        return jsonify({"error": "No active problem"}), 400

    session['attempts'] += 1
    first_try = session['attempts'] == 1

    # Check answer
    correct_answer = problem['answer']

    # Handle answer comparison
    try:
        # Try numeric comparison
        user_val = float(user_answer.replace(',', '').strip())
        correct_val = float(str(correct_answer).replace(',', '').strip())
        is_correct = abs(user_val - correct_val) < 0.01
    except (ValueError, TypeError):
        # String comparison (for fractions, text answers, etc.)
        is_correct = user_answer.lower() == str(correct_answer).lower()

    # Calculate points
    scoring = session['scoring']
    points_result = scoring.calculate_points(
        difficulty=problem['difficulty'],
        correct=is_correct,
        first_try=first_try
    )

    # Update session stats
    if is_correct:
        session['session_problems'] += 1
        session['session_correct'] += 1
        session['session_points'] += points_result['total_points']
        if first_try:
            session['session_first_try'] += 1

        # Update progress in database
        progress = Progress.get_or_create_today(user_id)
        progress.update(
            points=points_result['total_points'],
            attempted=1,
            correct=1,
            topic=problem['topic']
        )

        # Record problem history
        Progress.record_problem(
            user_id=user_id,
            problem_type=problem['problem_type'],
            topic=problem['topic'],
            difficulty=problem['difficulty'],
            correct=True,
            first_try=first_try,
            points=points_result['total_points']
        )

        # Check for achievements
        achievement_service = AchievementService(user_id)
        total_stats = Progress.get_total_stats(user_id)
        topic_stats = Progress.get_topic_stats(user_id)
        topic_correct = {t['topic']: t['correct_count'] for t in topic_stats}
        goal_streak = Progress.get_streak(user_id)

        context = {
            'current_streak': points_result['new_streak'],
            'session_points': session['session_points'],
            'session_problems': session['session_problems'],
            'session_correct': session['session_correct'],
            'session_first_try': session['session_first_try'],
            'topics_practiced': session['topics_practiced'],
            'themes_used': session['themes_used'],
            'total_attempted': total_stats['total_attempted'],
            'total_correct': total_stats['total_correct'],
            'topic_correct': topic_correct,
            'goal_streak': goal_streak
        }

        new_achievements = achievement_service.check_and_award(context)

        # Clear current problem
        session['current_problem'] = None

        return jsonify({
            "correct": True,
            "answer": str(correct_answer),
            "solution": problem['solution'],
            "points": points_result,
            "new_achievements": new_achievements
        })
    else:
        # Wrong answer
        Progress.record_problem(
            user_id=user_id,
            problem_type=problem['problem_type'],
            topic=problem['topic'],
            difficulty=problem['difficulty'],
            correct=False,
            first_try=first_try,
            points=0
        )

        if session['attempts'] == 1:
            session['session_problems'] += 1
            progress = Progress.get_or_create_today(user_id)
            progress.update(attempted=1)

        return jsonify({
            "correct": False,
            "attempts": session['attempts'],
            "hint": "Try again!" if session['attempts'] < 3 else None,
            "show_solution": session['attempts'] >= 3,
            "solution": problem['solution'] if session['attempts'] >= 3 else None,
            "answer": str(correct_answer) if session['attempts'] >= 3 else None
        })


@app.route('/api/skip', methods=['POST'])
def skip_problem():
    """Skip the current problem."""
    data = request.json or {}
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id required"}), 400

    session = get_session(user_id)
    problem = session.get('current_problem')

    if not problem:
        return jsonify({"error": "No active problem"}), 400

    # Reset streak
    session['scoring'].reset_streak()

    # Record skip
    Progress.record_problem(
        user_id=user_id,
        problem_type=problem['problem_type'],
        topic=problem['topic'],
        difficulty=problem['difficulty'],
        correct=False,
        first_try=False,
        points=0
    )

    response = {
        "skipped": True,
        "solution": problem['solution'],
        "answer": str(problem['answer'])
    }

    session['current_problem'] = None
    return jsonify(response)


# ============ Progress Endpoints ============

@app.route('/api/progress/<int:user_id>', methods=['GET'])
def get_progress(user_id):
    """Get progress data for a user."""
    days = request.args.get('days', 30, type=int)

    today = Progress.get_or_create_today(user_id)
    history = Progress.get_user_history(user_id, days)
    total_stats = Progress.get_total_stats(user_id)
    topic_stats = Progress.get_topic_stats(user_id)

    user = User.get_by_id(user_id)
    daily_goal = user.settings.get('daily_goal', 10) if user else 10
    streak = Progress.get_streak(user_id, daily_goal)

    # Get session data
    session = get_session(user_id)

    return jsonify({
        "today": today.to_dict(),
        "history": [p.to_dict() for p in history],
        "total": total_stats,
        "by_topic": topic_stats,
        "current_streak": session['scoring'].get_streak(),
        "goal_streak": streak,
        "daily_goal": daily_goal,
        "session": {
            "points": session['session_points'],
            "problems": session['session_problems'],
            "correct": session['session_correct']
        }
    })


@app.route('/api/achievements/<int:user_id>', methods=['GET'])
def get_achievements(user_id):
    """Get achievements for a user."""
    service = AchievementService(user_id)
    all_achievements = service.get_all_achievements_with_status()
    earned = [a for a in all_achievements if a['earned']]
    unearned = [a for a in all_achievements if not a['earned']]

    return jsonify({
        "earned": earned,
        "available": unearned,
        "total_earned": len(earned),
        "total_available": len(ACHIEVEMENTS)
    })


# ============ Metadata Endpoints ============

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get list of available topics."""
    topics = get_all_topics()
    topic_info = {
        "number_sense": {"name": "Number Sense & Numeration", "icon": "🔢"},
        "measurement": {"name": "Measurement", "icon": "📏"},
        "geometry": {"name": "Geometry", "icon": "📐"},
        "patterning": {"name": "Patterning & Algebra", "icon": "🔄"},
        "data_management": {"name": "Data Management & Probability", "icon": "📊"}
    }
    return jsonify([{"id": t, **topic_info.get(t, {"name": t, "icon": "📚"})} for t in topics])


@app.route('/api/themes', methods=['GET'])
def get_themes():
    """Get list of available themes."""
    return jsonify(ThemeEngine.get_all_themes())


@app.route('/api/difficulties', methods=['GET'])
def get_difficulties():
    """Get list of difficulty levels."""
    return jsonify([
        {"id": "easy", "name": "Easy", "points": 5},
        {"id": "medium", "name": "Medium", "points": 10},
        {"id": "hard", "name": "Hard", "points": 15}
    ])


if __name__ == '__main__':
    app.run(debug=True, port=5001)
