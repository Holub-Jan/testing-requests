from container.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Repository
from storage.repository_storage import RepositoryStorage


class RepositoryHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = RepositoryStorage(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning repo row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        repo = self.storage.select_by_data(query)
        if not repo:
            new_repo = Repository(name=name, org_id=org_id)
            self.storage.create(new_repo)
        return self.storage.select_by_data(query)
