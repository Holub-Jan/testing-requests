from storage import SQLiteClient
from storage.generic_storage import GenericStorage
from storage.models import User


class UserStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("user", User, client)
