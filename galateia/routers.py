from django.db import router
from articles.models import MongoTest

class MongoRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model == MongoTest:
            return 'articles'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model == MongoTest:
            return 'articles'
        else:
            return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'articles':
            return db == 'articles'
        else:
            return db == 'default'
        return False
