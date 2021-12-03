from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///jobs.db'

db = SQLAlchemy(app)

# Database of jobs
class Jobs(db.model):
    id = db.column(db.Integer, primary_key = True)
    job_title = db.column(db.String(200), nullable = False)
    employer = db.column(db.String(200), nullable = False)
    location = db.column(db.String(200))
    yearly_income = db.column(db.String(200))
    required_skills = db.column(db.String(200))
    years_experience = db.column(db.String(200))
    education_level = db.column(db.String(200))
    employment_type = db.column(db.String(200))
    job_post_link = db.column(db.String(300))

    def get(self, id = None):
        if id:
            return self.model.query.get(id)
        return self.model.query.all()

if __name__ == '__main__':
    app.run(debug=True)
