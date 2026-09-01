from app.database.database import engine, Base

# Import models so SQLAlchemy knows about them
from app.database import models


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")