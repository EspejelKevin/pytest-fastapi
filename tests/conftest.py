import os
import sys
from datetime import date

import pytest
from pytest_mock import MockerFixture

sys.path.append(f'{os.path.dirname(__file__)}/../app')


@pytest.fixture
def mock_movie_data(mocker: MockerFixture):
    from models import Movie

    mock_movie = mocker.Mock(Movie)
    mock_movie.id = 1
    mock_movie.title = 'mock movie title'
    mock_movie.description = 'mock movie description'
    mock_movie.genre = 'action'
    mock_movie.rating = 5
    mock_movie.release_date = date(2024, 11, 13)

    return mock_movie
