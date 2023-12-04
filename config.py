# config.py
import os


class Config(object):
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    STORAGE = 'mongodb'

    # HATEOAS Configuration


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    DB_NAME = 'tasktracker'
    MONGO_URI = f"mongodb://localhost:27017/{DB_NAME}"


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # Production specific settings
    pass
