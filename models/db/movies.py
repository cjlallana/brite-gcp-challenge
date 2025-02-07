from typing import Any, Optional
from uuid import uuid4

from pydantic import Field, computed_field, model_validator
from pydantic.alias_generators import to_snake

from models.db import DBModel


class Movie(DBModel):
    movie_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    year: int
    imdb_id: str
    rated: Optional[str] = None
    released: Optional[str] = None
    runtime: Optional[str] = None
    genre: Optional[str] = None
    director: Optional[str] = None
    writer: Optional[str] = None
    actors: Optional[str] = None
    plot: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    awards: Optional[str] = None
    poster: Optional[str] = None
    metascore: Optional[str] = None
    imdb_rating: Optional[str] = None
    imdb_votes: Optional[str] = None
    type: Optional[str] = None
    dvd: Optional[str] = None
    box_office: Optional[str] = None
    production: Optional[str] = None
    website: Optional[str] = None

    # When fetching multiple movies, OMDB returns a list of simplified
    # results that do not contain full details.
    full_details: Optional[bool] = False

    @computed_field
    @property
    def title_lower(self) -> str:
        """We want to store the title in lowercase in the database for
        case insensitive search.

        Returns:
            str: The title in lowercase
        """
        assert self.title
        return self.title.lower()

    @model_validator(mode="before")
    @classmethod
    def omdb_to_snake_fields(cls, data: Any) -> Any:
        """
        As OMDB API returns some field names in PascalCase and others in camelCase,
        this method converts everything to snake_case, to be consistent with Python.

        Args:
            data (Any): Should be a dictionary with field names as keys.

        Returns:
            Any: A new dictionary with snake_case field names.
        """
        if isinstance(data, dict):
            snake_data = {to_snake(k): v for k, v in data.items()}

        return snake_data
