from datetime import date
from typing import List

from models import Movie
from schemas import MovieSchema, UpdateMovieSchema
from services import IMovieService
from sqlmodel import Session, select


class MovieRepository(IMovieService):
    def __init__(self, db_factory: Session) -> None:
        self.db_factory = db_factory

    def get_movies(self) -> List[Movie]:
        with self.db_factory() as db:
            session: Session = db.get_session()
            statement = select(Movie)
            return session.exec(statement).all()

    def get_movie(self, id) -> Movie:
        with self.db_factory() as db:
            session: Session = db.get_session()
            statement = select(Movie).where(Movie.id == id)
            return session.exec(statement).one_or_none()

    def get_movie_by_title_and_release_date(self, title: str, release_date: date):
        with self.db_factory() as db:
            session: Session = db.get_session()
            statement = select(Movie).where(Movie.title == title).where(
                Movie.release_date == release_date)
            return session.exec(statement).one_or_none()

    def create_movie(self, movie: MovieSchema) -> bool:
        with self.db_factory() as db:
            session: Session = db.get_session()
            session.add(Movie(**movie.model_dump()))
            session.commit()
            return True

    def update_movie(self, movie_from_db: Movie, movie: UpdateMovieSchema) -> bool:
        with self.db_factory() as db:
            movie = movie.model_dump()
            session: Session = db.get_session()

            movie_from_db.title = movie.get('title', movie_from_db.title)
            movie_from_db.description = movie.get(
                'description', movie_from_db.description)
            movie_from_db.genre = movie.get('genre', movie_from_db.genre)
            movie_from_db.rating = movie.get('rating', movie_from_db.rating)
            movie_from_db.release_date = movie.get(
                'release_date', movie_from_db.release_date)
            movie_from_db.language = movie.get(
                'language', movie_from_db.language)
            movie_from_db.duration = movie.get(
                'duration', movie_from_db.duration)

            session.add(movie_from_db)
            session.commit()

            return True

    def delete_movie(self, movie_from_db: Movie) -> bool:
        with self.db_factory() as db:
            session: Session = db.get_session()
            session.delete(movie_from_db)
            session.commit()
            return True
