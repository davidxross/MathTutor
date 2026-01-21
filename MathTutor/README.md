# Grade 5 Math Interactive Tutor

An interactive math tutoring web application for Grade 5 students following the Canadian curriculum. Features themed problems, achievement badges, and progress tracking.

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-06B6D4?logo=tailwindcss)

## Features

- **5 Math Topics**: Number Sense, Measurement, Geometry, Patterning & Algebra, Data Management
- **3 Fun Themes**: Classic, Stranger Things, Puppy Paradise
- **3 Difficulty Levels**: Easy, Medium, Hard with increasing points
- **Achievement System**: 13 badges to earn
- **Progress Tracking**: Daily goals, streaks, and statistics
- **Step-by-Step Solutions**: Learn from every problem
- **Multi-User Support**: Multiple students can track their own progress

## Screenshots

| Login | Dashboard | Problem View |
|-------|-----------|--------------|
| Select or create a student profile | Track progress, stats, and achievements | Solve problems with themed content |

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

| Layer | Technology |
|-------|------------|
| Frontend | React 18, TypeScript, Tailwind CSS |
| Backend | Python Flask, Flask-CORS |
| Database | SQLite |
| State Management | React Context API |

## Project Structure

```
MathTutor/
├── backend/
│   ├── app.py              # Flask application & API routes
│   ├── requirements.txt    # Python dependencies
│   ├── database/
│   │   └── db.py           # SQLite setup & schema
│   ├── models/
│   │   ├── user.py         # User model & CRUD
│   │   └── progress.py     # Progress tracking & stats
│   ├── generators/         # Problem generators
│   │   ├── base.py         # Base generator class
│   │   ├── number_sense.py
│   │   ├── measurement.py
│   │   ├── geometry.py
│   │   ├── patterning.py
│   │   └── data_management.py
│   ├── themes/
│   │   └── theme_engine.py # Theme word substitutions
│   └── services/
│       ├── scoring.py      # Points calculation
│       └── achievements.py # Badge checking
└── frontend/
    ├── package.json
    ├── tailwind.config.js
    ├── tsconfig.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.tsx
        ├── index.tsx
        ├── index.css
        ├── components/
        │   ├── Login.tsx
        │   ├── Dashboard.tsx
        │   ├── ProblemView.tsx
        │   ├── SolutionModal.tsx
        │   ├── TopicSelector.tsx
        │   ├── ThemeSelector.tsx
        │   ├── ProgressBar.tsx
        │   ├── StatsPanel.tsx
        │   ├── BadgeDisplay.tsx
        │   ├── Calendar.tsx
        │   └── Celebration.tsx
        ├── contexts/
        │   ├── UserContext.tsx
        │   └── GameContext.tsx
        ├── hooks/
        │   ├── useProblems.ts
        │   └── useProgress.ts
        ├── types/
        │   └── index.ts
        └── utils/
            └── api.ts
```

## Math Topics & Problem Types

### Number Sense & Numeration
| Problem Type | Example |
|-------------|---------|
| Multiplication | What is 12 × 8? |
| Division | 72 ÷ 9 = ? |
| Fractions | Add 1/4 + 2/4 |
| Decimals | 3.5 + 2.7 = ? |
| Percentages | What is 25% of 80? |

### Measurement
| Problem Type | Example |
|-------------|---------|
| Perimeter | Find the perimeter of a rectangle (l=8, w=5) |
| Area | Calculate the area of a triangle (b=10, h=6) |
| Volume | What is the volume of a cube with sides of 4 cm? |
| Unit Conversion | Convert 2.5 km to meters |
| Time | A movie starts at 2:30 PM and is 1 hour 45 minutes long. When does it end? |

### Geometry
| Problem Type | Example |
|-------------|---------|
| Angles | The angles in a triangle are 60° and 70°. What is the third angle? |
| 2D Shapes | How many sides does a hexagon have? |
| 3D Shapes | How many faces does a rectangular prism have? |
| Symmetry | How many lines of symmetry does a square have? |
| Coordinates | What is the distance between (2,3) and (5,7)? |

### Patterning & Algebra
| Problem Type | Example |
|-------------|---------|
| Number Patterns | What comes next: 2, 6, 18, 54, ___? |
| Equations | Solve for x: 3x + 5 = 20 |
| Variables | If a = 4 and b = 3, what is 2a + b? |
| Growing Patterns | Pattern grows by adding 3 each time. If term 1 is 5, what is term 4? |
| Input-Output | If the rule is "multiply by 2, add 1", what output does 5 give? |

