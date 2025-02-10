from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import List
from bson import ObjectId
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from ..config.db import db, dbs, dbc
from ..schemas.schema import serializeFilm, serializeSeries, serializeChannel
from dotenv import load_dotenv
import os

load_dotenv()

read_only_router = APIRouter()

SECRET_PASSWORD = os.getenv("SECRET_KEY")

security = HTTPBearer()

def verify_password(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Pegando o token
    if token != SECRET_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta",
            headers={"WWW-Authenticate": "Bearer"},
        )

@read_only_router.get("/movies/found", summary="Exibir Todos Os Filmes", response_model=List[dict])
def list_films(password: str = Depends(verify_password)):
    movies = db.movies.find()
    return [serializeFilm(movie) for movie in movies]

@read_only_router.get("/movies/imdb/{imdbid}", summary="Buscar Filme pelo ID do IMDb", response_model=dict)
async def get_movie_by_imdbid(imdbid: str, password: str = Depends(verify_password)):
    movie = db.movies.find_one({"imdbid": imdbid})
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return serializeFilm(movie)

@read_only_router.get("/movies/search/title", summary="Buscar Filmes por Título", response_model=List[dict])
async def search_movies_by_title(title: str = Query(..., description="Título do filme"), password: str = Depends(verify_password)):
    query = {"title": {"$regex": title, "$options": "i"}}
    movies = db.movies.find(query)
    return [serializeFilm(movie) for movie in movies]

@read_only_router.get("/movies/search/genre", summary="Buscar Filmes por Gênero", response_model=List[dict])
async def search_movies_by_genre(genre: str = Query(..., description="Gênero do filme"), password: str = Depends(verify_password)):
    query = {"genre": {"$regex": genre, "$options": "i"}}
    movies = db.movies.find(query)
    return [serializeFilm(movie) for movie in movies]

@read_only_router.get("/series/found", summary="Exibir Todas As Series", response_model=List[dict])
async def list_series(password: str = Depends(verify_password)):
    series = dbs.series.find()
    return [serializeSeries(show) for show in series]

@read_only_router.get("/series/search/title", summary="Buscar Séries por Título", response_model=List[dict])
async def search_series_by_title(title: str = Query(..., description="Título da série"), password: str = Depends(verify_password)):
    query = {"title": {"$regex": title, "$options": "i"}}
    series = dbs.series.find(query)
    return [serializeSeries(show) for show in series]

@read_only_router.get("/series/search/genre", summary="Buscar Séries por Gênero", response_model=List[dict])
async def search_series_by_genre(genre: str = Query(..., description="Gênero da série"), password: str = Depends(verify_password)):
    query = {"genre": {"$regex": genre, "$options": "i"}}
    series = dbs.series.find(query)
    return [serializeSeries(show) for show in series]

@read_only_router.get("/series/imdb/{imdbid}", summary="Buscar Série pelo ID do IMDb", response_model=dict)
async def get_series_by_imdbid(imdbid: str, password: str = Depends(verify_password)):
    series = dbs.series.find_one({"imdbid": imdbid})
    if not series:
        raise HTTPException(status_code=404, detail="Série não encontrada")
    return serializeSeries(series)

@read_only_router.get("/channels/found", summary="Exibir Todos os Canais", response_model=List[dict])
def list_channels(password: str = Depends(verify_password)):
    channels = dbc.channels.find()
    return [serializeChannel(channel) for channel in channels]

@read_only_router.get("/channels/search/title", summary="Buscar Canais por Título", response_model=List[dict])
async def search_channels_by_title(title: str = Query(..., description="Título do canal"), password: str = Depends(verify_password)):
    query = {"title": {"$regex": title, "$options": "i"}}
    channels = dbc.channels.find(query)
    return [serializeChannel(channel) for channel in channels]

@read_only_router.get("/channels/search/genre", summary="Buscar Canais por Categoria", response_model=List[dict])
async def search_channels_by_genre(genre: str = Query(..., description="Categoria do canal"), password: str = Depends(verify_password)):
    query = {"genre": {"$regex": genre, "$options": "i"}}
    channels = dbc.channels.find(query)
    return [serializeChannel(channel) for channel in channels]

@read_only_router.get("/channels/{channel_id}", summary="Buscar Canal pelo ID", response_model=dict)
async def get_channel_by_id(channel_id: str, password: str = Depends(verify_password)):
    try:
        channel = dbc.channels.find_one({"_id": ObjectId(channel_id)})
        if not channel:
            raise HTTPException(status_code=404, detail="Canal não encontrado")
        return serializeChannel(channel)
    except Exception as e:
        raise HTTPException(status_code=400, detail="ID inválido")
