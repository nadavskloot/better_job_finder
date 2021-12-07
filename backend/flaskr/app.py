from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///jobs.db'

db = SQLAlchemy(app)

# Database of jobs
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer)
    job_title = db.Column(db.String(200), nullable = False)
    employer = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200))
    yearly_income = db.Column(db.String(200))
    required_skills = db.Column(db.String(200))
    years_experience = db.Column(db.String(200))
    education_level = db.Column(db.String(200))
    employment_type = db.Column(db.String(200))
    job_post_link = db.Column(db.String(300))

    def get(self, id = None):
        if id:
            return self.model.query.get(id)
        return self.model.query.all()

# Receives search data from the frontend and then returns a response object
@app.route("/search", methods=['POST', 'GET'])
def search():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)
