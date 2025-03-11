import os


class Config:
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///api-bank.sqlite"
    JWT_SECRET_KEY = "super-secret"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "super-test"
