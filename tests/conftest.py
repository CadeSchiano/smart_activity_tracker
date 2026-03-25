from apps.database import Base, engine


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def pytest_runtest_setup(item):
    reset_database()
