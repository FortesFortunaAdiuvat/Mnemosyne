import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.card import Base

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_mnemosyne_bdd.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for BDD testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_bdd_test_database():
    """Set up test database for the entire BDD test session"""
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    yield
    # Clean up
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def setup_and_teardown_bdd():
    """Setup and teardown for each BDD test"""
    # Import all models to ensure they're registered
    from app.models.card import Card
    from app.models.study_session import StudySession, CardReview
    from app.models.calendar import DailyActivity, StudyReminder
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client for BDD tests"""
    return TestClient(app)


@pytest.fixture
def context():
    """Create context dictionary for sharing data between BDD steps"""
    return {}
