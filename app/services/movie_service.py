from datetime import date
from typing import List

from models import Movie
from schemas import MovieSchema, UpdateMovieSchema

from .imovie_service import IMovieService


class MovieService(IMovieService):
    def __init__(self, movie_repository: IMovieService) -> None:
        self.movie_repository = movie_repository

    def get_movies(self) -> List[Movie]:
        return self.movie_repository.get_movies()

    def get_movie(self, id: int) -> Movie:
        return self.movie_repository.get_movie(id)

    def get_movie_by_title_and_release_date(self, title: str, release_date: date) -> Movie:
        return self.movie_repository.get_movie_by_title_and_release_date(title, release_date)

    def create_movie(self, movie: MovieSchema) -> bool:
        return self.movie_repository.create_movie(movie)

    def update_movie(self, movie_from_db: Movie, movie: UpdateMovieSchema) -> bool:
        return self.movie_repository.update_movie(movie_from_db, movie)

    def delete_movie(self, movie_from_db: Movie) -> bool:
        return self.movie_repository.delete_movie(movie_from_db)
