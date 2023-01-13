from storage import SQLiteClient
from storage.generic_storage import GenericStorage
from storage.models import Key


class KeyStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("key", Key, client)
