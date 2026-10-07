from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from radar_api import __version__
from radar_api.config import settings
from radar_api.logging import setup_logging
from radar_api.models import Category, LatestDocument, PaginatedResponse, Signal
from radar_api.repository import FileSignalRepository, SignalRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(
    title="Radar Venezuela API",
    version=__version__,
    description="API de solo lectura para señales de Radar Venezuela (MVP).",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


def get_repository() -> SignalRepository:
    return FileSignalRepository()


RepoDep = Annotated[SignalRepository, Depends(get_repository)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/v1/signals", response_model=PaginatedResponse[Signal])
def list_signals(
    repo: RepoDep,
    category: Category | None = None,
    from_date: date | None = Query(None, alias="from"),
    to_date: date | None = Query(None, alias="to"),
    tag: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    cursor: str | None = None,
) -> PaginatedResponse[Signal]:
    signals = repo.get_all(category=category, from_date=from_date, to_date=to_date, tag=tag)

    if cursor:
        try:
            cursor_idx = next(i for i, s in enumerate(signals) if s.id == cursor)
            signals = signals[cursor_idx + 1 :]
        except StopIteration:
            signals = []

    items = signals[:limit]
    next_cursor = items[-1].id if len(signals) > limit else None

    return PaginatedResponse(items=items, next_cursor=next_cursor)


@app.get("/v1/signals/{signal_id}", response_model=Signal)
def get_signal(signal_id: str, repo: RepoDep) -> Signal:
    signal = repo.get_by_id(signal_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Señal no encontrada")
    return signal


@app.get("/v1/radar/latest", response_model=LatestDocument)
def latest(repo: RepoDep) -> LatestDocument:
    signals = repo.get_all()
    # Retornamos los últimos 50
    return LatestDocument(schema_version="0.1.0", signals=signals[:50])


@app.get("/v1/meta/categories", response_model=list[str])
def list_categories() -> list[str]:
    # Extraer los valores literales del tipo Category
    from radar_api.models import Category
    import typing
    return list(typing.get_args(Category))


@app.get("/v1/meta/sources", response_model=list[str])
def list_sources(repo: RepoDep) -> list[str]:
    # Extrae una lista única de fuentes a partir de los datos existentes
    signals = repo.get_all()
    sources = set()
    for s in signals:
        for source in s.sources:
            sources.add(source.name)
    return sorted(sources)
