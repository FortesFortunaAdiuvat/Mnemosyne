# Mnemosyne - Spaced Repetition Learning System

A FastAPI-based spaced repetition learning system for efficient knowledge retention and memorization.

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

---



