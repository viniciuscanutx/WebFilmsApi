
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from ...helpers.verifypassword import verify_password
from ...config.db import db
from ...models.model import ChannelsDto


cd_router = APIRouter(prefix='/channels', tags=['Channels / Delete'])


@cd_router.delete("/{channel_id}", summary="Deletar Canal")
async def delete_channel(channel_id: str, password: str = Depends(verify_password)):
    result = db.channels.delete_one({"_id": ObjectId(channel_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Canal não encontrado")

    return {"message": "Canal removido com sucesso"}