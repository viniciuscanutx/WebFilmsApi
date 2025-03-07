from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from ...helpers.verifypassword import verify_password
from ...config.db import db


sdel_router = APIRouter(prefix='/series', tags=['Series / Delete'])



@sdel_router.delete("/{series_id}", summary="Deletar Série")
async def delete_series(series_id: str, password: str = Depends(verify_password)):
    result = db.series.delete_one({"_id": ObjectId(series_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Série não encontrada")

    return {"message": "Série deletada com sucesso"}


@sdel_router.delete("/{series_id}/seasons/{season_number}/episodes/{episode_number}", summary="Deletar Episódio")
async def delete_episode(series_id: str, season_number: int, episode_number: str, password: str = Depends(verify_password)):
    try:
        series = db.series.find_one({"_id": ObjectId(series_id)})
        if not series:
            raise HTTPException(status_code=404, detail="Série não encontrada")

        season = next((s for s in series["nseasons"] if s["seasonnumber"] == season_number), None)
        if not season:
            raise HTTPException(status_code=404, detail="Temporada não encontrada")

        episode = next((ep for ep in season["episodes"] if ep["epnumber"] == episode_number), None)
        if not episode:
            raise HTTPException(status_code=404, detail="Episódio não encontrado")

        result = db.series.update_one(
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