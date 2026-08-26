from http import HTTPStatus

from fastapi import FastAPI

from simple_todo.routes import auth, todo, users
from simple_todo.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(todo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}
