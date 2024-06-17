# sentiment_analysis.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# mongodb+srv://doadmin:Q60nlM48hF5239cK@db-mongodb-sgp1-90661-5821cd72.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-sgp1-90661
# mongodb+srv://doadmin:<replace-with-your-password>@db-mongodb-sgp1-90661-5821cd72.mongo.ondigitalocean.com/sentiment_analysis?replicaSet=db-mongodb-sgp1-90661&tls=true&authSource=admin
# Awik@123@Wok

# Database setup
client = MongoClient('mongodb+srv://doadmin:Q60nlM48hF5239cK@db-mongodb-sgp1-90661-5821cd72.mongo.ondigitalocean.com/sentiment_analysis?replicaSet=db-mongodb-sgp1-90661&tls=true&authSource=admin')
db = client.sentiment_analysis
collection = db.history

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text', '')
    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    # Save to database
    collection.insert_one({'text': text, 'sentiment': sentiment})

    return jsonify({'sentiment': sentiment})

@app.route('/history', methods=['GET'])
def get_history():
    history = list(collection.find({},{'_id':0}).sort("_id",-1))
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)