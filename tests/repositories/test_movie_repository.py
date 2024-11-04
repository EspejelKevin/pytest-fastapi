from db import SQLiteDatabase
from models import Movie
from pytest_mock import MockerFixture
from repositories import MovieRepository
from schemas import UpdateMovieSchema


class TestMovieRepository:
    def set_config(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.movie = mock_movie_data
        self.movies = [self.movie for _ in range(5)]
        self.db_factory = mocker.MagicMock(SQLiteDatabase)

    def test_get_movies(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.exec.\
            return_value.all.\
            return_value = self.movies

        movie_repository = MovieRepository(self.db_factory)
        movies = movie_repository.get_movies()

        for movie in movies:
            assert movie.id == 1
            assert movie.title == 'mock movie title'
            assert movie.description == 'mock movie description'
            assert movie.genre == 'action'
            assert movie.rating == 5

    def test_get_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie.id = 5
        self.movie.title = 'spider man'
        self.movie.rating = 2
        self.movie.genre = 'dramatic'

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.exec.\
            return_value.one_or_none.\
            return_value = self.movie

        movie_repository = MovieRepository(self.db_factory)
        movie = movie_repository.get_movie(None)

        assert movie.id == 5
        assert movie.title == 'spider man'
        assert movie.description == 'mock movie description'
        assert movie.genre == 'dramatic'
        assert movie.rating == 2

    def test_get_movie_by_title_and_release_date(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie.id = 10
        self.movie.title = 'hulk'
        self.movie.rating = 2
        self.movie.genre = 'horror'

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.exec.\
            return_value.one_or_none.\
            return_value = self.movie

        movie_repository = MovieRepository(self.db_factory)
        movie = movie_repository.get_movie_by_title_and_release_date(
            None, None)

        assert movie.id == 10
        assert movie.title == 'hulk'
        assert movie.description == 'mock movie description'
        assert movie.genre == 'horror'
        assert movie.rating == 2

    def test_create_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie = mocker.MagicMock(Movie)

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.add.\
            return_value.commit.\
            return_value = True

        movie_repository = MovieRepository(self.db_factory)
        success = movie_repository.create_movie(self.movie)

        assert success

    def test_update_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie = mocker.MagicMock(Movie)
        self.update_movie = mocker.MagicMock(UpdateMovieSchema)

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.add.\
            return_value.commit.\
            return_value = True

        movie_repository = MovieRepository(self.db_factory)
        success = movie_repository.update_movie(self.movie, self.update_movie)

        assert success

    def test_delete_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie = mocker.MagicMock(Movie)

        self.db_factory.return_value.__enter__.\
            return_value.get_session.\
            return_value.delete.\
            return_value.commit.\
            return_value = True

        movie_repository = MovieRepository(self.db_factory)
        success = movie_repository.delete_movie(self.movie)

        assert success
