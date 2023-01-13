from typing import List, Tuple

from pydantic import BaseModel
from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Team


class TTeam(BaseModel):
    name: str
    repositories: list
    users: list


class TeamHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning team row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        team_exists = self.exists(query)
        if not team_exists:
            new_team = Team(name=name, org_id=org_id)
            self._team_storage.create(new_team)
        return self._team_storage.select_by_query(query)

    def get_details(self, name: str, team_id: int) -> TTeam:
        query = [('team_id', team_id)]
        repos = self._repo_storage.select_by_query(query)
        users = self._user_storage.select_by_query(query)

        team = TTeam(name=name, repositories=repos, users=users)
        return team

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._team_storage.delete_by_id(id_, False)

        self._team_storage.update_ids()

    def update(self):
        # todo create update method
        pass

    def exists(self, query: List[Tuple]):
        return self._team_storage.select_by_query(query)
