from typing import List, Optional, Union
from pydantic import BaseModel

class MovieDto(BaseModel):
    imdbid: str
    title: str
    overview: str
    runtime: str
    releaseYear: str
    releaseDate: str
    parentalRating: str
    genre: List[str]
    rating: float
    ratingrt: float
    poster: str
    banner: str

class Episode(BaseModel):
    epnumber: str
    title: str
    link: str
    subtitles: Optional[str] = None

class Season(BaseModel):
    seasonnumber: int
    episodes: List[Episode] = []

class SeriesDto(BaseModel):
    imdbid: str
    title: str
    overview: str
    nseasons: Union[int, List[Season]]  
    releaseYear: int
    releaseDate: str
    status: str
    parentalRating: str
    genre: List[str]
    rating: float
    ratingrt: float
    poster: str
    banner: str


class ChannelsDto(BaseModel):
    title: str
    category: str
    logo: str