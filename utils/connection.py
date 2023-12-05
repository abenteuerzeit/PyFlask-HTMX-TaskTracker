import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def database_connection(func):
    """Decorator to ensure database connection before operation."""
    def wrapper(self, *args, **kwargs):
        if not self.client:
            self.initialize_db()
            if not self.client:
                logger.error("Operation failed: Database is not connected.")
                return None if func.__name__ != 'update_document' else False
        return func(self, *args, **kwargs)
    return wrapper
