from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from ...config.db import db
from ...helpers.verifypassword import verify_password


md_router = APIRouter(prefix='/movies', tags=['Movies / Delete'])
        
        
@md_router.delete("/{movie_id}", summary="Deletar Filme")
async def delete_film(movie_id: str, password: str = Depends(verify_password)):
    result = db.movies.delete_one({"_id": ObjectId(movie_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    return {"message": "Filme removido com sucesso"}