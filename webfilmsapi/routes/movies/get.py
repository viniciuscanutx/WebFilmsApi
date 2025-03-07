from typing import List

from fastapi import APIRouter, HTTPException, Query

from webfilmsapi.models.model import MovieDto
from webfilmsapi.schemas.schema import serializeFilm, serializeFilmDto

from ...config.db import db


mg_router = APIRouter(prefix='/movies', tags=['Movies / Get'])


@mg_router.get("/get", summary="Exibir Todos Os Filmes", response_model=List[MovieDto])
async def list_films():
    movies = db.movies.find()

    if not movies:
        raise HTTPException(status_code=500, detail="Filmes não encontrados")

    return [serializeFilmDto(movie) for movie in movies]


@mg_router.get("/imdb/{imdbid}", summary="Buscar Filme pelo ID do IMDb", response_model=MovieDto)
async def get_movie_by_imdbid(imdbid: str):
    movie = db.movies.find_one({"imdbid": imdbid})

    if not movie:
        raise HTTPException(status_code=404, detail="ID não encontrado")

    return serializeFilm(movie)


@mg_router.get("/search/title", summary="Buscar Filmes por Título", response_model=List[MovieDto])
async def search_movies_by_title(title: str = Query(..., description="Título do filme")):
    query = {"title": {"$regex": title, "$options": "i"}}
    movies = list(db.movies.find(query))

    if not movies:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado com o título fornecido.")

    return [serializeFilm(movie) for movie in movies]


@mg_router.get("/search/genre", summary="Buscar Filmes por Gênero", response_model=List[MovieDto])
async def search_movies_by_genre(genre: str = Query(..., description="Gênero do filme")):
    query = {"genre": {"$regex": genre, "$options": "i"}}
    movies = list(db.movies.find(query))

    if not movies:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado com o gênero fornecido.")

    return [serializeFilm(movie) for movie in movies]