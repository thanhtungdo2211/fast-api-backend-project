from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from sqlalchemy import create_engine

from configure import config
from api.router import api_router
from configure import config
from database import Base

engine = create_engine(config.URL_DATABASE)
Base.metadata.create_all(bind=engine)

app = FastAPI(
        title="Fast API backend project",
        version=config.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        default_response_class=UJSONResponse,
    )

app.include_router(router=api_router)