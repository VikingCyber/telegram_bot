from typing import List, Tuple

from pymongo import ReplaceOne
from pymongo.database import Database
from models import HistoricalEvent, Player


class ObjectNotExists(Exception):
    """ Исключение вызывается, когда документа нет в бд"""
    pass


class HistoricalEventDao:
    def __init__(self, database: Database):
        self.database = database
        self.collection = self.database['history']

    def all(self) -> List[HistoricalEvent]:
        cursor = self.collection.find({})
        events = [HistoricalEvent(**event) for event in cursor]
        return events


class PlayerDao:
    def __init__(self, data_source: Database):
        self.data_source = data_source
        self.collection = self.data_source['Players']

    def create(self, player: Player) -> Tuple[Player, bool]:
        player_db = self.collection.find_one({'_id': player._id})
        created = player_db is None

        if player_db:
            player = Player(**player_db)
        else:
            self.collection.insert_one(
                {
                    "_id": player._id,
                    "current_event": player.current_event,
                    "guessed_events": player.guessed_events,
                    "attempts": player.attempts,
                    "score": player.score,
                }
            )
        return player, created

    def get(self, player_id: int) -> Player:
        player = self.collection.find_one({"_id": player_id})
        if not player:
            raise ObjectNotExists(
                f"Игрока с id {player_id} не существует."
            )
        return Player(**player)

    def save_many(self, players: List[Player]):
        if not players:
            return

        update_players = [
            ReplaceOne(
                {"_id": player._id},
                {
                    "current_event": player.current_event,
                    "guessed_events": player.guessed_events,
                    "attempts": 0,
                    "score": player.score,
                },
                upsert=True,  # указывает Mongodb создать документ если c таким _id нет
            )
            for player in players
        ]
        self.collection.bulk_write(update_players)  # метод Mongodb для пакетной(множественной) записи
