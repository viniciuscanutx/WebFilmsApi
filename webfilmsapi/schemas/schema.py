from typing import List, Dict

def serializeFilm(item) -> dict:
    return {
        "id": str(item["_id"]),
        "imdbid": item["imdbid"],
        "title": item["title"],
        "overview": item["overview"],
        "runtime": item["runtime"],
        "releaseYear": item["releaseYear"],
        "releaseDate": item["releaseDate"],
        "parentalRating": item["parentalRating"],
        "genre": item["genre"],
        "rating": item["rating"],
        "rattingrt": item["rattingrt"],
        "poster": item["poster"],
        "banner": item["banner"],
        "link": item["link"],
        "subtitles": item["subtitles"]
    }

def serializeSeries(item) -> dict:
    return {
        "id": str(item["_id"]),
        "imdbid": item["imdbid"],
        "title": item["title"],
        "overview": item["overview"],
        "nseasons": [
            {
                "seasonnumber": season["seasonnumber"],
                "episodes": season.get("episodes", [])
            } for season in item["nseasons"]
        ],
        "releaseYear": item["releaseYear"],
        "releaseDate": item["releaseDate"],
        "status": item["status"],
        "parentalRating": item["parentalRating"],
        "genre": item.get("genre", []),
        "rating": item["rating"],
        "rattingrt": item["rattingrt"],
        "poster": item["poster"],
        "banner": item["banner"]
    }
    
def serializeSeriesDto(item) -> dict:
    return {
        "id": str(item["_id"]),
        "imdbid": item["imdbid"],
        "title": item["title"],
        "overview": item["overview"],
        "nseasons": len(item["nseasons"]),
        "releaseYear": item["releaseYear"],
        "releaseDate": item["releaseDate"],
        "status": item["status"],
        "parentalRating": item["parentalRating"],
        "genre": item.get("genre", []),
        "rating": item["rating"],
        "rattingrt": item["rattingrt"],
        "poster": item["poster"],
        "banner": item["banner"]
    }


def serializeChannel(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title"],
        "category": item["category"],
        "link": item["link"],
        "logo": item["logo"]
    }

def serializeDict(a) -> dict:
    return {**{i: str(a[i]) for i in a if i == '_id'}, 
            **{i: a[i] for i in a if i != '_id'}}

def serializeList(entity) -> List[Dict]:
    return [serializeDict(a) for a in entity]

