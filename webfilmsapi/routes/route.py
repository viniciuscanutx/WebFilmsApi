from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query

from ..helpers.verifypassword import verify_password
from ..config.db import db, dbc, dbs
from ..models.model import (
    Channels,
    ChannelsDto,
    Episode,
    Series,
    SeriesDto,
    SuccessMessageID,
    SuccessMessageTitle,
)
from ..schemas.schema import (
    serializeChannel,
    serializeSeries,
    serializeSeriesDto,
)

user = APIRouter()


@user.get("/", include_in_schema=False)
def welcome():
    movies_count = db.movies.count_documents({})
    series_count = dbs.series.count_documents({})
    channels_count = dbc.channels.count_documents({})

    return {
        "message": "WebFilmsAPI",
        "total_movies": movies_count,
        "total_series": series_count,
        "total_channels": channels_count
    }


@user.get("/series/found", tags=["Series"], summary="Exibir Todas As Series", response_model=List[SeriesDto])
async def list_series():
    series = dbs.series.find()

    if not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@user.get("/series/search/title", tags=["Series"], summary="Buscar Séries por Título", response_model=List[SeriesDto])
async def search_series_by_title(title: str = Query(..., description="Título da série")):
    query = {"title": {"$regex": title, "$options": "i"}}

    series = list(dbs.series.find(query))

    if not series:
        raise HTTPException(status_code=404, detail="Nenhuma serie encontrada com o titulo fornecido.")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@user.get("/series/search/genre", tags=["Series"], summary="Buscar Séries por Gênero", response_model=List[SeriesDto])
async def search_series_by_genre(genre: str = Query(..., description="Gênero da série")):
    query = {"genre": {"$regex": genre, "$options": "i"}}

    series = list(dbs.series.find(query))

    if not series:
        raise HTTPException(status_code=404, detail="Nenhuma serie encontrada com o gênero fornecido.")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@user.get("/series/imdb/{imdbid}", tags=["Series"], summary="Buscar Série pelo ID do IMDb", response_model=SeriesDto)
async def get_series_by_imdbid(imdbid: str):
    series = dbs.series.find_one({"imdbid": imdbid})

    if not series:
        raise HTTPException(status_code=404, detail="Série não encontrada")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return serializeSeriesDto(series)


@user.post("/series/add", tags=["Series"], summary="Adicionar Serie", response_model=SuccessMessageID)
async def add_series(series: Series, password: str = Depends(verify_password)):
    series_data = series.model_dump()

    if isinstance(series_data["nseasons"], int):
        series_data["nseasons"] = [
            {
                "seasonnumber": i + 1,
                "episodes": []
            } for i in range(series_data["nseasons"])
        ]

    result = dbs.series.insert_one(series_data)
    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Erro ao adicionar série")

    return {'message': 'Série adicionada com sucesso!', 'imdbid': series.imdbid}


