from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.movies.get import mg_router
from .routes.movies.post import mp_router
from .routes.movies.put import mput_router
from .routes.movies.delete import md_router

app = FastAPI(
    title="WebFilmsAPI",
    description="Sua API de Filmes, Séries e Canais.",
    version="1.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    license_info={
        "name": "MIT",
    },
    swagger_ui_parameters={
        "docExpansion": "none",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(mg_router)
app.include_router(mp_router)
app.include_router(mput_router)
app.include_router(md_router)
