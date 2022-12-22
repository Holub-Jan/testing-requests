from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import User
from storage.user_storage import UserStorage


class UserHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = UserStorage(client)

    def get_or_create(self, name: str, team_id: int):
        # Returning key row, if it doesn't exist, it also creates it
        query = [('name', name), ('team_id', team_id)]
        user = self.storage.select_by_query(query)
        if not user:
            new_user = User(name=name, team_id=team_id)
            self.storage.create(new_user)
        return self.storage.select_by_query(query)
