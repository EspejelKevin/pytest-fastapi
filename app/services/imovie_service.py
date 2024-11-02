from abc import ABCMeta, abstractmethod
from datetime import date
from typing import List

from models import Movie
from schemas import MovieSchema, UpdateMovieSchema


class IMovieService(metaclass=ABCMeta):
    @abstractmethod
    def get_movies(self) -> List[Movie]:
        raise NotImplementedError

    @abstractmethod
    def get_movie(self, id: int) -> Movie:
        raise NotImplementedError

    @abstractmethod
    def get_movie_by_title_and_release_date(self, title: str, release_date: date) -> Movie:
        raise NotImplementedError

    @abstractmethod
    def create_movie(self, movie: MovieSchema) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_movie(self, movie_from_db: Movie, movie: UpdateMovieSchema) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_movie(self, movie_from_db: Movie) -> bool:
        raise NotImplementedError
