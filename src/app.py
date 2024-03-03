from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate
from faker import Faker
from random import choice
import sqlite3
import os 
import json

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Trendscope.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Faker
fake = Faker()
Faker.seed(0)

# database model(s)
class AlertSubscription(db.Model):
    print( "on Alert subscription class")
    id = db.Column(db.Integer, primary_key=True)
    print("id :"+ id )
    email = db.Column(db.String(120), unique=True, nullable=False)
    trend_keyword = db.Column(db.String(120), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)

def create_alert_subscription(email, trend_keyword, frequency):
    return {
        "email": email,
        "trend_keyword": trend_keyword,
        "frequency": frequency
    }

def save_alert_subscription(subscription):
    try:
        with open('subscriptions.json', 'r+') as file:
            subscriptions = json.load(file)
            subscriptions.append(subscription)
            file.seek(0)
            json.dump(subscriptions, file, indent=4)
    except FileNotFoundError:
        with open('subscriptions.json', 'w') as file:
            json.dump([subscription], file, indent=4)
    
           
# Define utility functions here
industries = ['Technology', 'Finance', 'Healthcare', 'Education', 'Entertainment']
def fetch_market_trends():
    trends = []
    for _ in range(10):  # Generate 10 dummy trends
        trends.append({
            "id": fake.random_int(min=1, max=100),
            "name": fake.company(),
            "category": choice(industries),
            "startDate": str(fake.past_date()),
            "status": choice(["Active", "Emerging", "Declining"]),
            "sources": [fake.url() for _ in range(2)],
            "analysis": fake.paragraph(nb_sentences=2),
        })
    return jsonify(trends)

def setupAlerts():
    data = request.json
    print("Received alert setup request:", data)
    # Here you would include logic to save the alert to the database
    return jsonify({"message": "Alert set up successfully", "data": data})

# Define your route handlers here
@app.route('/')
def home():
    return "Welcome to TrendScope!"

@app.route('/subscribe', methods=['GET'])
def subscribe():
    return render_template('subscribe.html')

@app.route('/market-trends', methods=['GET'])
def get_market_trends_route():
    trends= fetch_market_trends()
    return render_template('market_trends.html', trends=trends)

@app.route('/setup-alert', methods=['POST'])
def setup_alert():
    trend_name = request.form['trend']
    user_email = request.form['email']
    # For now, just print the information or log it
    print(f"Setting up alert for {user_email} on trend {trend_name}")
    # Redirect to a confirmation page or back to the trends page
    return redirect(url_for('market_trends'))


@app.route('/alerts', methods=['GET'])
def get_alerts_route():
    subscriptions = get_alert_subscriptions()
    return jsonify(subscriptions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Tables were created successfully!")
    app.run(debug=True)