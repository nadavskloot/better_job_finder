from flask_sqlalchemy import SQLAlchemy

class Database:
    def __init__(self, app):
        db = SQLAlchemy(app)
        self.db = db
        self.model = jobFactory(db)

    def get(self, id=None):
        if id:
            return self.model.query.get(id)
        return self.model.query.all()

    def create():
        return 0

def jobFactory(db):
    class Job(db.model):
        __tablename__ = 'jobs'

        def __init__(self, title):
            self.title = title
    return Job