### Data Management & Probability
| Problem Type | Example |
|-------------|---------|
| Mean | Find the average of: 12, 15, 18, 21, 14 |
| Median | Find the median of: 3, 7, 2, 9, 5 |
| Mode | Find the mode of: 4, 7, 4, 9, 4, 2 |
| Range | Find the range of: 15, 22, 8, 31, 19 |
| Probability | A bag has 3 red and 5 blue marbles. What's the probability of picking red? |
| Graph Reading | Based on a bar chart, which category has the highest value? |

## Themes

### Classic
Standard textbook-style math problems with generic names and scenarios.

### Stranger Things
Problems set in Hawkins featuring characters and elements from the show:
- **Characters**: Eleven, Mike, Dustin, Lucas, Will, Max, Nancy, Steve, Hopper
- **Items**: Eggos, walkie-talkies, Christmas lights, D&D dice
- **Places**: The Upside Down, Hawkins Lab, the arcade

**Example**: *Eleven has 24 Eggos to share equally among 4 friends. How many Eggos does each friend get?*

### Puppy Paradise
Problems featuring adorable puppies and dog-themed scenarios:
- **Puppies**: Buddy, Max, Bella, Charlie, Luna, Cooper, Daisy, Rocky, Sadie, Tucker
- **Items**: Dog treats, chew toys, tennis balls, food bowls
- **Places**: Dog park, pet store, backyard

**Example**: *Bella found 15 tennis balls at the dog park. She buried 1/3 of them. How many did she bury?*

## Scoring System

### Base Points
| Difficulty | Points |
|------------|--------|
| Easy | 5 points |
| Medium | 10 points |
| Hard | 15 points |

### Bonuses
| Bonus | Points | Condition |
|-------|--------|-----------|
| First-Try Bonus | +2 points | Correct on first attempt |
| Streak Bonus | +5 points | Every 3 correct in a row |

### Attempts
- Maximum 3 attempts per problem
- Hints provided after incorrect attempts
- Full solution shown after 3 attempts or when skipping

## Achievements

| Badge | Name | Requirement |
|-------|------|-------------|
| ⚡ | Quick Learner | 5 correct in a row |
| 🔢 | Number Ninja | 10 Number Sense correct |
| 📏 | Measurement Master | 10 Measurement correct |
| 📐 | Geometry Genius | 10 Geometry correct |
| 🔄 | Pattern Pro | 10 Patterning correct |
| 📊 | Data Detective | 10 Data Management correct |
| 🏆 | Week Warrior | 7-day goal streak |
| ⭐ | Perfect Day | 100% first-try accuracy (min 5 problems) |
| 💯 | Hundred Club | 100+ points in one session |
| 🗺️ | Math Explorer | Try all 5 topics |
| 🎭 | Theme Explorer | Try all 3 themes |
| 💪 | Persistent Learner | 50 problems attempted |
| 🎯 | Century Solver | 100 problems solved correctly |

## API Reference

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/user` | Create new user |
| GET | `/api/user/:id` | Get user profile |
| GET | `/api/users` | List all users |
| PUT | `/api/settings/:id` | Update user settings |

### Problems
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/problem` | Generate a new problem |
| POST | `/api/answer` | Submit an answer |
| POST | `/api/skip` | Skip current problem |

**Query Parameters for `/api/problem`:**
- `topic`: number_sense, measurement, geometry, patterning, data_management
- `difficulty`: easy, medium, hard
- `theme`: classic, stranger_things, puppy
- `user_id`: User ID for tracking

### Progress & Achievements
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/progress/:userId` | Get progress data |
| GET | `/api/achievements/:userId` | Get achievements |

### Metadata
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/topics` | List available topics |
| GET | `/api/themes` | List available themes |
| GET | `/api/difficulties` | List difficulty levels |

## Development

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm 9+

### Running Tests
```bash
# Backend (from backend directory)
python -m pytest

# Frontend (from frontend directory)
npm test
```

### Building for Production
```bash
# Frontend
cd frontend
npm run build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Canadian Grade 5 Mathematics Curriculum
- React and Flask communities
- All contributors and testers
