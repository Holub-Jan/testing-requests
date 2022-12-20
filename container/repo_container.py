from container.generic_container import GenericContainer
from storage import SQLiteClient
from storage.models import Repository
from storage.repository_storage import RepositoryStorage


class RepositoryContainer(GenericContainer):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = RepositoryStorage(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning repo row, if it doesn't exist, it also creates it
        org = self.storage.select_by_data([('name', name), ('org_id', org_id)])
        if not org:
            new_org = Repository(name=name, org_id=org_id)
            self.storage.create(new_org)
        return self.storage.select_by_name(name)
