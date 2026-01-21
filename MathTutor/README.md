# Grade 5 Math Interactive Tutor

An interactive math tutoring web application for Grade 5 students following the Canadian curriculum. Features themed problems, achievement badges, and progress tracking.

## Features

- **5 Math Topics**: Number Sense, Measurement, Geometry, Patterning & Algebra, Data Management
- **3 Fun Themes**: Classic, Stranger Things, Puppy Paradise
- **3 Difficulty Levels**: Easy, Medium, Hard with increasing points
- **Achievement System**: 13 badges to earn
- **Progress Tracking**: Daily goals, streaks, and statistics
- **Step-by-Step Solutions**: Learn from every problem

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

The backend runs at http://localhost:5001

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend runs at http://localhost:3000

## Tech Stack

- **Frontend**: React 18, TypeScript, Tailwind CSS
- **Backend**: Python Flask
- **Database**: SQLite

## Project Structure

```
MathTutor/
├── backend/
│   ├── app.py              # Flask application
│   ├── database/           # SQLite setup
│   ├── models/             # User and Progress models
│   ├── generators/         # Problem generators for each topic
│   ├── themes/             # Theme engine
│   └── services/           # Scoring and achievements
└── frontend/
    ├── src/
    │   ├── components/     # React components
    │   ├── contexts/       # State management
    │   ├── hooks/          # Custom hooks
    │   ├── types/          # TypeScript interfaces
    │   └── utils/          # API client
    └── public/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/problem` | Generate a new problem |
| POST | `/api/answer` | Submit an answer |
| POST | `/api/skip` | Skip current problem |
| GET | `/api/user/:id` | Get user profile |
| POST | `/api/user` | Create new user |
| GET | `/api/progress/:userId` | Get progress data |
| GET | `/api/achievements/:userId` | Get achievements |
| GET | `/api/topics` | List available topics |
| GET | `/api/themes` | List available themes |
| GET | `/api/difficulties` | List difficulty levels |

## Themes

### Classic
Standard textbook-style math problems.

### Stranger Things
Problems set in Hawkins featuring Eleven, the Upside Down, Eggos, and D&D adventures!

### Puppy Paradise
Problems featuring adorable puppies, dog treats, and fun activities at the dog park!

## Achievements

- **Quick Learner**: 5 correct in a row
- **Number Ninja**: 10 Number Sense correct
- **Measurement Master**: 10 Measurement correct
- **Geometry Genius**: 10 Geometry correct
- **Pattern Pro**: 10 Patterning correct
- **Data Detective**: 10 Data Management correct
- **Week Warrior**: 7-day goal streak
- **Perfect Day**: 100% first-try accuracy (min 5 problems)
- **Hundred Club**: 100+ points in one session
- **Math Explorer**: Try all 5 topics
- **Theme Explorer**: Try all 3 themes
- **Persistent Learner**: 50 problems attempted
- **Century Solver**: 100 problems solved correctly
