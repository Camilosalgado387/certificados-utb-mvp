from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import Base, engine, SessionLocal
from . import models
from .routers import catalog
from .services.seed import seed_catalog

# Garantiza que la carpeta local para guardar PDFs siempre exista al arrancar
STORAGE_DIR = Path(__file__).resolve().parent.parent / "storage" / "certificados"
STORAGE_DIR.mkdir(parents = True, exist_ok = True)


@asynccontextmanager

async def lifespan(app: FastAPI):
   
    Base.metadata.create_all(bind = engine)
    db = SessionLocal()
    try:
        seed_catalog(db)
    finally:
        db.close()
    yield
app = FastAPI(
    title="API Prototipo Certificados Académicos UTB",
    description="MVP local sin infraestructura pesada(FastAPI + SQLite)",
    version="0.1.0",
    lifespan = lifespan
)
# CORS: Como Next.js correrá en localhost:3000 yFastAPI en localhost:8000,
# el navegador bloquearía las peticiones si no autorizamos explícitamente ese origen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Sistema"])
def health_check():
    return{
        "status": "ok",
        "service":"certificados-utb-mvp",
        "storage_ready": STORAGE_DIR.exists(),
    }


app.include_router(catalog.router)