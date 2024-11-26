import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
def read_root() -> Any:
    return {"message": "Hello World "}