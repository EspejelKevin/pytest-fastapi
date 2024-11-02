import uvicorn
from container import AppContainer
from fastapi import FastAPI
from models import Movie
from routes import router
from sqlmodel import SQLModel


def on_startup():
    AppContainer.init()
    SQLModel.metadata.create_all(AppContainer.db_engine())


app = FastAPI(
    on_startup=[on_startup]
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app)
