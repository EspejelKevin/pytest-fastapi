import container
from controllers import MovieController
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from schemas import MovieSchemaIn, UpdateMovieSchema

router = APIRouter(prefix='/api/v1')


@router.get('/check/status', tags=['Health Check'])
def check_status() -> dict:
    return {'status': 'ok'}


@router.get('/movies', tags=['Movies'])
def get_movies() -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.get_movies()
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.get_movie(id)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.post('/movies', tags=['Movies'])
def create_movie(movie: MovieSchemaIn) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.create_movie(movie)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.put('/movie/{id}', tags=['Movies'])
def update_movie(id: int, movie: UpdateMovieSchema) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.update_movie(id, movie)
        return JSONResponse(content=response.content, status_code=response.status_code)


@router.delete('/movie/{id}', tags=['Movies'])
def delete_movie(id: int) -> JSONResponse:
    with container.AppContainer.scope() as app:
        movie_controller: MovieController = app.controllers.movie_controller()
        response = movie_controller.delete_movie(id)
        return JSONResponse(content=response.content, status_code=response.status_code)
