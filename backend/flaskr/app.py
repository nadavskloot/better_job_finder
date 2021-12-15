from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pprint
import sys
sys.path.append('../')
from scrapers import linkedin_scraping
from scrapers import indeed_scraping

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
CORS(app)

# SQLAlchemy attaches database to app
# Marshmallow allows for conversion of database data to different data types
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database of jobs
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)
    job_title = db.Column(db.String(200), nullable=False)
    employer = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    salary = db.Column(db.Integer, nullable=True)
    required_skills = db.Column(db.String(200), nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    education_level = db.Column(db.String(200), nullable=True)
    employment_type = db.Column(db.String(200), nullable=True)
    job_post_link = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return '(Job Title: %r)' % self.job_title

# Resets and re-creates the database each time the server restarts
db.drop_all()
db.create_all()
db.session.commit()

# Schema for converting the data in Jobs database to dictionary format
# Necessary for sending Jobs data as json to the frontend
class JobsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jobs

# Receives search data from the frontend and then returns a response object
@app.route("/getSearchResults", methods=['POST', 'GET'])
def getSearchResults():

    # If POST request, execute job search query using web-scrapers
    if request.method == 'POST':
        db.session.query(Jobs).delete()
        db.session.commit()
        userSearch = dict(request.get_json())
        allJobs = []
        linkedinJobs = linkedin_scraping.main(userSearch)
        allJobs.extend(linkedinJobs)
        # for job in linkedinJobs:
        #     job["required_skills"] = str(job["required_skills"])
        #     job["education_level"] = str(job["education_level"])
        #     db.session.add(Jobs(**job))
        #     db.session.commit()
        indeedJobs = indeed_scraping.main(userSearch)
        allJobs.extend(indeedJobs)
        for job in allJobs:
            job["required_skills"] = str(job["required_skills"])
            job["education_level"] = str(job["education_level"])
            db.session.add(Jobs(**job))
            db.session.commit()
        # pp = pprint.PrettyPrinter()
        # pp.pprint(linkedinJobs)
        return jsonify(allJobs)
    # If GET request, retrieve Jobs database data and send to frontend
    else:
        jobs = Jobs.query.order_by(Jobs.score * -1).all()
        jobs_schema = JobsSchema(many=True)
        output = jobs_schema.dump(jobs)
        return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
