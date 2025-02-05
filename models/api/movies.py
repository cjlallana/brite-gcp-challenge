from pydantic import UUID4, Field

from models.api import ApiBaseModel


class Movie(ApiBaseModel):
    movie_id: UUID4 = Field(alias="_id")
    title: str
    year: int
    imdb_id: str
