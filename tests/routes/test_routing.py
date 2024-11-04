import json
from datetime import date

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from main import router
from pytest_mock import MockerFixture
from schemas import MovieSchema


class TestRouting:
    paths = {value: index for index, value in enumerate(['check_status', 'get_movies', 'get_movie',
                                                         'create_movie', 'update_movie', 'delete_movie'])}

    def set_config(self, mocker: MockerFixture) -> None:
        self.movie = MovieSchema(id=1, title='hulk', description='hulk',
                                 genre='action', rating=5, release_date=date.today())
        self.movie.release_date = str(self.movie.release_date)
        self.movies = [self.movie.model_dump() for _ in range(3)]

        self.mock_controller = mocker.MagicMock()

        mocker.patch('container.AppContainer.scope', return_value=mocker.MagicMock(
            __enter__=lambda _: mocker.MagicMock(
                controllers=mocker.MagicMock(movie_controller=lambda: self.mock_controller))
        ))

    def test_check_status(self) -> None:
        response = router.routes[self.paths['check_status']].endpoint()

        assert response == {'status': 'ok'}

    def test_get_movies(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        self.mock_controller.get_movies.return_value = mocker.Mock(
            content=jsonable_encoder(self.movies), status_code=200)

        response = router.routes[self.paths['get_movies']].endpoint()

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        assert json.loads(response.body) == self.movies

    def test_get_movie(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        self.mock_controller.get_movie.return_value = mocker.Mock(
            content=jsonable_encoder(self.movie), status_code=200)

        response = router.routes[self.paths['get_movie']].endpoint(id=1)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        assert json.loads(response.body) == self.movie.model_dump()

    def test_crete_movie(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        self.mock_controller.create_movie.return_value = mocker.Mock(
            content={'message': 'movie hulk created with success'}, status_code=201)

        response = router.routes[self.paths['create_movie']].endpoint(
            movie=None)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 201
        assert json.loads(response.body) == {
            'message': 'movie hulk created with success'}

    def test_update_movie(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        self.mock_controller.update_movie.return_value = mocker.Mock(
            content={'message': 'movie hulk updated with success'}, status_code=200)

        response = router.routes[self.paths['update_movie']].endpoint(id=1,
                                                                      movie=None)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        assert json.loads(response.body) == {
            'message': 'movie hulk updated with success'}

    def test_delete_movie(self, mocker: MockerFixture) -> None:
        self.set_config(mocker)

        self.mock_controller.delete_movie.return_value = mocker.Mock(
            content={'message': 'movie hulk deleted with success'}, status_code=200)

        response = router.routes[self.paths['delete_movie']].endpoint(id=1)

        assert isinstance(response, JSONResponse)
        assert response.status_code == 200
        assert json.loads(response.body) == {
            'message': 'movie hulk deleted with success'}
