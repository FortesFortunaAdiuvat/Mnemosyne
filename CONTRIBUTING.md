# Contributing to Mnemosyne

Welcome to the Mnemosyne project! We're excited to have you contribute to building the future of memory and learning. This guide will help you get started with contributing to our spaced repetition learning system.

## 🎯 Project Philosophy

Mnemosyne follows these core principles:

- **Test-Driven Development (TDD)**: Write tests first, then implement features
- **Behavior-Driven Development (BDD)**: Focus on user behavior and outcomes
- **Classical Learning**: Honor timeless educational principles
- **Scientific Rigor**: Base features on cognitive science research
- **Simplicity**: Keep code clean, readable, and maintainable

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Git** for version control
- **Basic understanding** of FastAPI, SQLAlchemy, and pytest
- **Familiarity** with spaced repetition concepts (helpful but not required)

### Development Environment Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Mnemosyne.git
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

4. **Verify Installation**
   ```bash
   # Run tests to ensure everything works
   python3 -m pytest tests/test_main.py -v
   
   # Start the development server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the Development Environment**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 🔄 Development Workflow

### 1. **Issue Selection and Planning**

- Browse [open issues](https://github.com/FortesFortunaAdiuvat/Mnemosyne/issues)
- Comment on issues you'd like to work on
- For new features, create an issue first to discuss the approach
- Use labels to categorize: `bug`, `feature`, `enhancement`, `documentation`

### 2. **Branch Strategy**

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description

# Keep your branch up to date
git fetch origin
git rebase origin/main
```

### 3. **Test-Driven Development Process**

**Step 1: Write Tests First**
```bash
# Create or update test files
touch tests/test_your_feature.py

# Write failing tests that define expected behavior
python3 -m pytest tests/test_your_feature.py -v
# Tests should fail initially
```

**Step 2: Implement Features**
```bash
# Implement the minimum code to make tests pass
# Run tests frequently during development
python3 -m pytest tests/test_your_feature.py -v
```

**Step 3: Refactor and Optimize**
```bash
# Improve code quality while keeping tests green
# Run full test suite to ensure no regressions
python3 -m pytest tests/ -v
```

## 🏗️ Adding New Features

### Adding API Endpoints

1. **Create Tests First** (`tests/test_your_feature.py`)
   ```python
   import pytest
   from fastapi.testclient import TestClient
   from app.main import app

   client = TestClient(app)

   def test_new_endpoint():
       response = client.get("/api/your-endpoint")
       assert response.status_code == 200
       assert "expected_field" in response.json()
   ```

2. **Create Pydantic Schemas** (`app/models/schemas.py`)
   ```python
   from pydantic import BaseModel, Field
   from typing import Optional

   class YourFeatureCreate(BaseModel):
       name: str = Field(..., min_length=1, max_length=100)
       description: Optional[str] = None

   class YourFeatureResponse(BaseModel):
       id: int
       name: str
       description: Optional[str]
       created_at: datetime

       class Config:
           from_attributes = True
   ```

3. **Create Database Models** (`app/models/your_feature.py`)
   ```python
   from sqlalchemy import Column, Integer, String, DateTime
   from sqlalchemy.sql import func
   from app.models.card import Base

   class YourFeature(Base):
       __tablename__ = "your_features"

       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False)
       description = Column(String(500), nullable=True)
       created_at = Column(DateTime(timezone=True), server_default=func.now())
   ```

4. **Update Database Configuration** (`app/core/database.py`)
   ```python
   def create_tables():
       """Create all tables in the database"""
       # Import all models to ensure they're registered with Base
       from app.models.card import Card
       from app.models.study_session import StudySession, CardReview
       from app.models.calendar import DailyActivity, StudyReminder
       from app.models.your_feature import YourFeature  # Add this line
       
       # Create all tables using the shared Base
       Base.metadata.create_all(bind=engine)
   ```

5. **Create API Routes** (`app/api/routes/your_feature.py`)
   ```python
   from fastapi import APIRouter, Depends, HTTPException, status
   from sqlalchemy.orm import Session
   from app.core.database import get_db
   from app.models.your_feature import YourFeature
   from app.models.schemas import YourFeatureCreate, YourFeatureResponse

   router = APIRouter()

   @router.post("/", response_model=YourFeatureResponse, status_code=status.HTTP_201_CREATED)
   def create_feature(feature: YourFeatureCreate, db: Session = Depends(get_db)):
       db_feature = YourFeature(**feature.dict())
       db.add(db_feature)
       db.commit()
       db.refresh(db_feature)
       return db_feature
   ```

