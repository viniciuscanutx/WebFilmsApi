from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from ...schemas.schema import serializeSeries
from ...helpers.verifypassword import verify_password
from ...config.db import db
from ...models.model import (
    Episode,
    Series,
)


sput_router = APIRouter(prefix='/series', tags=['Series / Put'])


@sput_router.put("/{series_id}", summary="Atualizar Série", response_model=Series)
async def update_series(series_id: str, series: Series, password: str = Depends(verify_password)):
    result = db.series.update_one(
        {"_id": ObjectId(series_id)},
        {"$set": series.model_dump()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Série não encontrada")

    updated_series = db.series.find_one({"_id": ObjectId(series_id)})

    return serializeSeries(updated_series)


@sput_router.put("/{series_id}/seasons/{season_number}/episodes/{episode_number}", summary="Atualizar um Episódio", response_model=Episode)
async def update_episode(series_id: str, season_number: int, episode_number: str, episode: Episode, password: str = Depends(verify_password)):
    try:
        series = db.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        episode_index = next((index for (index, ep) in enumerate(season["episodes"]) if ep["epnumber"] == episode_number), None)
        if episode_index is None:
            raise HTTPException(status_code=404, detail="Episódio não encontrado")

        episode_data = episode.model_dump()
        result = db.series.update_one(
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

        updated_series = db.series.find_one({"_id": ObjectId(series_id)})
        return serializeSeries(updated_series)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
