from typing import List, Tuple

from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import User


class UserHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str, team_id: int):
        # Returning key row, if it doesn't exist, it also creates it
        query = [('name', name), ('team_id', team_id)]
        user_exists = self.exists(query)
        if not user_exists:
            new_user = User(name=name, team_id=team_id)
            self._user_storage.create(new_user)
        return self._user_storage.select_by_query(query)

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._user_storage.delete_by_id(id_, False)

        self._user_storage.update_ids()

    def update(self):
        # todo create update method
        pass

    def exists(self, query: List[Tuple]):
        return self._user_storage.select_by_query(query)