import json
from datetime import date
from pathlib import Path
from typing import Protocol

from radar_api.config import settings
from radar_api.models import Category, Signal


class SignalRepository(Protocol):
    def get_all(
        self,
        category: Category | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        tag: str | None = None,
    ) -> list[Signal]:
        ...

    def get_by_id(self, signal_id: str) -> Signal | None:
        ...


class FileSignalRepository:
    def __init__(self, data_dir: str | None = None):
        self.signals_path = Path(data_dir or settings.data_dir) / "signals.json"

    def _load(self) -> list[Signal]:
        if not self.signals_path.exists():
            return []
        data = json.loads(self.signals_path.read_text(encoding="utf-8"))
        return [Signal.model_validate(s) for s in data.get("signals", [])]

    def get_all(
        self,
        category: Category | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        tag: str | None = None,
    ) -> list[Signal]:
        signals = self._load()
        
        if category:
            signals = [s for s in signals if s.category == category]
        if from_date:
            signals = [s for s in signals if s.as_of_date >= from_date]
        if to_date:
            signals = [s for s in signals if s.as_of_date <= to_date]
        if tag:
            signals = [s for s in signals if tag in s.tags]
            
        # Orden descendente por captura para cursor-based pagination simple
        signals.sort(key=lambda s: s.captured_at, reverse=True)
        return signals

    def get_by_id(self, signal_id: str) -> Signal | None:
        for s in self._load():
            if s.id == signal_id:
                return s
        return None
