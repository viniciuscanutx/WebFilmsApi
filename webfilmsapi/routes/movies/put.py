from fastapi import APIRouter, Depends, HTTPException

from bson import ObjectId

from webfilmsapi.models.model import Movies, SuccessMessageID

from ...helpers.verifypassword import verify_password
from ...config.db import db


mput_router = APIRouter(prefix='/movies', tags=['Movies / Put'])


@mput_router.put("/{movie_id}", summary="Atualizar Filme", response_model=SuccessMessageID)
async def update_film(movie_id: str, film: Movies, password: str = Depends(verify_password)):
    result = db.movies.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": film.model_dump()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    return {'message': 'Filme atualizado com sucesso!', 'imdbid': film.imdbid}