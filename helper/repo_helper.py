from typing import List, Tuple

from pydantic import BaseModel
from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Repository


class RRepository(BaseModel):
    name: str
    keys: list


class RepositoryHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning repo row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        repo_exists = self.exists(query)
        if not repo_exists:
            new_repo = Repository(name=name, org_id=org_id)
            self._repo_storage.create(new_repo)
        return self._repo_storage.select_by_query(query)

    def get_details(self, name: str, repo_id: int) -> RRepository:
        query = [('repo_id', repo_id)]
        keys = self._key_storage.select_by_query(query)
        repo = RRepository(name=name, keys=keys)

        return repo

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._repo_storage.delete_by_id(id_, False)
            # delete keys, delete from teams, delete team users

        self._repo_storage.update_ids()

    def update_col_by_id(self, id_: int, col_name: str, new_value: str):
        return self._repo_storage.update_column_by_id(id_, col_name, new_value)

    def update_row_by_id(self, row_data):
        return self._repo_storage.update_row_by_id(row_data)

    def exists(self, query: List[Tuple]):
        return self._repo_storage.select_by_query(query)

    def get_id(self, name: str, org_id: int):
        query = [('name', name), ('org_id', org_id)]
        repo_exists = self.exists(query)
        if repo_exists:
            repo_obj = self.get_or_create(name, org_id)
            return repo_obj[0].id_
