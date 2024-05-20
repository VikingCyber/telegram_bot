from pathlib import Path
from config_reader import config
from dataclasses import dataclass, field
from typing import Optional, List
from aiogram.types import FSInputFile


@dataclass
class Player:
    _id: int
    current_event: Optional[int] = None
    guessed_events: List[int] = field(default_factory=list)
    score: int = 0
    attempts: int = 0

    @property
    def in_game(self) -> bool:
        return isinstance(self.current_event, int)


@dataclass
class HistoricalEvent:
    _id: int
    _type: str
    event: str
    date: int
    description: str
    image_path: str

    def get_image_file(self):
        if self.image_path:
            path = Path(config.BASE_DIR).joinpath(self.image_path)
            return FSInputFile(path)

    def explain(self) -> str:
        return "{} - {}".format(self.date, self.event)
