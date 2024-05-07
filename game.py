import os
from dataclasses import dataclass, field
from typing import Optional, List
from pymongo import collection
from pymongo.database import Database
from config_reader import config
from aiogram.types import FSInputFile


@dataclass
class Player:
    _id: int
    current_event: Optional[int] = None
    guessed_events: List[int] = field(default_factory=list)
    score: int = 0
    attempts: int = 0

    @property
    def in_game(self):
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
            path = os.path.join(config.BASE_DIR, self.image_path)
            return FSInputFile(path) if os.path.isfile(path) else None

    def explain(self):
        return "{} - {}".format(self.date, self.event)


class GuessGame:
    def __init__(self, database: Database):
        self.events_collection: collection = database["events"]

    def get_random_event(self) -> Optional[HistoricalEvent]:
        event = self.events_collection.aggregate([{"$sample": {"size": 1}}])
        if event:
            return HistoricalEvent(**event[0])
        return None
