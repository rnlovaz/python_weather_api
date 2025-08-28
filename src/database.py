import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Load env variables
load_dotenv()

db_name = os.getenv("POSTGRES_DB", "weather_locations")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_host = os.getenv("POSTGRES_HOST", "0.0.0.0")

DATABASE_URL = (
    f"postgresql+psycopg://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}"
)

# echo=True logs SQL queries to the console
engine = create_engine(DATABASE_URL, echo=True)


# Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session