@user.put("/series/{series_id}", tags=["Series"], summary="Atualizar Série", response_model=Series)
async def update_series(series_id: str, series: Series, password: str = Depends(verify_password)):
    result = dbs.series.update_one(
        {"_id": ObjectId(series_id)},
        {"$set": series.model_dump()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Série não encontrada")

    updated_series = dbs.series.find_one({"_id": ObjectId(series_id)})

    return serializeSeries(updated_series)


@user.delete("/series/{series_id}", tags=["Series"], summary="Deletar Série")
async def delete_series(series_id: str, password: str = Depends(verify_password)):
    result = dbs.series.delete_one({"_id": ObjectId(series_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Série não encontrada")

    return {"message": "Série removida com sucesso"}


@user.post("/series/{series_id}/seasons/{season_number}/episodes", tags=["Episodes"], summary="Adicionar um Episódio", response_model=Episode)
async def add_episode(series_id: str, season_number: int, episode: Episode, password: str = Depends(verify_password)):
    try:
        series = dbs.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        if isinstance(series["nseasons"], int):
            series["nseasons"] = [{"seasonnumber": i + 1, "episodes": []} for i in range(series["nseasons"])]
            dbs.series.update_one({"_id": ObjectId(series_id)}, {"$set": {"nseasons": series["nseasons"]}})

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            season = {"seasonnumber": season_number, "episodes": []}
            series["nseasons"].append(season)
            dbs.series.update_one({"_id": ObjectId(series_id)}, {"$push": {"nseasons": season}})

        episode_data = episode.model_dump()

        result = dbs.series.update_one(
            {
                "_id": ObjectId(series_id),
                "nseasons.seasonnumber": season_number
            },
            {
                "$push": {
                    "nseasons.$.episodes": episode_data
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Falha ao adicionar episódio")

        updated_series = dbs.series.find_one({"_id": ObjectId(series_id)})
        return serializeSeries(updated_series)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.put("/series/{series_id}/seasons/{season_number}/episodes/{episode_number}", tags=["Episodes"], summary="Atualizar um Episódio", response_model=Episode)
async def update_episode(series_id: str, season_number: int, episode_number: str, episode: Episode, password: str = Depends(verify_password)):
    try:
        series = dbs.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        episode_index = next((index for (index, ep) in enumerate(season["episodes"]) if ep["epnumber"] == episode_number), None)
        if episode_index is None:
            raise HTTPException(status_code=404, detail="Episódio não encontrado")

        episode_data = episode.model_dump()
        result = dbs.series.update_one(
            {
                "_id": ObjectId(series_id),
                "nseasons.seasonnumber": season_number,
                "nseasons.episodes.epnumber": episode_number
            },
            {
                "$set": {
                    "nseasons.$[season].episodes.$[episode]": episode_data
                }
            },
            array_filters=[
                {"season.seasonnumber": season_number},
                {"episode.epnumber": episode_number}
            ]
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Falha ao atualizar episódio")

        updated_series = dbs.series.find_one({"_id": ObjectId(series_id)})
        return serializeSeries(updated_series)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.delete("/series/{series_id}/seasons/{season_number}/episodes/{episode_number}", tags=["Episodes"], summary="Deletar Episódio")
async def delete_episode(series_id: str, season_number: int, episode_number: str, password: str = Depends(verify_password)):
    try:
        series = dbs.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        episode = next((ep for ep in season["episodes"] if ep["epnumber"] == episode_number), None)
        if not episode:
            raise HTTPException(status_code=404, detail="Episódio não encontrado")

        result = dbs.series.update_one(
            {
                "_id": ObjectId(series_id),
                "nseasons.seasonnumber": season_number
            },
            {
                "$pull": {
                    "nseasons.$.episodes": {
                        "epnumber": episode_number
                    }
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Falha ao remover o episódio")

        return {"message": "Episódio removido com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.get("/channels/found", tags=["Channels"], summary="Exibir Todos os Canais", response_model=List[ChannelsDto])
def list_channels():
    channels = dbc.channels.find()

    if not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]


@user.get("/channels/search/title", tags=["Channels"], summary="Buscar Canais por Título", response_model=List[ChannelsDto])
async def search_channels_by_title(title: str = Query(..., description="Título do canal")):
    query = {"title": {"$regex": title, "$options": "i"}}

    channels = dbc.channels.find(query)

    if not channels:
        raise HTTPException(status_code=404, detail="Titulo do canal não encontrado")
    elif not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]


@user.get("/channels/search/genre", tags=["Channels"], summary="Buscar Canais por Categoria", response_model=List[ChannelsDto])
async def search_channels_by_genre(genre: str = Query(..., description="Categoria do canal")):
    query = {"genre": {"$regex": genre, "$options": "i"}}

    channels = dbc.channels.find(query)

    if not channels:
        raise HTTPException(status_code=404, detail="Genero do canal não encontrado")
    elif not channels:
        raise HTTPException(status_code=500, detail="Canais não encontrados")

    return [serializeChannel(channel) for channel in channels]


@user.get("/channels/{channel_id}", tags=["Channels"], summary="Buscar Canal pelo ID", response_model=ChannelsDto)
async def get_channel_by_id(channel_id: str):
    try:
        channel = dbc.channels.find_one({"_id": ObjectId(channel_id)})

        if not channel:
            raise HTTPException(status_code=404, detail="Canal não encontrado")

        return serializeChannel(channel)

    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")


@user.post("/channels/add", tags=["Channels"], summary="Adicionar Canal", response_model=Channels)
def add_channel(channel: Channels, password: str = Depends(verify_password)):
    result = dbc.channels.insert_one(channel.model_dump())

    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Erro ao adicionar canal")

    return {"title": str(result.inserted_id)}


@user.put("/channels/{channel_id}", tags=["Channels"], summary="Atualizar Canal", response_model=SuccessMessageTitle)
async def update_channel(channel_id: str, channel: Channels, password: str = Depends(verify_password)):
    try:

        if not ObjectId.is_valid(channel_id):
            raise HTTPException(status_code=400, detail="ID do canal inválido")

        result = dbc.channels.update_one(
            {"_id": ObjectId(channel_id)},
            {"$set": channel.model_dump()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Canal não encontrado")

        return {'message': 'Canal atualizado com sucesso!', 'title': channel.title}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user.delete("/channels/{channel_id}", tags=["Channels"], summary="Deletar Canal")
async def delete_channel(channel_id: str, password: str = Depends(verify_password)):
    result = dbc.channels.delete_one({"_id": ObjectId(channel_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Canal não encontrado")

    return {"message": "Canal removido com sucesso"}
