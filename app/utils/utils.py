from typing import Dict, List

from models import Movie
from schemas import MovieSchema


def mapping(movies: List[Movie] | Movie) -> List[MovieSchema] | MovieSchema:
    if isinstance(movies, list):
        return [MovieSchema(**movie.model_dump()) for movie in movies]
    return MovieSchema(**movies.model_dump())
