import uuid

from fastapi import status
from schemas import MovieSchema, Response, UpdateMovieSchema
from services import IMovieService
from utils import mapping


class MovieController:
    def __init__(self, movie_service: IMovieService):
        self.movie_service = movie_service
        self.transaction_id = str(uuid.uuid4())

    def get_movies(self) -> Response:
        movies = self.movie_service.get_movies()
        movies_mapped = mapping(movies)
        movies_mapped = list(map(lambda movie: dict(
            sorted(movie.model_dump().items())), movies_mapped))
        return Response(movies_mapped, self.transaction_id)

    def get_movie(self, id: int) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response({'message': 'movie not found. Try again'}, self.transaction_id, status.HTTP_404_NOT_FOUND)

        movie_mapped = mapping(movie)
        return Response(movie_mapped, self.transaction_id)

    def create_movie(self, movie: MovieSchema) -> Response:
        existing_movie = self.movie_service.get_movie_by_title_and_release_date(
            movie.title, movie.release_date)

        if existing_movie:
            return Response({'message': 'movie already exists'}, self.transaction_id, status.HTTP_409_CONFLICT)

        success = self.movie_service.create_movie(movie)

        if not success:
            return Response({'message': 'An error ocurred while executing this operation'},
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} created with success'}, self.transaction_id, status.HTTP_201_CREATED)

    def update_movie(self, id: int, update_movie: UpdateMovieSchema) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response({'message': 'movie not found, try again'}, self.transaction_id, status.HTTP_404_NOT_FOUND)

        success = self.movie_service.update_movie(movie, update_movie)

        if not success:
            return Response({'message': 'An error ocurred while performing this operation'},
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} updated with success'}, self.transaction_id)

    def delete_movie(self, id: int) -> Response:
        movie = self.movie_service.get_movie(id)

        if not movie:
            return Response({'message': 'movie not found, try again'}, self.transaction_id, status.HTTP_404_NOT_FOUND)

        success = self.movie_service.delete_movie(movie)

        if not success:
            return Response({'message': 'An error ocurred while performing this operation'},
                            self.transaction_id, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': f'movie {movie.title} deleted with success'}, self.transaction_id)
