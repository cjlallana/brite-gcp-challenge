from fastapi import HTTPException

from services.movies import (
    get_movie_by_id,
    get_movie_by_name,
    get_movies_from_firestore,
    populate_database,
    retrieve_movies_from_omdb,
)


async def test_retrieve_movies_from_omdb():
    movies = await retrieve_movies_from_omdb()
    assert movies
    assert len(movies) == 100
    assert movies[1].title


async def test_populate_database():
    try:
        write_info = await populate_database()
    except HTTPException as e:  # If database is already populated
        assert e.status_code == 400
    else:
        assert write_info
        assert len(write_info) == 100


async def test_get_movies_from_firestore():
    movies = await get_movies_from_firestore()
    assert movies
    assert len(movies) == 10


async def test_get_movies_from_firestore_with_limit():
    movies = await get_movies_from_firestore(limit=20)
    assert movies
    assert len(movies) == 20


async def test_get_movies_from_firestore_with_pagination():
    movies_page1 = await get_movies_from_firestore()
    assert movies_page1
    assert len(movies_page1) == 10

    movies_page2 = await get_movies_from_firestore(page=2)
    assert movies_page2
    assert len(movies_page2) == 10

    assert movies_page1[0].title != movies_page2[0].title
    assert movies_page1 != movies_page2


async def test_get_movie_by_id():
    movie = await get_movie_by_id("4bdecc86-635b-4d63-86f5-2760aa5e6982")
    assert movie
    assert movie.title == "Sobre las olas"


async def test_get_movie_by_name():
    movie = await get_movie_by_name("Sobre las olas")
    assert movie
    assert movie.title == "Sobre las olas"
