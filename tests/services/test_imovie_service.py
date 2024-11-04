import pytest
from pytest_mock import MockerFixture
from services import IMovieService


class TestIMovieService:
    def set_config(self, mocker: MockerFixture) -> None:
        mocker.patch.multiple(IMovieService, __abstractmethods__=set())
        self.imovie_service_mock = IMovieService()
        self.movie_mock = mocker.Mock()
        self.date_mock = mocker.Mock()

    def test_not_implemented_methods(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.get_movies()

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.get_movie(1)

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.get_movie_by_title_and_release_date(
                '', self.date_mock)

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.create_movie(self.movie_mock)

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.update_movie(
                self.movie_mock, self.movie_mock)

        with pytest.raises(NotImplementedError):
            self.imovie_service_mock.delete_movie(self.movie_mock)
