from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres.dlhnsfcfpwcyaurrxhez:pswd@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
    
    class Config:
        env_file = ".env"

settings = Settings() 

# SQLAlchemy engine and session setup using settings
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)