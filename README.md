# Mnemosyne - Spaced Repetition Learning System

![Mnemosyne the Tutor](images/Mnemosyne_Tutor.png)

📚 Mnemosyne: Learning That Endures
Introduction
Mnemosyne is an AI-powered educational framework that blends spaced repetition, active recall, and classical learning theory into a unified, modern platform for lifelong knowledge mastery.

The project is named after Mnemosyne, the ancient Greek Titaness and goddess of memory, revered as the mother of the Nine Muses, who inspired the arts and sciences. In myth, Mnemosyne stood as a pillar of mental order, continuity, and creativity—qualities we aim to embed in this intelligent learning system.

In classical lore, to drink from the River Mnemosyne was to remember everything with perfect clarity. This project aspires to become that metaphorical river: a medium through which users retain knowledge intuitively, effectively, and enduringly.

Mission Statement
Mnemosyne's mission is to empower learners with a system that:

🧠 Enhances long-term retention through scientifically validated methods such as spaced repetition and active recall.

🤖 Adapts intelligently using AI to personalize review schedules, prioritize weak areas, and optimize the learning curve.

🏛️ Revives classical learning models, drawing inspiration from the Socratic method, dialectic reasoning, and the muse-driven pursuit of excellence in diverse fields.

🌍 Supports learners at all levels—from autodidacts to educators, students, and professionals seeking deep expertise.

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

1. **Install Dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Run the FastAPI Server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**
   - **API Root**: http://localhost:8000/
   - **Interactive API Docs**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **API Info**: http://localhost:8000/api/info

### Running Tests

```bash
python3 -m pytest tests/ -v
```

## 📁 Project Structure

```
mnemosyne/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/routes/          # API route handlers
│   ├── core/                # Core configuration and utilities
│   ├── models/              # Database models
│   └── services/            # Business logic services
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🧪 Current Features

- ✅ FastAPI Hello World endpoint
- ✅ Health check endpoint
- ✅ API information endpoint
- ✅ Automatic API documentation (Swagger UI)
- ✅ CORS middleware configuration
- ✅ Basic test suite with pytest

## 🔄 Development Workflow

This project follows Test-Driven Development (TDD) and Behavior-Driven Development (BDD) methodologies:

1. Write tests first
2. Implement features to pass tests
3. Refactor and optimize
4. Repeat

## 🎯 Roadmap

- [ ] User authentication system
- [ ] Database integration (SQLAlchemy)
- [ ] Card management endpoints
- [ ] Spaced repetition algorithm
- [ ] Study session management
- [ ] Progress tracking and analytics
- [ ] Frontend interface
- [ ] Migrate to UV package management and Ruff
- [ ] Use TOML files to manage information sources

---
