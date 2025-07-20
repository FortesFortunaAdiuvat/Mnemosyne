from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLite database URL
SQLALCHEMY_DATABASE_URL = settings.database_url or "sqlite:///./mnemosyne.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all tables in the database"""
    # Import all models to ensure they're registered with Base
    from app.models.card import Card
    from app.models.study_session import StudySession, CardReview
    from app.models.calendar import DailyActivity, StudyReminder
    
    # Create all tables using the shared Base
    Base.metadata.create_all(bind=engine)
