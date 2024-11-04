from datetime import date

import pytest
from pytest_mock import MockerFixture
from repositories import MovieRepository
from services import MovieService


class TestMovieService:
    def set_config(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.movie = mock_movie_data
        self.movies = [self.movie for _ in range(5)]

        self.movie_repository = mocker.Mock(MovieRepository)
        self.movie_repository.get_movies.return_value = self.movies
        self.movie_repository.get_movie.return_value = self.movie
        self.movie_repository.create_movie.return_value = True
        self.movie_repository.update_movie.return_value = True
        self.movie_repository.delete_movie.return_value = True

        self.movie_service = MovieService(self.movie_repository)

    def test_get_movies_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        for movie in self.movie_service.get_movies():
            assert movie.id == 1
            assert movie.title == 'mock movie title'
            assert movie.genre == 'action'
            assert movie.rating == 5
            assert movie.release_date != date.today()

    def test_get_movie_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        movie = self.movie_service.get_movie(1)

        assert movie.id == 1
        assert movie.title == 'mock movie title'
        assert movie.genre == 'action'
        assert movie.rating == 5
        assert movie.release_date != date.today()

    def test_get_movie_by_title_and_release_date_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie.id = 2
        self.movie.title = 'SpiderMan'
        self.movie.rating = 3
        self.movie.genre = 'Romantic'

        self.movie_repository.get_movie_by_title_and_release_date.return_value = self.movie

        self.movie_service = MovieService(self.movie_repository)

        movie = self.movie_service.get_movie_by_title_and_release_date(
            '', None)

        assert movie.id == 2
        assert movie.title == 'SpiderMan'
        assert movie.genre == 'Romantic'
        assert movie.rating == 3
        assert movie.release_date != date.today()

    def test_create_movie_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        success = self.movie_service.create_movie(None)
        assert success

    def test_update_movie_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        success = self.movie_service.update_movie(None, None)
        assert success

    def test_delete_movie_service(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        success = self.movie_service.delete_movie(None)
        assert success

    def test_create_movie_service_failed(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_repository.create_movie.side_effect = Exception(
            'Error while creating movie')

        self.movie_service = MovieService(self.movie_repository)

        with pytest.raises(Exception) as excinfo:
            self.movie_service.create_movie(None)

        assert excinfo.value.args[0] == 'Error while creating movie'

    def test_update_movie_service_failed(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_repository.update_movie.side_effect = Exception(
            'Error while updating movie')

        self.movie_service = MovieService(self.movie_repository)

        with pytest.raises(Exception) as excinfo:
            self.movie_service.update_movie(None, None)

        assert excinfo.value.args[0] == 'Error while updating movie'

    def test_delete_movie_service_failed(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_repository.delete_movie.side_effect = Exception(
            'Error while deleting movie')

        self.movie_service = MovieService(self.movie_repository)

        with pytest.raises(Exception) as excinfo:
            self.movie_service.delete_movie(None)

        assert excinfo.value.args[0] == 'Error while deleting movie'
