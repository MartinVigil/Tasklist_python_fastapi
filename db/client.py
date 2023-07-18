from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:KJtE0dqR8FjNY10OqGEe@containers-us-west-141.railway.app:6619/railway")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
