from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class MovieSchemaIn(BaseModel):
    title: str
    description: str
    genre: str
    rating: int = Field(ge=0, le=5)
    release_date: date
    language: Optional[str] = None
    duration: Optional[int] = None

    @field_validator('title', 'description', 'genre', mode='before')
    @classmethod
    def validate_empty_fields(cls, value: str) -> str:
        if not value or value == ' ':
            raise ValueError('must not be empty str')
        return value

    @field_validator('release_date', mode='before')
    def validate_none_fields(cls, value: date) -> date:
        if not value:
            raise ValueError('must not be null')
        return value


class MovieSchema(MovieSchemaIn):
    id: int


class UpdateMovieSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    genre: Optional[str] = None
    rating: Optional[int] = None
    release_date: Optional[date] = None
    language: Optional[str] = None
    duration: Optional[int] = None

    @field_validator('title', 'description', 'genre', mode='before')
    @classmethod
    def validate_empty_fields(cls, value: str) -> str:
        if not value or value == ' ':
            raise ValueError('must not be empty str')
        return value
