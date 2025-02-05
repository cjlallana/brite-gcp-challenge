import os

from fastapi import HTTPException

from api import app
from core.firestore_config import db
from services.movies import MovieService

# OMDB API Configuration
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "83a26ab")
OMDB_URL = "http://www.omdbapi.com/"


# Fetch 100 movies from OMDB and save them to Firestore
@app.get("/initialize")
async def initialize_database():
    info = await MovieService().populate_database()
    return {"message": f"Database initialized with {len(info)} movies."}


# Add a new movie to Firestore by fetching details from OMDB
@app.post("/movies")
async def add_movie(title: str):
    response = requests.get(OMDB_URL, params={"apikey": OMDB_API_KEY, "t": title})
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            db.collection(MOVIES_COLLECTION).document(data["imdbID"]).set(data)
            return {"message": "Movie added successfully"}
        raise HTTPException(status_code=404, detail="Movie not found in OMDB")
    raise HTTPException(status_code=500, detail="Failed to fetch movie from OMDB")
