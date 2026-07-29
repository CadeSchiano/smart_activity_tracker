import os

# The production app deliberately refuses to start without this secret.
os.environ.setdefault("JWT_SECRET_KEY", "test-only-secret-that-is-at-least-32-characters")

from apps.database import Base, engine


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def pytest_runtest_setup(item):
    reset_database()