6. **Register Routes** (`app/main.py`)
   ```python
   from app.api.routes import cards, study, calendar, your_feature

   # Include routers
   app.include_router(cards.router, prefix="/api/cards", tags=["cards"])
   app.include_router(study.router, prefix="/api/study", tags=["study"])
   app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])
   app.include_router(your_feature.router, prefix="/api/your-feature", tags=["your-feature"])
   ```

### Database Schema Changes

1. **Always Create Migration-Safe Changes**
   - Add new columns with default values
   - Avoid dropping columns without deprecation period
   - Use nullable columns for optional fields

2. **Update All Related Models**
   - Database models (`app/models/`)
   - Pydantic schemas (`app/models/schemas.py`)
   - Test fixtures and data

3. **Test Database Changes**
   ```bash
   # Remove existing database to test fresh creation
   rm -f mnemosyne.db test_*.db
   
   # Run tests to ensure database creation works
   python3 -m pytest tests/test_main.py -v
   ```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── test_main.py              # Basic API functionality
├── test_cards.py             # Card management features
├── test_spaced_repetition.py # SM-2 algorithm logic
├── test_study_sessions.py    # Study session management
├── test_calendar.py          # Calendar and habit tracking
└── test_your_feature.py      # Your new feature tests
```

### Writing Good Tests

1. **Follow the AAA Pattern**
   ```python
   def test_feature_behavior():
       # Arrange - Set up test data
       test_data = {"name": "Test Feature"}
       
       # Act - Perform the action
       response = client.post("/api/features/", json=test_data)
       
       # Assert - Verify the results
       assert response.status_code == 201
       assert response.json()["name"] == "Test Feature"
   ```

2. **Test Edge Cases**
   - Invalid input data
   - Missing required fields
   - Database constraints
   - Error conditions

3. **Use Descriptive Test Names**
   ```python
   def test_create_card_with_valid_data_returns_201():
       # Test implementation
       pass

   def test_create_card_with_missing_front_returns_422():
       # Test implementation
       pass
   ```

4. **Isolate Tests**
   ```python
   @pytest.fixture(autouse=True)
   def setup_and_teardown():
       Base.metadata.create_all(bind=engine)
       yield
       Base.metadata.drop_all(bind=engine)
   ```

### Running Tests

```bash
# Run all tests
source .venv/bin/activate
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_cards.py -v

# Run specific test
python3 -m pytest tests/test_cards.py::test_create_card_success -v

# Run tests with coverage
python3 -m pytest tests/ --cov=app --cov-report=html
```

## 📝 Code Style and Standards

### Python Code Style

- **Follow PEP 8** for Python code formatting
- **Use type hints** for function parameters and return values
- **Write docstrings** for classes and functions
- **Keep functions small** and focused on single responsibilities

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def get_due_cards(db: Session, deck_name: Optional[str] = None, limit: int = 20) -> List[Card]:
    """
    Retrieve cards that are due for review.
    
    Args:
        db: Database session
        deck_name: Optional deck filter
        limit: Maximum number of cards to return
        
    Returns:
        List of Card objects due for review
    """
    query = db.query(Card).filter(Card.next_review <= datetime.now())
    
    if deck_name:
        query = query.filter(Card.deck_name == deck_name)
        
    return query.limit(limit).all()
```

### API Design Principles

1. **RESTful Endpoints**
   ```
   GET    /api/cards/           # List resources
   POST   /api/cards/           # Create resource
   GET    /api/cards/{id}       # Get specific resource
   PUT    /api/cards/{id}       # Update resource
   DELETE /api/cards/{id}       # Delete resource
   ```

2. **Consistent Response Formats**
   ```python
   # Success responses
   {"id": 1, "name": "Card Name", "created_at": "2023-01-01T00:00:00Z"}
   
   # Error responses
   {"detail": "Card not found"}
   {"detail": [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]}
   ```

3. **Proper HTTP Status Codes**
   - `200 OK` - Successful GET, PUT
   - `201 Created` - Successful POST
   - `204 No Content` - Successful DELETE
   - `400 Bad Request` - Invalid input
   - `404 Not Found` - Resource not found
   - `422 Unprocessable Entity` - Validation errors

### Database Best Practices

1. **Use Proper Relationships**
   ```python
   class StudySession(Base):
       __tablename__ = "study_sessions"
       
       id = Column(Integer, primary_key=True)
       user_id = Column(Integer, ForeignKey("users.id"))
       
       # Relationship
       user = relationship("User", back_populates="sessions")
   ```

