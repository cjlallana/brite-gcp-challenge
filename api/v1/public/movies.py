import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.firestore_config import db, movies_ref
from services.movies import get_movie_by_id, get_movies_from_firestore

# Authorization token (can be replaced with a more secure method)
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "my_secret_token")
security = HTTPBearer()

router = APIRouter(
    prefix="/v1",
    tags=["movies"],
)


# Utility function to validate authorization token
def authorize(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized")


# Firestore collection name
MOVIES_COLLECTION = "movies"


@router.get("/")
async def root():
    return {"message": "Welcome to the Public API"}


# List movies with pagination and sorting by title
@router.get("/movies")
async def get_movies(limit: int = 10, page: int = 1):
    logging.info(f"Fetching movies with limit {limit} and page {page}")
    return await get_movies_from_firestore(limit, page)


# Get a single movie by ID
@router.get("/movies/{movie_id}")
async def get_movie(movie_id: str):
    return await get_movie_by_id(movie_id)


# Get a movie by title (case insensitive search)
@router.get("/movies/title/{title}")
async def get_movie_by_title(title: str):
    return await get_movie_by_title(title)


# Remove a movie by ID (protected)
@router.delete("/movies/{movie_id}")
async def delete_movie(
    movie_id: str, credentials: HTTPAuthorizationCredentials = Depends(authorize)
):
    movie_ref = db.collection(MOVIES_COLLECTION).document(movie_id)
    if not movie_ref.get().exists:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie_ref.delete()
    return {"message": "Movie deleted successfully"}
