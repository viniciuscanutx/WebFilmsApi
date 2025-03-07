
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from ...helpers.verifypassword import verify_password
from ...config.db import db
from ...models.model import Channels, SuccessMessageTitle


cput_router = APIRouter(prefix='/channels', tags=['Channels / Put'])


@cput_router.put("/{channel_id}", summary="Atualizar Canal", response_model=SuccessMessageTitle)
async def update_channel(channel_id: str, channel: Channels, password: str = Depends(verify_password)):
    try:

        if not ObjectId.is_valid(channel_id):
            raise HTTPException(status_code=400, detail="ID do canal inválido")

        result = db.channels.update_one(
            {"_id": ObjectId(channel_id)},
            {"$set": channel.model_dump()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Canal não encontrado")

        return {'message': 'Canal atualizado com sucesso!', 'title': channel.title}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))