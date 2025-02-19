import logging

from fastapi import APIRouter, HTTPException

from models.api.movies import MovieReq
from services.movies import MovieService

router = APIRouter(
    prefix="/v1/movies",
    tags=["movies"],
)


# List movies with pagination and sorting by title
@router.get("/")
async def list_movies(limit: int = 10, page: int = 1):
    logging.info(f"Fetching movies with limit {limit} and page {page}")
    return await MovieService().list_movies_from_firestore(limit, page)


# Get a single movie by ID
@router.get("/{movie_id}")
async def get_movie(movie_id: str):
    logging.info(f"Fetching movie with ID {movie_id}")
    return await MovieService().get_movie_by_id(movie_id)


# Get a movie by title (case insensitive search)
@router.get("/search")
async def get_movie_by_title(title: str | None = None):
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    logging.info(f"Fetching movie with title {title}")
    return await MovieService().get_movie_by_title(title)


# Add a new movie to Firestore by fetching details from OMDB
@router.post("/")
async def add_movie(req: MovieReq):
    info, status = await MovieService().add_movie(req)
    return {"message": info, "status": status}
