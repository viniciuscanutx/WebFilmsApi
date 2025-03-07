from fastapi import APIRouter
from ...config.db import db

user = APIRouter()

@user.get("/", include_in_schema=False)
def welcome():
    movies_count = db.movies.count_documents({})
    series_count = db.series.count_documents({})
    channels_count = db.channels.count_documents({})

    return {
        "message": "WebFilmsAPI",
        "total_movies": movies_count,
        "total_series": series_count,
        "total_channels": channels_count
    }
