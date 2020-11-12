class mitocwRouter:
    """
    A router to control all database operations on models in the
    mitocw application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read mitocw models go to mitocw_db.
        """
        if model._meta.app_label == 'mitocw':
            return 'mitocw_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the mitocw app only appears in the 'mitocw_db'
        database.
        """
        if app_label == 'mitocw':
            return db == 'mitocw_db'
        return None

class nptelRouter:
    """
    A router to control all database operations on models in the
    nptel application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read nptel models go to nptel_db.
        """
        if model._meta.app_label == 'nptel':
            return 'nptel_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write nptel models go to nptel_db.
        """
        if model._meta.app_label == 'nptel':
            return 'nptel_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the nptel app only appears in the 'nptel_db'
        database.
        """
        if app_label == 'nptel':
            return db == 'nptel_db'
        return None

class udacityRouter:
    """
    A router to control all database operations on models in the
    udacity application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read udacity models go to udacity_db.
        """
        if model._meta.app_label == 'udacity':
            return 'udacity_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the udacity app only appears in the 'udacity_db'
        database.
        """
        if app_label == 'udacity':
            return db == 'udacity_db'
        return None
