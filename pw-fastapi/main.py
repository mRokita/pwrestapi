import secrets

import uvicorn
from fastapi import FastAPI, Path, Query, Depends, Body, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class User(BaseModel):
    id: int
    name: str = Field(pattern=r"[a-z]+")


USERS_DB = {
    1: User(id=1, name="a"),
    2: User(id=2, name="b"),
    3: User(id=3, name="c"),
}

auth = HTTPBasic()


def get_user(user_id: int = Path(...)) -> User:
    return USERS_DB[user_id]


def get_authenticated_user(
        credentials: HTTPBasicCredentials = Depends(auth)) -> str:
    if secrets.compare_digest(credentials.password, "1234"):
        return credentials.username
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )


@app.get("/users/{user_id}")
def retrieve_user(user: User = Depends(get_user),
                  authenticated_user: str = Depends(get_authenticated_user)
                  ) -> User:
    print(authenticated_user)
    return user


@app.patch("/users/{user_id}")
def update_user_name(user: User = Depends(get_user),
                     user_name: str = Body(...)) -> User:
    user.name = user_name
    return user


if __name__ == "__main__":
    uvicorn.run(app)
