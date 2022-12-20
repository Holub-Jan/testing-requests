from storage import SQLiteClient
from storage.generic_storage import GenericStorage
from storage.models import Team


class TeamStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("team", Team, client)
