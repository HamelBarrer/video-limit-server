from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import record_router

app = FastAPI()

if not Path('static').exists():
    Path('static').mkdir()

app.mount('/static', StaticFiles(directory='static'), name='static')

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(record_router.router)
