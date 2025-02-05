from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from core.fastapi_config import app
from models.db.movies import Movie

client = TestClient(app)

MOCK_OMDB_API_RESPONSE = {
    "Title": "Guardians of the Galaxy Vol. 2",
    "Year": "2017",
    "Rated": "PG-13",
    "Released": "05 May 2017",
    "Runtime": "136 min",
    "Genre": "Action, Adventure, Comedy",
    "Director": "James Gunn",
    "Writer": "James Gunn, Dan Abnett, Andy Lanning",
    "Actors": "Chris Pratt, Zoe Saldana, Dave Bautista",
    "Plot": "The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father, the ambitious celestial being Ego.",
    "Language": "English",
    "Country": "United States",
    "Awards": "Nominated for 1 Oscar. 15 wins & 60 nominations total",
    "Poster": "https://m.media-amazon.com/images/M/MV5BNWE5MGI3MDctMmU5Ni00YzI2LWEzMTQtZGIyZDA5MzQzNDBhXkEyXkFqcGc@._V1_SX300.jpg",
    "Metascore": "67",
    "imdbRating": "7.6",
    "imdbVotes": "784,257",
    "imdbID": "tt3896198",
    "Type": "movie",
    "DVD": "N/A",
    "BoxOffice": "$389,813,101",
    "Production": "N/A",
    "Website": "N/A",
    "Response": "True",
}

MOCK_FIRESTORE_MOVIE = {
    "id": "1",
    "title": "The Matrix",
    "year": "1999",
    "genre": "Action, Sci-Fi",
    "director": "Lana Wachowski, Lilly Wachowski",
    "plot": "A computer hacker learns about the true nature of reality.",
}


def test_movie_model():
    movie = Movie(**MOCK_OMDB_API_RESPONSE)

    assert movie.title == "Guardians of the Galaxy Vol. 2"
    assert movie.year == 2017
    assert movie.imdb_id


def test_api():
    response = client.get("/v1/")
    assert response.status_code == 200


@patch("api.v1.public.movies.movies_ref")
def test_api_get_movie_by_id(mock_movies_ref):
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = MOCK_FIRESTORE_MOVIE
    mock_movies_ref.document.return_value.get.return_value = (
        mock_doc  # Ensure get() works
    )

    response = client.get("/v1/movies/1")
    assert response.status_code == 200
    assert response.json()["title"] == "The Matrix"
