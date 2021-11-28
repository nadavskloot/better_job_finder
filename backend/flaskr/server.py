from flask import Flask
from database import Database

app = Flask(__name__)

db = Database(app)

if __name__ == '__main__':
    app.run(debug=True)
