import uuid

from fastapi import status
from schemas import MovieSchema, Response, UpdateMovieSchema
from services import IMovieService
from utils import Utils


class MovieController:
    def __init__(self, movie_service: IMovieService):
        self.movie_service = movie_service
        self.transaction_id = str(uuid.uuid4())
        self.message_not_found = {'message': 'movie not found. Try again'}
        self.message_internal_error = {
            'message': 'An error ocurred while executing this operation'}
        self.message_already_exists = {'message': 'movie already exists'}

    def get_movies(self) -> Response:
        movies = self.movie_service.get_movies()
        movies_mapped = Utils.mapping(movies)
        movies_mapped = list(map(lambda movie: dict(
            sorted(movie.model_dump().items())), movies_mapped))
        return Response(movies_mapped, self.transaction_id)

    def get_movie(self, id: int) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response(self.message_not_found, self.transaction_id, status.HTTP_404_NOT_FOUND)

        movie_mapped = Utils.mapping(movie)
        return Response(movie_mapped, self.transaction_id)

    def create_movie(self, movie: MovieSchema) -> Response:
        existing_movie = self.movie_service.get_movie_by_title_and_release_date(
            movie.title, movie.release_date)

        if existing_movie:
            return Response(self.message_already_exists, self.transaction_id, status.HTTP_409_CONFLICT)

        success = self.movie_service.create_movie(movie)

        if not success:
            return Response(self.message_internal_error,
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} created with success'}, self.transaction_id, status.HTTP_201_CREATED)

    def update_movie(self, id: int, update_movie: UpdateMovieSchema) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response(self.message_not_found, self.transaction_id, status.HTTP_404_NOT_FOUND)

        success = self.movie_service.update_movie(movie, update_movie)

        if not success:
            return Response(self.message_internal_error,
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} updated with success'}, self.transaction_id)

    def delete_movie(self, id: int) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response(self.message_not_found, self.transaction_id, status.HTTP_404_NOT_FOUND)

        success = self.movie_service.delete_movie(movie)

        if not success:
            return Response(self.message_internal_error,
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} deleted with success'}, self.transaction_id)
