from fastapi import APIRouter, Depends, HTTPException

from webfilmsapi.models.model import Movies, SuccessMessageID

from ...helpers.verifypassword import verify_password
from ...config.db import db


mp_router = APIRouter(prefix='/movies', tags=['Movies / Post'])


@mp_router.post("/add", summary="Adicionar Filme", response_model=SuccessMessageID)
async def add_film(film: Movies, password: str = Depends(verify_password)):
    film_dict = film.model_dump()
    result = db.movies.insert_one(film_dict)

    if not result.inserted_id:
        raise HTTPException(status_code=400, detail="Erro ao adicionar filme")

    return {'message': 'Filme adicionado com sucesso!', 'imdbid': film.imdbid}