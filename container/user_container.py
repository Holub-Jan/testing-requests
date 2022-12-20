from container.generic_container import GenericContainer
from storage import SQLiteClient
from storage.models import User
from storage.user_storage import UserStorage


class UserContainer(GenericContainer):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = UserStorage(client)

    def get_or_create(self, name: str, team_id: int):
        # Returning key row, if it doesn't exist, it also creates it
        org = self.storage.select_by_data([('name', name), ('team_id', team_id)])
        if not org:
            new_org = User(name=name, team_id=team_id)
            self.storage.create(new_org)
        return self.storage.select_by_name(name)
