import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.movies import MovieService

router = APIRouter(
    prefix="/v1/internal/movies",
    tags=["movies"],
)

# Authorization token (can be replaced with a more secure method)
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token")
security = HTTPBearer()

# OMDB API Configuration
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "83a26ab")
OMDB_URL = "http://www.omdbapi.com/"


# Utility function to validate authorization token
def authorize(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")


# Fetch 100 movies from OMDB and save them to Firestore
@router.get("/initialize")
async def initialize_database(
    credentials: HTTPAuthorizationCredentials = Depends(authorize),
):
    info = await MovieService().populate_database()
    return {"message": f"Database initialized with {len(info)} movies."}


# Add a new movie to Firestore by fetching details from OMDB
@router.post("/")
async def add_movie(
    title: str, credentials: HTTPAuthorizationCredentials = Depends(authorize)
):
    info = await MovieService().add_movie(title)
    return {"message": info}


# Remove a movie by ID
@router.delete("/{movie_id}")
async def delete_movie(
    movie_id: str, credentials: HTTPAuthorizationCredentials = Depends(authorize)
):
    await MovieService().delete_movie(movie_id)
    return {"message": "Movie deleted successfully"}
