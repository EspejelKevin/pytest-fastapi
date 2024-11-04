import uvicorn
from container import AppContainer
from fastapi import FastAPI
from models import Movie
from routes import router
from sqlmodel import SQLModel


def on_startup():
    AppContainer.init()
    SQLModel.metadata.create_all(AppContainer.db_engine())


tags = [
    {
        'name': 'Health Check',
        'description': 'Check status of the service. Verify if the service is up'
    },
    {
        'name': 'Movies',
        'description': 'CRUD Movies'
    }
]


app = FastAPI(
    title='Movies',
    summary='CRUD Movies',
    description='Service to handler operations CRUD about Movies',
    openapi_tags=tags,
    on_startup=[on_startup],
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
