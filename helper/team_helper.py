from pydantic import BaseModel
from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Team
from storage.repository_storage import RepositoryStorage
from storage.team_storage import TeamStorage
from storage.user_storage import UserStorage


class TTeam(BaseModel):
    name: str
    repositories: list
    users: list


class TeamHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self._team_storage = TeamStorage(client)
        self._repo_storage = RepositoryStorage(client)
        self._user_storage = UserStorage(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning team row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        team = self._team_storage.select_by_query(query)
        if not team:
            new_team = Team(name=name, org_id=org_id)
            self._team_storage.create(new_team)
        return self._team_storage.select_by_query(query)

    def get_details(self, name: str, team_id: int) -> TTeam:
        query = [('team_id', team_id)]
        repos = self._repo_storage.select_by_query(query)
        users = self._user_storage.select_by_query(query)

        team = TTeam(name=name, repositories=repos, users=users)
        return team
