from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle

app = FastAPI(title="My Movie Recommender")

# --- CORS CONFIGURATION ---
# This tells the browser it is safe for localhost:3000 to talk to 127.0.0.1:8000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the movie names and our trained brain when the server starts
movies_df = pd.read_csv('movies.csv')
with open('svd_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Helper function to turn a Movie ID into a real Movie Title
def get_movie_title(movie_id):
    movie = movies_df[movies_df['movieId'] == movie_id]
    if not movie.empty:
        return movie.iloc[0]['title']
    return "Unknown Movie"

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: int):
    all_movie_ids = movies_df['movieId'].unique()
    predictions = []
    
    for m_id in all_movie_ids:
        prediction = model.predict(uid=user_id, iid=m_id)
        predictions.append((m_id, prediction.est))
        
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_5 = predictions[:5]
    
    results = []
    for m_id, estimated_rating in top_5:
        results.append({
            "title": get_movie_title(m_id),
            "predicted_stars": round(estimated_rating, 2)
        })
        
    return {"user_id": user_id, "top_picks": results}