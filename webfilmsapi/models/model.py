from typing import List, Optional, Union
from pydantic import BaseModel

class Movies(BaseModel):
    imdbid: str
    title: str
    overview: str
    runtime: str
    releaseYear: str
    releaseDate: str
    parentalRating: str
    genre: List[str]
    rating: str
    rattingrt: Optional[float] = None
    poster: str
    banner: str
    link: str
    subtitles: str

class Episode(BaseModel):
    epnumber: str
    title: str
    link: str
    subtitles: Optional[str] = None

class Season(BaseModel):
    seasonnumber: int
    episodes: List[Episode] = []

class Series(BaseModel):
    imdbid: str
    title: str
    overview: str
    nseasons: Union[int, List[Season]]  
    releaseYear: str
    releaseDate: str
    status: str
    parentalRating: str
    genre: List[str]
    rating: float
    rattingrt: Optional[float] = None
    poster: str
    banner: str


class Channels(BaseModel):
    title: str
    category: str
    link: str
    logo: str