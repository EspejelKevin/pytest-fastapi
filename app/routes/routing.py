import container
from controllers import MovieController
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from schemas import MovieSchemaIn, UpdateMovieSchema

router = APIRouter(prefix='/api/v1')


@router.get('/check/status')
def check_status() -> dict:
    return {'status': 'ok'}


@router.get('/movies')
def get_movies() -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.get_movies()
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.get('/movies/{id}')
def get_movie(id: int) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.get_movie(id)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.post('/movies')
def create_movie(movie: MovieSchemaIn) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.create_movie(movie)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.put('/movie/{id}')
def update_movie(id: int, movie: UpdateMovieSchema) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.update_movie(id, movie)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.delete('/movie/{id}')
def delete_movie(id: int) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.delete_movie(id)
        return JSONResponse(content=response.content, status_code=response.status_code)
