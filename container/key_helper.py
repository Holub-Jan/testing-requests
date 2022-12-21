from container.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.key_storage import KeyStorage
from storage.models import Key


class KeyHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = KeyStorage(client)

    def get_or_create(self, name: str, repo_id: int, private_key: str, public_key: str, read_only: int):
        # Returning key row, if it doesn't exist, it also creates it
        query = [('name', name), ('repo_id', repo_id)]
        key = self.storage.select_by_data(query)
        if not key:
            new_key = Key(name=name,
                          repo_id=repo_id,
                          private_key=private_key,
                          public_key=public_key,
                          read_only=read_only)
            self.storage.create(new_key)
        return self.storage.select_by_data(query)
