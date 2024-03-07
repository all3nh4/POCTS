from flask import Flask, jsonify, redirect, request, render_template, url_for
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
app.config['SQLALCHEMY_ECHO'] = True

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


class MarketTrends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120)) 
    startDate = db.Column(db.String(50))
    status = db.Column(db.String(50))
    sources = db.Column(db.String(500))
    analysis = db.Column(db.Text)
    
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
    for _ in range(10):
        sources_list = [fake.url() for _ in range(2)]
        trend = MarketTrends(
        name=fake.company(),
        category=choice(industries),
        startDate=str(fake.past_date()),
        status=choice(["Active", "Emerging", "Declining"]),
        sources=[fake.url() for _ in range(2)],
        analysis=fake.paragraph(nb_sentences=2)
        )
        db.session.add(trend)
        trends.append(trend)
    try:
        db.session.commit()
        
    except Exception as e:
        print(f"error{e}")

    return trends

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

@app.route('/market-trend/2', methods=['GET'])
def get_market_trend_by_id():
    trend = MarketTrends.query.filter_by(id=2).first()

    if trend:
        trend_data = {
            "id": trend.id,
            "name": trend.name,
            "category": trend.category,
            "startDate": trend.startDate,
            "status": trend.status,
            "sources": trend.sources,
            "analysis": trend.analysis
        }
        return jsonify(trend_data)
    else:
        return jsonify({"message": "Market trend not found"}), 401



@app.route('/market-trends', methods=['GET'])
def get_market_trends_route():
    trends= fetch_market_trends()
    return render_template('market_trends.html', trends=trends)
    #return trends

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

@app.route('/submit-sector', methods=['POST'])
def submit_sector():
    sector = request.form['sector']
    keywords = ['keyword1', 'keyword2']  # Example keywords related to the sector

    # Step 1: Gather data from Twitter (pseudo-code)
    twitter_data = gather_data_from_twitter(keywords)

    # Step 2: Gather data from news API (pseudo-code)
    news_data = gather_data_from_news_api(keywords)

    # Step 3: Scrape blogs for relevant posts (pseudo-code)
    blog_data = scrape_blogs_for_data(keywords)

    # Combine all data into a single text block for analysis
    combined_text = twitter_data + news_data + blog_data

    # Step 4: Store the combined text data in Azure Blob Storage
    store_data_in_azure(combined_text, sector)

    # Step 5: Analyze the combined text with OpenAI (pseudo-code)
    analysis_results = analyze_with_openai(combined_text)

    return jsonify(analysis_results)

def gather_data_from_twitter(keywords):
    # Pseudo-code for gathering data from Twitter
    # Use Twitter API to search for tweets containing the keywords
    return "Data from Twitter"

def gather_data_from_news_api(keywords):
    # Pseudo-code for gathering data from a news API
    # Use a news API to fetch articles related to the keywords
    return "Data from news API"

def scrape_blogs_for_data(keywords):
    # Pseudo-code for scraping blogs
    # Use web scraping techniques to gather relevant blog posts
    return "Data from blogs"

def store_data_in_azure(data, sector):
    # Pseudo-code for storing data in Azure Blob Storage
    # Use Azure Blob Storage SDK to upload the combined data
    blob_service_client = azure.storage.blob.BlobServiceClient.from_connection_string('your_connection_string')
    blob_client = blob_service_client.get_blob_client(container='your_container', blob=f'{sector}_data.txt')
    blob_client.upload_blob(data)

def analyze_with_openai(text):
    # Pseudo-code for analyzing text with OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(engine="davinci", prompt=text, max_tokens=50)
    return response.choices[0].text.strip()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Tables were created successfully!")
    app.run(debug=True)