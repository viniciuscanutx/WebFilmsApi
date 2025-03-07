from typing import List

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from ...schemas.schema import serializeChannel
from ...config.db import db
from ...models.model import ChannelsDto


cg_router = APIRouter(prefix='/channels', tags=['Channels / Get'])


@cg_router.get("/found", summary="Exibir Todos os Canais", response_model=List[ChannelsDto])
def list_channels():
    channels = db.channels.find()

    if not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]

@cg_router.get("/search/title", summary="Buscar Canais por Título", response_model=List[ChannelsDto])
async def search_channels_by_title(title: str = Query(..., description="Título do canal")):
    query = {"title": {"$regex": title, "$options": "i"}}

    channels = db.channels.find(query)

    if not channels:
        raise HTTPException(status_code=404, detail="Titulo do canal não encontrado")
    elif not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]


@cg_router.get("/search/genre", summary="Buscar Canais por Categoria", response_model=List[ChannelsDto])
async def search_channels_by_genre(genre: str = Query(..., description="Categoria do canal")):
    query = {"genre": {"$regex": genre, "$options": "i"}}

    channels = db.channels.find(query)

    if not channels:
        raise HTTPException(status_code=404, detail="Genero do canal não encontrado")
    elif not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]


@cg_router.get("/{channel_id}", summary="Buscar Canal pelo ID", response_model=ChannelsDto)
async def get_channel_by_id(channel_id: str):
    try:
        channel = db.channels.find_one({"_id": ObjectId(channel_id)})

        if not channel:
            raise HTTPException(status_code=404, detail="Canal não encontrado")

        return serializeChannel(channel)

    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")