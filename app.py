from flask import Flask, request, jsonify 
from flask_cors import CORS  # Import CORS from flask_cors 
import pickle 
 
app = Flask(__name__) 
CORS(app)  # Enable CORS for all routes 
 
# Load the trained model and vectorizer 
with open('../ML/trained_model.pkl', 'rb') as model_file: 
    nb_classifier = pickle.load(model_file) 
 
with open('../ML/vectorizer.pkl', 'rb') as vectorizer_file: 
    vectorizer = pickle.load(vectorizer_file) 
 
@app.route('/categorize_news', methods=['POST']) 
def categorize_news(): 
    data = request.get_json() 
    news_data = data['newsData'] 
 
    # Vectorize the titles 
    titles = [article['title'] for article in news_data] 
    titles_tfidf = vectorizer.transform(titles) 
 
    # Predict categories 
    predicted_categories = nb_classifier.predict(titles_tfidf) 
 
    # Create a dictionary to store categorized news 
    categorized_news = {} 
    for article, category in zip(news_data, predicted_categories): 
        # Include all attributes for each article 
        article.update({'category': category}) 
        if category not in categorized_news: 
            categorized_news[category] = [] 
        categorized_news[category].append(article) 
 
    # Add CORS headers to the response 
    response = jsonify(categorized_news) 
    response.headers.add('Access-Control-Allow-Origin', '*') 
    response.headers.add('Access-Control-Allow-Methods', 'POST') 
 
    return response 
@app.route('/recommended_news', methods=['POST']) 
def recommended_news(): 
    data = request.get_json() 
    categorized_news = data['categorizedNews'] 
    recentlyviewed_news=data['recentlyViewedArticles']
    recommended_news=[]
    categories = [article['category'] for article in recentlyviewed_news] 
    categories.sort()
    Categories=[]
    for category in categories:
        if(category not in Categories):
            Categories.append(category)
    if len(Categories)>0:
        for article in categorized_news[Categories[0]]:
            if(article['title'] not in recentlyviewed_news):
                recommended_news.append(article)
    if len(Categories)>1:
        for article in categorized_news[Categories[1]]:
            if(article['title'] not in recentlyviewed_news):
                recommended_news.append(article)
    if len(Categories)>2:
        for article in categorized_news[Categories[2]]:
            if(article['title'] not in recentlyviewed_news):
                recommended_news.append(article)
    # Add CORS headers to the response 
    response = jsonify(recommended_news) 
    response.headers.add('Access-Control-Allow-Origin', '*') 
    response.headers.add('Access-Control-Allow-Methods', 'POST') 
    return response 
