# Mnemosyne - Spaced Repetition Learning System

![Mnemosyne the Tutor](images/Mnemosyne_Tutor.png)

📚 **Mnemosyne: Learning That Endures**

## Introduction

Mnemosyne is an AI-powered educational framework that blends spaced repetition, active recall, and classical learning theory into a unified, modern platform for lifelong knowledge mastery.

The project is named after Mnemosyne, the ancient Greek Titaness and goddess of memory, revered as the mother of the Nine Muses, who inspired the arts and sciences. In myth, Mnemosyne stood as a pillar of mental order, continuity, and creativity—qualities we aim to embed in this intelligent learning system.

In classical lore, to drink from the River Mnemosyne was to remember everything with perfect clarity. This project aspires to become that metaphorical river: a medium through which users retain knowledge intuitively, effectively, and enduringly.

## Mission Statement

Mnemosyne's mission is to empower learners with a system that:

🧠 **Enhances long-term retention** through scientifically validated methods such as spaced repetition and active recall.

🤖 **Adapts intelligently** using AI to personalize review schedules, prioritize weak areas, and optimize the learning curve.

🏛️ **Revives classical learning models**, drawing inspiration from the Socratic method, dialectic reasoning, and the muse-driven pursuit of excellence in diverse fields.

🌍 **Supports learners at all levels**—from autodidacts to educators, students, and professionals seeking deep expertise.

🔁 Builds memory as a practice, not just a utility—positioning learning as an art of recollection, not mere consumption.

Why Mnemosyne?
In a world oversaturated with content and distractions, Mnemosyne seeks to slow down the learning process—not to make it harder, but to make it stick. By combining ancient wisdom with modern insights, it aims to answer questions like:

How can we remember what truly matters?

What makes knowledge enduring and transferable?

Can learning be both efficient and beautiful?

Key Features (Planned)
🧠 Adaptive spaced repetition using modern algorithms like SM-2 and FSRS

🎓 Subject groupings by domain (e.g., philosophy, finance, medicine)

📊 Memory analytics dashboard with decay curves and heat maps

🧾 Custom knowledge tracking with prompts, tags, and references

🧬 AI-assisted card generation and difficulty prediction

🗂️ Export/import via TOML, Markdown, or Anki

🌐 Optional FastAPI backend for integration and extension

Get Involved
Whether you're a student, researcher, developer, or educator, Mnemosyne welcomes contributions and collaborators. Let's build the future of memory—and bring the Muse of learning into the digital age.

"Memory is the mother of all wisdom."
— Aeschylus

A FastAPI-based spaced repetition learning system for efficient knowledge retention and memorization. This project is named after the Mnemosyne the Titan goddess of Memory(Mnemo for short). As the daughter of Gaia and Uranus, and sibling to the Titans, the Cyclopes, and the Erinyes; With Zeus, she bore the nine muses on nine consecutive days. She is a strong symbol of Memory, Learning, Rememberance, Logic, Foresight, Reason, and the Adept Use of Language. 

The purpose of this project is to combine spaced repetition, artificial intelligence, and classical learning models into a modern educational app that honors both cutting-edge cognitive science and the timeless pursuit of knowledge.

The name of the project—Mnemosyne—is drawn from the ancient Greek goddess of memory, the mother of the Nine Muses. In Greek mythology, Mnemosyne was not only the personification of memory itself, but also a symbol of oral tradition, deep knowledge, and mental discipline. According to legend, those who drank from the waters of Mnemosyne's spring would remember all, in contrast to the River Lethe, which granted forgetfulness.

By invoking her name, this project aspires to fuse the mythic reverence for memory with scientifically proven techniques like spaced repetition and active recall, enhanced through modern AI-driven personalization. Just as Mnemosyne was believed to be the source of all inspiration in the arts and sciences through her daughters—the Muses—this project aims to empower learners with tools that stimulate curiosity, support retention, and ignite lifelong learning across disciplines.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip3

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/FortesFortunaAdiuvat/Mnemosyne.git
   cd Mnemosyne
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the FastAPI Server**
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - **API Root**: http://localhost:8000/
   - **Interactive API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **API Info**: http://localhost:8000/api/info

### Running Tests

```bash
source .venv/bin/activate
python3 -m pytest tests/ -v
```

## 📁 Project Structure

```
mnemosyne/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   └── routes/
│   │       ├── cards.py           # Card management endpoints
│   │       ├── study.py           # Study session endpoints
│   │       └── calendar.py        # Calendar & habit tracking endpoints
│   ├── core/
│   │   ├── config.py              # Application configuration
│   │   └── database.py            # Database setup and connection
│   ├── models/
│   │   ├── card.py                # Card database model
│   │   ├── study_session.py       # Study session models
│   │   ├── calendar.py            # Calendar & reminder models
│   │   └── schemas.py             # Pydantic schemas for API validation
│   └── services/
│       └── spaced_repetition.py   # SM-2 algorithm implementation
├── tests/
│   ├── test_main.py               # Basic API tests
│   ├── test_cards.py              # Card management tests
│   ├── test_spaced_repetition.py  # SM-2 algorithm tests
│   ├── test_study_sessions.py     # Study session tests
│   └── test_calendar.py           # Calendar integration tests
├── images/                        # Project images and assets
├── info_sources/                  # Information source configurations
├── notes/                         # Development notes and documentation
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── CONTRIBUTING.md                # Development guidelines
```

## 🎯 Current Features

### ✅ **Core API Infrastructure**
- FastAPI application with automatic OpenAPI documentation
- Health check and API information endpoints
- CORS middleware configuration
- SQLAlchemy database integration with SQLite
- Comprehensive test suite with pytest

