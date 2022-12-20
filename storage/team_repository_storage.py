from storage import SQLiteClient
from storage.generic_storage import GenericStorage
from storage.models import TeamRepository


class TeamRepositoryStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("teamRepository", TeamRepository, client)
