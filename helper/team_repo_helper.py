from typing import List, Tuple

from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import TeamRepository


class TeamRepositoryHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str, team_id: int, org_id: int, role: str):
        # Returning team repository row, if it doesn't exist, it also creates it
        query = [('name', name), ('team_id', team_id), ('org_id', org_id)]
        team_repo_exists = self.exists(query)
        if not team_repo_exists:
            new_team_repo = TeamRepository(name=name, team_id=team_id, org_id=org_id, role=role)
            self._team_repo_storage.create(new_team_repo)
        return self._team_repo_storage.select_by_query(query)

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._team_repo_storage.delete_by_id(id_, False)

        self._team_repo_storage.update_ids()

    def update_row_by_id(self, row_data):
        return self._team_repo_storage.update_row_by_id(row_data)

    def exists(self, query: List[Tuple]):
        return self._team_repo_storage.select_by_query(query)

    def get_role(self, query: List[Tuple]):
        return self._team_repo_storage.select_by_query(query)[0].role

    def get_id(self, name: str, team_id: int, org_id: int, role: str):
        query = [('name', name), ('team_id', team_id), ('org_id', org_id)]
        team_repo_exists = self.exists(query)
        if team_repo_exists:
            team_repo_obj = self.get_or_create(name, team_id, org_id, role)
            return team_repo_obj[0].id_