2. **Add Indexes for Performance**
   ```python
   class Card(Base):
       __tablename__ = "cards"
       
       id = Column(Integer, primary_key=True, index=True)
       deck_name = Column(String(100), index=True)  # Frequently queried
       next_review = Column(DateTime, index=True)   # Used in filtering
   ```

3. **Use Appropriate Data Types**
   ```python
   # Good
   ease_factor = Column(Float, default=2.5)
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   
   # Avoid
   ease_factor = Column(String)  # Should be numeric
   created_at = Column(String)   # Should be datetime
   ```

## 🔍 Code Review Process

### Before Submitting a Pull Request

1. **Self-Review Checklist**
   - [ ] All tests pass locally
   - [ ] Code follows project style guidelines
   - [ ] New features have comprehensive tests
   - [ ] Documentation is updated if needed
   - [ ] No debugging code or console.log statements
   - [ ] Database migrations are safe and tested

2. **Run Quality Checks**
   ```bash
   # Run all tests
   python3 -m pytest tests/ -v
   
   # Check code formatting (if using black)
   black --check app/ tests/
   
   # Check imports (if using isort)
   isort --check-only app/ tests/
   ```

### Pull Request Guidelines

1. **Create Descriptive PRs**
   ```markdown
   ## Description
   Brief description of changes and motivation.
   
   ## Changes Made
   - Added new endpoint for feature X
   - Updated database schema for Y
   - Fixed bug in Z functionality
   
   ## Testing
   - [ ] All existing tests pass
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed
   
   ## Documentation
   - [ ] README updated if needed
   - [ ] API documentation reflects changes
   ```

2. **Link Related Issues**
   ```markdown
   Closes #123
   Related to #456
   ```

3. **Keep PRs Focused**
   - One feature or bug fix per PR
   - Avoid mixing unrelated changes
   - Keep changes as small as reasonable

## 🐛 Bug Reports and Feature Requests

### Reporting Bugs

Use the GitHub issue template and include:

1. **Environment Information**
   - Python version
   - Operating system
   - Dependencies versions

2. **Steps to Reproduce**
   ```markdown
   1. Start the server with `uvicorn app.main:app --reload`
   2. Send POST request to `/api/cards/` with data: {...}
   3. Observe error response
   ```

3. **Expected vs Actual Behavior**
   - What you expected to happen
   - What actually happened
   - Error messages or logs

4. **Additional Context**
   - Screenshots if applicable
   - Related code snippets
   - Possible solutions you've considered

### Feature Requests

1. **Describe the Problem**
   - What problem does this feature solve?
   - Who would benefit from this feature?

2. **Propose a Solution**
   - Detailed description of the proposed feature
   - How it would work from a user perspective
   - API design considerations

3. **Consider Alternatives**
   - Alternative solutions you've considered
   - Why this approach is preferred

## 📚 Learning Resources

### Spaced Repetition and Memory Science

- **Research Papers**
  - Ebbinghaus, H. (1885). Memory: A Contribution to Experimental Psychology
  - Wozniak, P. A. (1990). Optimization of learning
  - Cepeda, N. J., et al. (2006). Distributed practice in verbal recall tasks

- **Algorithms**
  - [SM-2 Algorithm](https://www.supermemo.com/en/archives1990-2015/english/ol/sm2) - Current implementation
  - [FSRS Algorithm](https://github.com/open-spaced-repetition/fsrs4anki) - Future consideration

### Technical Resources

- **FastAPI**: [Official Documentation](https://fastapi.tiangolo.com/)
- **SQLAlchemy**: [ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- **Pytest**: [Testing Guide](https://docs.pytest.org/en/stable/)
- **Pydantic**: [Data Validation](https://pydantic-docs.helpmanual.io/)

## 🤝 Community Guidelines

### Communication

- **Be respectful** and inclusive in all interactions
- **Ask questions** if you're unsure about anything
- **Share knowledge** and help other contributors
- **Give constructive feedback** in code reviews

### Getting Help

1. **Check existing documentation** first
2. **Search closed issues** for similar problems
3. **Ask in discussions** for general questions
4. **Create issues** for specific bugs or feature requests

### Recognition

Contributors are recognized in:
- README acknowledgments
- Release notes for significant contributions
- GitHub contributor statistics

## 🎉 Thank You!

Thank you for contributing to Mnemosyne! Your efforts help build a tool that can genuinely improve how people learn and remember. Every contribution, whether it's code, documentation, bug reports, or feature suggestions, makes a difference.

Together, we're building the future of memory and learning. Let's make it beautiful, effective, and accessible to all.

---

*"The best way to learn is to teach, and the best way to remember is to help others remember."*

**Welcome to the Mnemosyne community! 🧠✨**