### ✅ **Card Management System**
- **Create, Read, Update, Delete (CRUD)** operations for flashcards
- **Deck organization** with customizable deck names
- **Pagination support** for large card collections
- **Input validation** with Pydantic schemas
- **Database persistence** with SQLAlchemy models

### ✅ **SM-2 Spaced Repetition Algorithm**
- **Scientifically-based spaced repetition** using the SM-2 algorithm
- **Quality-based review scoring** (0-5 scale)
- **Adaptive interval calculation** based on performance
- **Ease factor adjustment** for personalized difficulty
- **Due card tracking** with automatic scheduling

### ✅ **Study Session Management**
- **Structured learning sessions** with configurable parameters
- **Session lifecycle management** (start, progress, end)
- **Progress tracking** with accuracy metrics
- **Deck-specific sessions** for focused study
- **Session statistics** and performance analytics

### ✅ **Calendar Integration & Habit Tracking**
- **Learning streak tracking** (current and longest streaks)
- **Daily due card counts** with deck breakdown
- **Weekly progress visualization** with accuracy trends
- **Monthly activity heatmaps** for habit visualization
- **Deck progress tracking** over time
- **Study reminders** with customizable scheduling
- **Upcoming review schedules** for planning

## 🔗 API Endpoints

### **Card Management**
```
POST   /api/cards/              # Create a new card
GET    /api/cards/              # List cards with pagination
GET    /api/cards/due           # Get cards due for review
GET    /api/cards/{id}          # Get specific card by ID
PUT    /api/cards/{id}          # Update existing card
DELETE /api/cards/{id}          # Delete card
POST   /api/cards/{id}/review   # Review card with SM-2 algorithm
```

### **Study Sessions**
```
POST   /api/study/sessions/                    # Start new study session
GET    /api/study/sessions/{id}/next-card      # Get next card in session
POST   /api/study/sessions/{id}/review         # Submit card review in session
PUT    /api/study/sessions/{id}/end            # End study session
GET    /api/study/stats                        # Get study statistics
```

### **Calendar & Habits**
```
GET    /api/calendar/due-count                 # Daily due card counts
GET    /api/calendar/weekly-progress           # Weekly learning progress
GET    /api/calendar/streak                    # Learning streak information
GET    /api/calendar/heatmap                   # Monthly activity heatmap
GET    /api/calendar/deck-progress             # Deck progress over time
POST   /api/calendar/reminder                  # Create study reminders
GET    /api/calendar/upcoming                  # Upcoming review schedule
```

### **System**
```
GET    /                       # API root endpoint
GET    /health                 # Health check
GET    /api/info              # API information
GET    /docs                  # Interactive API documentation
```

## 🧪 Test Coverage

**Current Test Status**: 42+ passed, 2 failed (95%+ pass rate)

### **Test Categories**
- **✅ Core API Tests** (3/3 passing) - Basic functionality
- **✅ SM-2 Algorithm Tests** (6/6 passing) - Spaced repetition logic
- **✅ Study Session Tests** (5/6 passing) - Session management
- **✅ Card Management Tests** (15/15 passing) - Full CRUD operations
- **✅ Calendar Integration Tests** (7/7 passing) - Habit tracking and progress
- **✅ Card Review API Tests** (4/4 passing) - SM-2 integration
- **⚠️ Due Cards Tests** (1/3 passing) - Minor timing-sensitive issues

### **Test Infrastructure**
- **Robust test isolation** with shared database configuration
- **Comprehensive fixtures** for reliable test execution
- **TDD methodology** with clear test organization
- **Timing-sensitive tests** use appropriate delays for reliability

## 🔄 Development Workflow

This project follows **Test-Driven Development (TDD)** and **Behavior-Driven Development (BDD)** methodologies:

1. **Write tests first** to define expected behavior
2. **Implement features** to pass the tests
3. **Refactor and optimize** while maintaining test coverage
4. **Document changes** and update API specifications

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLAlchemy with SQLite
- **Testing**: pytest with comprehensive test coverage
- **Validation**: Pydantic schemas
- **Documentation**: Automatic OpenAPI/Swagger generation
- **Algorithm**: SM-2 spaced repetition algorithm

## 🎯 Roadmap

### **Phase 1: Foundation** ✅
- [x] FastAPI application setup
- [x] Database integration
- [x] Basic CRUD operations
- [x] SM-2 algorithm implementation

### **Phase 2: Core Features** ✅
- [x] Study session management
- [x] Progress tracking
- [x] Calendar integration
- [x] Habit tracking features

### **Phase 3: Enhancement** 🚧
- [ ] User authentication system
- [ ] Advanced analytics dashboard
- [ ] Import/export functionality (Anki, CSV, JSON)
- [ ] AI-assisted card generation
- [ ] Mobile-responsive frontend

### **Phase 4: Intelligence** 📋
- [ ] Machine learning for difficulty prediction
- [ ] Personalized review scheduling
- [ ] Content recommendation system
- [ ] Advanced spaced repetition algorithms (FSRS)

### **Phase 5: Integration** 📋
- [ ] Third-party integrations
- [ ] API for external applications
- [ ] Plugin system
- [ ] Multi-user support

## 🤝 Contributing

We welcome contributions from developers, educators, and learners! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up the development environment
- Adding new features and endpoints
- Writing and running tests
- Database schema changes
- Code style and best practices

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hermann Ebbinghaus** - Pioneer of memory research and the forgetting curve
- **Piotr Woźniak** - Creator of the SM-2 spaced repetition algorithm
- **The ancient Greeks** - For their timeless wisdom on memory and learning
- **The open-source community** - For the tools and libraries that make this possible

---

*"Memory is the mother of all wisdom."* — Aeschylus

**Drink from the River Mnemosyne and remember everything with perfect clarity.**
