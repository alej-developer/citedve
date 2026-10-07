from __future__ import annotations

from datetime import date

from fastapi import FastAPI, HTTPException, Query

from radar_api import __version__
from radar_api.models import ClaimType, Domain, LatestDocument, Signal
from radar_api.store import load_latest, load_signals

app = FastAPI(
    title="Radar Venezuela API",
    version=__version__,
    description=(
        "Consulta de señales citadas. Cada señal incluye fuente, fecha de captura y enlace. "
        "No constituye consejo de inversión."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/v1/signals", response_model=list[Signal])
def list_signals(
    domain: Domain | None = None,
    claim_type: ClaimType | None = None,
    edition: date | None = None,
    limit: int = Query(default=100, ge=1, le=500),
) -> list[Signal]:
    signals = load_signals()
    if domain:
        signals = [s for s in signals if s.domain == domain]
    if claim_type:
        signals = [s for s in signals if s.claim_type == claim_type]
    if edition:
        signals = [s for s in signals if s.edition == edition]
    return signals[:limit]


@app.get("/v1/signals/latest", response_model=LatestDocument)
def latest() -> LatestDocument:
    return load_latest()


@app.get("/v1/signals/{signal_id}", response_model=Signal)
def get_signal(signal_id: str) -> Signal:
    for signal in load_signals():
        if signal.id == signal_id:
            return signal
    raise HTTPException(status_code=404, detail="Señal no encontrada")
