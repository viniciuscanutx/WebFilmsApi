from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.route import user
from .routes.privateroutes import read_only_router

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


app.include_router(user)

app.include_router(read_only_router, prefix="/private", include_in_schema=False)
