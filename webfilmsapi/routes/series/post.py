from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.schema import serializeSeries
from ...helpers.verifypassword import verify_password
from ...config.db import db
from ...models.model import (
    Episode,
    Series,
    SuccessMessageID,
)


spost_router = APIRouter(prefix='/series', tags=['Series / Post'])


@spost_router.post("/add", summary="Adicionar Serie", response_model=SuccessMessageID)
async def add_series(series: Series, password: str = Depends(verify_password)):
    series_data = series.model_dump()

    if isinstance(series_data["nseasons"], int):
        series_data["nseasons"] = [
            {
                "seasonnumber": i + 1,
                "episodes": []
            } for i in range(series_data["nseasons"])
        ]

    result = db.series.insert_one(series_data)
    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Erro ao adicionar série")

    return {'message': 'Série adicionada com sucesso!', 'imdbid': series.imdbid}


@spost_router.post("/{series_id}/seasons/{season_number}/episodes", summary="Adicionar um Episódio", response_model=Episode)
async def add_episode(series_id: str, season_number: int, episode: Episode, password: str = Depends(verify_password)):
    try:
        series = db.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        if isinstance(series["nseasons"], int):
            series["nseasons"] = [{"seasonnumber": i + 1, "episodes": []} for i in range(series["nseasons"])]
            db.series.update_one({"_id": ObjectId(series_id)}, {"$set": {"nseasons": series["nseasons"]}})

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            season = {"seasonnumber": season_number, "episodes": []}
            series["nseasons"].append(season)
            db.series.update_one({"_id": ObjectId(series_id)}, {"$push": {"nseasons": season}})

        episode_data = episode.model_dump()

        result = db.series.update_one(
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

        updated_series = db.series.find_one({"_id": ObjectId(series_id)})
        return serializeSeries(updated_series)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))