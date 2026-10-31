import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

def _normalize_database_url(url: str) -> str:
    """Memastikan URL PostgreSQL milih driver Psycopg 3"""
    if url.startswith("postgres://"):
        url = "postgresql+psycopg://" + url[len("postgres://") :]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://") :]
    
    if not url.startswith("postgresql+psycopg://"):
        raise RuntimeError(
            "DATABASE_URL harus menggunakan PostgreSQL dengan driver Psycopg 3."
        )
        
    return url

_raw_database_url = os.getenv("DATABASE_URL", "").strip()
if not _raw_database_url:
    raise RuntimeError(
        "DATABASE_URL belum diatur. Isi variabel tersebut di environment"
        "atau file .env pada root project."
    ) 

DATABASE_URL = _normalize_database_url(_raw_database_url)

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if origin.strip()
]