from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/allenhafezipour/projects/TrendScope/Trendscope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class AlertSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    trend_keyword = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return "Welcome to TrendScope!"

# Additional routes...

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
