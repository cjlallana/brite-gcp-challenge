from typing import Any, Optional
from uuid import uuid4

from pydantic import ConfigDict, Field, computed_field, model_validator
from pydantic.alias_generators import to_pascal

from models.db import DBModel


class Movie(DBModel):
    movie_id: str = Field(alias="_id", default_factory=lambda: str(uuid4()))
    title: str
    year: int
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
    imdb_id: str
    type: Optional[str] = None
    dvd: Optional[str] = None
    box_office: Optional[str] = None
    production: Optional[str] = None
    website: Optional[str] = None

    model_config = ConfigDict(alias_generator=to_pascal, populate_by_name=True)

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
    def capitalize_fields(cls, data: Any) -> Any:
        """
        As OMDB API returns some field names in PascalCase and others in camelCase,
        this method capitalizes the first letter of each field so they are consistent.
        There might be some specific fields that need a special treatment as well.
        The method is intended to be used before data is parsed into the model.

        Args:
            data (Any): Input data that should be a dictionary with field names as keys.

        Returns:
            Any: A new dictionary with consistent field names.
        """
        if isinstance(data, dict):
            capitalized_data = {k[0].upper() + k[1:]: v for k, v in data.items()}
            capitalized_data["imdb_id"] = data.get("imdbID")  # special treatment

        return capitalized_data
