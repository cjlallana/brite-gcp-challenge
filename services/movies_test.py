from unittest.mock import patch

from fastapi import HTTPException

from models.api.movies import MovieReq
from models.db.movies import Movie
from services.movies import MovieService

svc = MovieService()


async def test_retrieve_100_movies_from_omdb():
    movies = await svc.retrieve_100_movies_from_omdb()
    assert movies
    assert len(movies) == 100
    assert movies[1].title


async def test_retrieve_movie_from_omdb():
    movie = await svc.retrieve_movie_from_omdb("las vegas")
    assert movie
    assert movie.title == "Las Vegas"
    assert movie.title_lower == "las vegas"


async def test_populate_database():
    try:
        write_info = await svc.populate_database()
    except HTTPException as e:  # If database is already populated
        assert e.status_code == 400
    else:
        assert write_info
        assert len(write_info) == 100


async def test_get_movies_from_firestore():
    movies = await svc.list_movies_from_firestore()
    assert movies
    assert len(movies) == 10


async def test_get_movies_from_firestore_with_limit():
    movies = await svc.list_movies_from_firestore(limit=20)
    assert movies
    assert len(movies) == 20


async def test_get_movies_from_firestore_with_pagination():
    movies_page1 = await svc.list_movies_from_firestore()
    assert movies_page1
    assert len(movies_page1) == 10

    movies_page2 = await svc.list_movies_from_firestore(page=2)
    assert movies_page2
    assert len(movies_page2) == 10

    assert movies_page1[0].title != movies_page2[0].title
    assert movies_page1 != movies_page2


# async def test_get_movie_by_id():
#     movie = await svc.get_movie_by_id("4bdecc86-635b-4d63-86f5-2760aa5e6982")
#     assert movie
#     assert movie.title == "Sobre las olas"


# async def test_get_movie_by_title():
#     movie = await svc.get_movie_by_title("Las Vegas")
#     assert movie
#     assert movie.title == "Las Vegas"


@patch("services.movies.MovieService._get_movie_by_title")
async def test_add_movie_already_exists_in_firestore(mock_get_movie_by_title):
    # Pretend the movie already exists and has full details
    mock_get_movie_by_title.return_value = Movie(
        movie_id="mock_id",
        title="el zorro",
        year=2000,
        imdb_id="mock_id",
        full_details=True,
    )

    req = MovieReq(title="el zorro")
    info, status = await svc.add_movie(req)
    assert info == "Movie already exists in Firestore"
    assert status == 200


@patch("services.movies.movies_ref")
async def test_add_movie_not_exists_in_firestore(mock_movies_ref):
    # Avoid actually adding it
    mock_movies_ref.document.return_value.set.return_value = True

    req = MovieReq(title="el zorro")
    info, status = await svc.add_movie(req)

    assert info == "Movie added successfully"
    assert status == 201
