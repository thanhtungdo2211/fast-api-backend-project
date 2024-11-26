from fastapi import FastAPI
from api.routes import test

app = FastAPI()

app.include_router(test.router, tags=["test"])