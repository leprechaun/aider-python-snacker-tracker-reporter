from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./snacker_tracker.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)

class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
