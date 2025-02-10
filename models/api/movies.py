from pydantic import Field

from models.api import ApiBaseModel


class MovieRes(ApiBaseModel):
    movie_id: str = Field(alias="_id")
    title: str
    year: int
    imdb_id: str


class MovieReq(ApiBaseModel):
    title: str
