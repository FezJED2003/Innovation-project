import pandas as pd
import csv
import sys
import nltk
from flask import Flask, request, jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import json
import requests
import ast  # For safely evaluating JSON-like strings

# Increase CSV buffer size
csv.field_size_limit(10_000_000)

# Create Flask app
app = Flask(__name__)

# Manually set CORS headers to allow cross-origin requests
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all domains
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow specific headers
    return response

# Load CSV files with 'id' as string for safety
movies_df = pd.read_csv("imdb_movies.csv", dtype={'id': str})
credits_df = pd.read_csv("movie_data.csv", engine="python", dtype={'id': str})

# Standardize column names by stripping spaces and converting to lowercase
movies_df.columns = movies_df.columns.str.strip().str.lower()
credits_df.columns = credits_df.columns.str.strip().str.lower()

# Check if 'id' exists in both DataFrames
if 'id' in movies_df.columns and 'id' in credits_df.columns:
    # Remove rows with non-numeric or missing 'id' values
    movies_df = movies_df[movies_df['id'].str.isnumeric()]
    credits_df = credits_df[credits_df['id'].str.isnumeric()]

    # Convert 'id' columns to integers
    movies_df['id'] = movies_df['id'].astype(int)
    credits_df['id'] = credits_df['id'].astype(int)

    # Merge the DataFrames based on 'id'
    movies_df = movies_df.merge(credits_df, on='id', how='left')
    print("\n Data loaded and merged successfully!\n")
else:
    print("\n Error: 'id' column is missing in one or both DataFrames.\n")

# Print column names to verify merge
print("🎯 Column names in movies_df after merging:", movies_df.columns.tolist())
print("🎯 Column names in credits_df:", credits_df.columns.tolist())

# Print first few rows for verification
print("\n📊 Sample data from movies_df:")
print(movies_df.head())

print("\n📊 Sample data from credits_df:")
print(credits_df.head())

# my API key
TMDB_API_KEY = "3cb6a2c6a362a17415a5eeca2df7f971"

# Function to fetch genres from TMDb API
def fetch_genres(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie_id = data["results"][0]["id"]
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
            details_response = requests.get(details_url)
            if details_response.status_code == 200:
                details = details_response.json()
                return [genre["name"] for genre in details.get("genres", [])]
    return ["Unknown"]

# Add genres if missing
if 'genres' not in movies_df.columns:
    print("\nGenres column is missing. Fetching from TMDb API...")
    movies_df['genres'] = movies_df['names'].apply(fetch_genres)

# Function to extract cast/crew names from JSON-like column
def extract_names(data):
    try:
        people = ast.literal_eval(data)  # Convert string to list of dictionaries
        return [person["name"] for person in people[:5]]  # Return first 5 names
    except:
        return ["Unknown"]

# Extract names from cast & crew columns
movies_df["cast_names"] = movies_df["cast"].apply(extract_names)
movies_df["crew_names"] = movies_df["crew"].apply(extract_names)

# Function to fetch keywords from TMDb API
def fetch_keywords(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={TMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie_id = data["results"][0]["id"]
            keywords_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}"
            keywords_response = requests.get(keywords_url)
            if keywords_response.status_code == 200:
                keywords_data = keywords_response.json()
                return [kw["name"] for kw in keywords_data.get("keywords", [])]
    return ["Unknown"]

if 'keywords' not in movies_df.columns:
    print("\nKeywords column is missing. Fetching from TMDb API...")
    movies_df["keywords"] = movies_df["names"].apply(fetch_keywords)

# Initialize NLP
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# Function to get recommendations
def get_recommendations(movie_title):
    movie_title = movie_title.lower()
    results = movies_df[movies_df["names"].str.lower().str.contains(movie_title, na=False)]
    
    if not results.empty:
        return results[["names", "genres", "keywords", "cast_names"]].head(5).to_dict(orient="records")
    else:
        return fetch_tmdb_recommendations(movie_title)

# Fetch recommendations from TMDb if not found in dataset
def fetch_tmdb_recommendations(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            movie_id = data["results"][0]["id"]
            rec_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
            rec_response = requests.get(rec_url)
            if rec_response.status_code == 200:
                rec_data = rec_response.json()
                return [{"title": movie["title"], "rating": movie["vote_average"]} for movie in rec_data["results"][:5]]
    return [{"title": "No recommendations found."}]

# Flask API to get recommendations
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    movie_title = data.get("movie_title", "")
    
    if not movie_title:
        return jsonify({"error": "Movie title is required!"}), 400

    recommendations = get_recommendations(movie_title)
    return jsonify(recommendations)

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)

# Print the entire dataset (use with caution for large datasets)
print("\nFull movies_df Data:")
print(movies_df.to_string())  

print("\n Full credits_df Data:")
print(credits_df.to_string()) 
