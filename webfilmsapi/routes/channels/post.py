from fastapi import APIRouter, Depends, HTTPException

from ...helpers.verifypassword import verify_password
from ...config.db import db
from ...models.model import Channels


cp_router = APIRouter(prefix='/channels', tags=['Channels / Post'])


@cp_router.post("/add", summary="Adicionar Canal", response_model=Channels)
def add_channel(channel: Channels, password: str = Depends(verify_password)):
    result = db.channels.insert_one(channel.model_dump())

    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Erro ao adicionar canal")

    return {"title": str(result.inserted_id)}