from typing import List
from fastapi import APIRouter, HTTPException, Query

from ...schemas.schema import serializeSeriesDto
from ...config.db import db
from ...models.model import SeriesDto


sg_router = APIRouter(prefix='/series', tags=['Series / Get'])


@sg_router.get("/found", summary="Exibir Todas As Series", response_model=List[SeriesDto])
def list_series():
    series = db.series.find()

    if not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@sg_router.get("/search/title", summary="Buscar Séries por Título", response_model=List[SeriesDto])
def search_series_by_title(title: str = Query(..., description="Título da série")):
    query = {"title": {"$regex": title, "$options": "i"}}

    series = list(db.series.find(query))

    if not series:
        raise HTTPException(status_code=404, detail="Nenhuma serie encontrada com o titulo fornecido.")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@sg_router.get("/search/genre", summary="Buscar Séries por Gênero", response_model=List[SeriesDto])
def search_series_by_genre(genre: str = Query(..., description="Gênero da série")):
    query = {"genre": {"$regex": genre, "$options": "i"}}

    series = list(db.series.find(query))

    if not series:
        raise HTTPException(status_code=404, detail="Nenhuma serie encontrada com o gênero fornecido.")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return [serializeSeriesDto(serie) for serie in series]


@sg_router.get("/imdb/{imdbid}", summary="Buscar Série pelo ID do IMDb", response_model=SeriesDto)
def get_series_by_imdbid(imdbid: str):
    series = db.series.find_one({"imdbid": imdbid})

    if not series:
        raise HTTPException(status_code=404, detail="Série não encontrada")
    elif not series:
        raise HTTPException(status_code=500, detail="Séries não encontradas")

    return serializeSeriesDto(series)