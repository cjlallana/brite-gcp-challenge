import os

import requests
from fastapi import HTTPException

from core.firestore_config import MOVIES_COLLECTION, db
from models.api.movies import Movie as MovieAPI
from models.db.movies import Movie as MovieDB

# OMDB API Configuration
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "83a26ab")
OMDB_URL = "http://www.omdbapi.com/"


class MovieService:

    # ---- OMDB API related methods ----
    async def retrieve_100_movies_from_omdb(self) -> list[MovieDB]:
        """
        Retrieve 100 movies from OMDB API.

        :return: A list of 100 Movie objects.
        """
        movies_dict: list[dict] = []
        for page in range(1, 11):  # 10 movies per page * 10 pages = 100 movies
            response = requests.get(
                OMDB_URL,
                params={
                    "apikey": OMDB_API_KEY,
                    "s": "las",
                    "type": "movie",
                    "page": page,
                },
            )
            if response.status_code == 200:
                data = response.json()
                if "Search" in data:
                    movies_dict.extend(data["Search"])
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to fetch data from OMDB"
                )

        movies = [MovieDB.model_validate(movie) for movie in movies_dict]
        return movies

    async def retrieve_movie_from_omdb(self, title: str) -> MovieDB:
        """
        Retrieve a movie from OMDB API by title.

        :param title: The title of the movie to retrieve.
        :return: A Movie object with the movie's data.
        :raises HTTPException: If the movie is not found in OMDB or there is an error
            while fetching the data.
        """

        response = requests.get(
            OMDB_URL, params={"apikey": OMDB_API_KEY, "type": "movie", "t": title}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("Response") == "True":
                return MovieDB.model_validate(data)
            raise HTTPException(status_code=404, detail="Movie not found in OMDB")
        raise HTTPException(status_code=500, detail="Failed to fetch movie from OMDB")

    # ---- Firestore related methods ----

    async def populate_database(self) -> list:
        # First, check that the database is not populated yet
        collection_ref = db.collection(MOVIES_COLLECTION)
        count_query = collection_ref.count()
        count_result = count_query.get()
        if count_result[0][0].value > 0:
            raise HTTPException(status_code=400, detail="Database is already populated")

        movies = await self.retrieve_100_movies_from_omdb()

        batch = db.batch()
        for movie in movies:
            doc_ref = db.collection(MOVIES_COLLECTION).document(movie.movie_id)
            batch.set(doc_ref, movie.model_dump())
        return batch.commit()

    async def get_movies_from_firestore(self, limit: int = 10, page: int = 1):
        movies_ref = db.collection(MOVIES_COLLECTION).order_by("title")
        movies = movies_ref.offset((page - 1) * limit).limit(limit).stream()

        return [MovieAPI.model_validate(movie.to_dict()) for movie in movies]

    async def get_movie_by_id(self, movie_id: str) -> MovieAPI:
        movie = db.collection(MOVIES_COLLECTION).document(movie_id).get()
        if not movie.exists:
            raise HTTPException(status_code=404, detail="Movie not found")
        return MovieAPI.model_validate(movie.to_dict())

    async def _list_movies_by_title(self, title: str) -> list[MovieAPI]:
        movies_ref = db.collection(MOVIES_COLLECTION)
        query = movies_ref.where("title_lower", "==", title.lower())
        movies = query.stream()

        return [MovieAPI.model_validate(movie.to_dict()) for movie in movies]

    async def get_movie_by_title(self, title: str) -> MovieAPI:
        movies_api = await self._list_movies_by_title(title)
        if not movies_api:
            raise HTTPException(status_code=404, detail="Movie not found")
        else:
            # We're supposed to retrieve only one movie
            return movies_api[0]

    async def add_movie(self, title: str):
        # Fetch full movie details from OMDB
        omdb_movie = await self.retrieve_movie_from_omdb(title)
        # Prepare to update or create the movie in Firestore
        movie_ref = db.collection(MOVIES_COLLECTION)

        # Check if a movie with the same title already exists in Firestore
        firestore_movies = await self._list_movies_by_title(omdb_movie.title)
        if firestore_movies:
            doc = movie_ref.document(firestore_movies[0].movie_id)
            doc.update(omdb_movie.model_dump())
            return {"message": "Movie updated successfully"}
        else:
            doc = movie_ref.document(omdb_movie.movie_id)
            doc.set(omdb_movie.model_dump())
            return {"message": "Movie added successfully"}

    async def delete_movie(self, movie_id: str):
        movie_ref = db.collection(MOVIES_COLLECTION).document(movie_id)
        if not movie_ref.get().exists:
            raise HTTPException(status_code=404, detail="Movie not found")
        movie_ref.delete()
