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
    rating: float
    ratingrt: float
    poster: str
    banner: str
    link: str
    subtitles: str


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
    ratingrt: float
    poster: str
    banner: str


class SeriesDto(BaseModel):
    imdbid: str
    title: str
    overview: str
    nseasons: int
    releaseYear: str
    releaseDate: str
    status: str
    parentalRating: str
    genre: List[str]
    rating: float
    ratingrt: float
    poster: str
    banner: str


class Channels(BaseModel):
    title: str
    category: str
    link: str
    logo: str
    
    
class SuccessMessageID(BaseModel):
    message: str
    imdbid: str
    
    
class SuccessMessageTitle(BaseModel):
    message: str
    title: str
    
    
class ChannelsDto(BaseModel):
    title: str
    category: str
    logo: str