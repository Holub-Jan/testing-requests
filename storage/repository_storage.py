from storage import SQLiteClient
from storage.generic_storage import GenericStorage
from storage.models import Repository


class RepositoryStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("repository", Repository, client)
