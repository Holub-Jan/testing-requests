from pydantic import BaseModel

from container.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.key_storage import KeyStorage
from storage.models import Repository
from storage.repository_storage import RepositoryStorage


class RRepository(BaseModel):
    name: str
    keys: list


class RepositoryHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self._repo_storage = RepositoryStorage(client)
        self._key_storage = KeyStorage(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning repo row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        repo = self._repo_storage.select_by_query(query)
        if not repo:
            new_repo = Repository(name=name, org_id=org_id)
            self._repo_storage.create(new_repo)
        return self._repo_storage.select_by_query(query)

    def get_details(self, name: str, repo_id: int) -> RRepository:
        query = [('repo_id', repo_id)]
        keys = self._key_storage.select_by_query(query)
        repo = RRepository(name=name, keys=keys)

        return repo
