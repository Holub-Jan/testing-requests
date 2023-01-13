from typing import List

from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Key


class KeyHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str, repo_id: int, private_key: str, public_key: str, read_only: int):
        # Returning key row, if it doesn't exist, it also creates it
        query = [('name', name), ('repo_id', repo_id)]
        key_exists = self.exists(query)
        if not key_exists:
            new_key = Key(name=name,
                          repo_id=repo_id,
                          private_key=private_key,
                          public_key=public_key,
                          read_only=read_only)
            self._key_storage.create(new_key)
        return self._key_storage.select_by_query(query)

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._key_storage.delete_by_id(id_, False)

        self._key_storage.update_ids()

    def update(self):
        # todo create update method
        pass

    def exists(self, query: List[Tuple]):
        return self._key_storage.select_by_query(query)
