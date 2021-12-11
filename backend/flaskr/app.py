from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pprint
import sys
sys.path.append('../')
from scrapers import linkedin_scraping

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
CORS(app, resources={r'/*': {'origins': '*'}})
# app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database of jobs
class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    score = db.Column(db.Integer)
    job_title = db.Column(db.String(200), nullable = False)
    employer = db.Column(db.String(200), nullable = False)
    location = db.Column(db.String(200))
    salary = db.Column(db.String(200))
    # required_skills = db.Column(db.String(200))
    # years_experience = db.Column(db.String(200))
    # education_level = db.Column(db.String(200))
    # employment_type = db.Column(db.String(200))
    job_post_link = db.Column(db.String(300))

    def __repr__(self):
        return '(Job Title: %r)' % self.job_title

class JobsSchema(ma.ModelSchema):
    class Meta:
        model = Jobs

# Receives search data from the frontend and then returns a response object
@app.route("/getSearchResults", methods=['POST', 'GET'])
# @cross_origin(origin="*", headers=['content-type'])
def getSearchResults():
    response_object = {'status': 'success'}
    print(request.get_json())
    
    
    if request.method == 'POST':
        db.drop_all()
        userSearch = dict(request.get_json())
        linkedinJobs = linkedin_scraping.main(userSearch)
        pp = pprint.PrettyPrinter()
        pp.pprint(linkedinJobs)
        return jsonify(response_object)
    else:
        new_job = Jobs(
            score = 2,
            job_title = "Software Engineer",
            employer = "Google",
            location = "San Francisco",
            salary = "$100,000",
            job_post_link = "www.google.com"
        )
        db.session.add(new_job)
        db.session.commit()
        another_job = Jobs(
            score = 1,
            job_title = "QA Engineer",
            employer = "Google",
            location = "San Francisco",
            salary = "$100,000",
            job_post_link = "www.google.com"
        )
        db.session.add(another_job)
        db.session.commit()
        jobs = Jobs.query.order_by(Jobs.score * -1).all()
        jobs_schema = JobsSchema(many=True)
        output = jobs_schema.dump(jobs).data
        print(type(jobs[0]), file=sys.stderr)
        # return jsonify(Jobs.query.order_by(Jobs.score * -1).all())
        return jsonify(output)

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)
