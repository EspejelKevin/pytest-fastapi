from datetime import date
from typing import List

from controllers import MovieController
from pytest_mock import MockerFixture
from schemas import MovieSchema, Response
from services import MovieService
from utils import Utils


class TestMovieController:
    def set_config(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.movie = mock_movie_data
        self.movies = [self.movie for _ in range(5)]

        self.movie_service = mocker.Mock(MovieService)
        self.movie_service.get_movies.return_value = self.movies

        self.movie_controller = MovieController(self.movie_service)
        self.movie_controller.transaction_id = 'transaction_id_mock'

    def test_get_movies(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        def mock_mapping(movies) -> List[MovieSchema]:
            mock_data = {'id': 1, 'title': 'hulk', 'description': 'hulk',
                         'rating': 5, 'genre': 'action', 'release_date': date.today()}

            return [MovieSchema(**mock_data) for _ in range(2)]

        mocker.patch.object(Utils, 'mapping', mock_mapping)

        response = self.movie_controller.get_movies()

        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.meta.transaction_id == 'transaction_id_mock'
        assert isinstance(response.base_response.response, List)
        assert isinstance(response.base_response.response[0], dict)
        assert len(response.base_response.response) == 2
        assert response.base_response.response[0]['title'] == 'hulk'

    def test_get_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_service.get_movie.return_value = None

        self.movie_controller = MovieController(self.movie_service)
        self.movie_controller.transaction_id = 'get_movie_id'

        response = self.movie_controller.get_movie(1)

        assert isinstance(response, Response)
        assert response.status_code == 404
        assert response.base_response.response == {
            'message': 'movie not found. Try again'}

        self.movie_service.get_movie.return_value = self.movie

        self.movie_controller = MovieController(self.movie_service)
        self.movie_controller.transaction_id = 'movie_exists'

        def mock_mapping(movie) -> List[MovieSchema]:
            mock_data = {'id': 3, 'title': 'super girl', 'description': 'super girl',
                         'rating': 5, 'genre': 'action', 'release_date': date.today()}

            return MovieSchema(**mock_data)

        mocker.patch.object(Utils, 'mapping', mock_mapping)

        response = self.movie_controller.get_movie(1)

        assert isinstance(response, Response)
        assert response.status_code == 200
        assert isinstance(response.base_response.response, MovieSchema)
        assert response.base_response.response.id == 3
        assert response.base_response.response.title == 'super girl'
        assert isinstance(response.content, dict)

    def test_create_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_service.get_movie_by_title_and_release_date.return_value = True

        self.movie_controller = MovieController(self.movie_service)

        self.create_movie = mocker.Mock(MovieSchema)
        self.create_movie.title = 'spider man'
        self.create_movie.release_date = mocker.Mock(date)
        response = self.movie_controller.create_movie(self.create_movie)

        assert isinstance(response, Response)
        assert response.status_code == 409
        assert response.base_response.response == {
            'message': 'movie already exists'}

        self.movie_service.get_movie_by_title_and_release_date.return_value = False
        self.movie_service.create_movie.return_value = False

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.create_movie(self.create_movie)

        assert isinstance(response, Response)
        assert response.status_code == 500
        assert response.base_response.response == {
            'message': 'An error ocurred while executing this operation'}

        self.movie_service.create_movie.return_value = True

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.create_movie(self.create_movie)

        assert isinstance(response, Response)
        assert response.status_code == 201
        assert response.base_response.response == {
            'message': 'movie spider man created with success'}

    def test_update_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_service.get_movie.return_value = None

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.update_movie(1, None)

        assert isinstance(response, Response)
        assert response.status_code == 404
        assert response.content['response'] == {
            'message': 'movie not found. Try again'}

        self.movie.title = 'superman'

        self.movie_service.get_movie.return_value = self.movie
        self.movie_service.update_movie.return_value = False

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.update_movie(1, None)

        assert isinstance(response, Response)
        assert response.status_code == 500
        assert response.base_response.response == {
            'message': 'An error ocurred while executing this operation'}

        self.movie_service.update_movie.return_value = True

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.update_movie(1, None)

        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.content['response'] == {
            'message': 'movie superman updated with success'}

    def test_delete_movie(self, mocker: MockerFixture, mock_movie_data) -> None:
        self.set_config(mocker, mock_movie_data)

        self.movie_service.get_movie.return_value = None

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.delete_movie(None)

        assert isinstance(response, Response)
        assert response.status_code == 404
        assert response.content['response'] == {
            'message': 'movie not found. Try again'}

        self.movie.title = 'superman'

        self.movie_service.get_movie.return_value = self.movie
        self.movie_service.delete_movie.return_value = False

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.delete_movie(None)

        assert isinstance(response, Response)
        assert response.status_code == 500
        assert response.base_response.response == {
            'message': 'An error ocurred while executing this operation'}

        self.movie_service.delete_movie.return_value = True

        self.movie_controller = MovieController(self.movie_service)

        response = self.movie_controller.delete_movie(None)

        assert isinstance(response, Response)
        assert response.status_code == 200
        assert response.content['response'] == {
            'message': 'movie superman deleted with success'}
