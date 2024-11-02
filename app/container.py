from contextlib import contextmanager
from typing import Optional

from controllers import MovieController
from db import SQLiteDatabase
from dependency_injector import containers, providers
from repositories import MovieRepository
from services import MovieService
from sqlalchemy import Engine


class DatabasesContainer(containers.DeclarativeContainer):
    sqlite = providers.Singleton(
        SQLiteDatabase, uri='sqlite:///database.db')


class RepositoriesContainer(containers.DeclarativeContainer):
    databases: DatabasesContainer = providers.DependenciesContainer()
    movie_repository = providers.Singleton(
        MovieRepository, db_factory=databases.sqlite.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    movie_service = providers.Factory(
        MovieService, movie_repository=repositories.movie_repository)


class ControllersContainer(containers.DeclarativeContainer):
    services: ServicesContainer = providers.DependenciesContainer()
    movie_controller = providers.Factory(
        MovieController, movie_service=services.movie_service)


class BaseContainer(containers.DeclarativeContainer):
    databases = providers.Container(DatabasesContainer)
    repositories = providers.Container(
        RepositoriesContainer, databases=databases)
    services = providers.Container(
        ServicesContainer, repositories=repositories)
    controllers = providers.Container(
        ControllersContainer, services=services)


class AppContainer:
    container: Optional[BaseContainer] = None

    @classmethod
    @contextmanager
    def scope(cls):
        try:
            cls.container.services.init_resources()
            yield cls.container
        finally:
            cls.container.services.shutdown_resources()

    @classmethod
    def init(cls) -> None:
        if cls.container is None:
            cls.container = BaseContainer()

    @classmethod
    def db_engine(cls) -> Engine:
        return cls.container.databases.sqlite().engine()
