from fastapi import HTTPException

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


async def test_get_movie_by_id():
    movie = await svc.get_movie_by_id("4bdecc86-635b-4d63-86f5-2760aa5e6982")
    assert movie
    assert movie.title == "Sobre las olas"


async def test_get_movie_by_title():
    movie = await svc.get_movie_by_title("Las Vegas")
    assert movie
    assert movie.title == "Las Vegas"


async def test_add_movie_already_exists_in_firestore():
    info = await svc.add_movie("las vegas")
    assert info


async def test_add_movie_not_exists_in_firestore():
    info = await svc.add_movie("el zorro")
    assert info
