from abc import ABC

from helper import OrganizationHelper
from helper.key_helper import KeyHelper
from helper.repo_helper import RepositoryHelper
from helper.team_helper import TeamHelper
from helper.team_repo_helper import TeamRepositoryHelper
from helper.user_helper import UserHelper
from storage import SQLiteClient


class GenericLieutenant(ABC):
    def __init__(self, client: SQLiteClient, org_name: str):
        self._client = client
        self._org_name = org_name

        self.org_table = OrganizationHelper(self._client)
        self.repo_table = RepositoryHelper(self._client)
        self.team_table = TeamHelper(self._client)
        self.team_repo_table = TeamRepositoryHelper(self._client)
        self.user_table = UserHelper(self._client)
        self.key_table = KeyHelper(self._client)

    def _org_id(self):
        return self.org_table.get_or_create(self._org_name)[0].id_

    def _repo_id(self, repo_name: str):
        return self.repo_table.get_or_create(repo_name, self._org_id())[0].id_

    def _team_id(self, team_name: str):
        return self.team_table.get_or_create(team_name, self._org_id())[0].id_

    def _team_repo_id(self, name: str, team_id: int, repo_id: int, role: str):
        return self.team_repo_table.get_or_create(name, team_id, repo_id, role)[0].id_

    def _user_id(self, user_name, team_id):
        return self.user_table.get_or_create(user_name, team_id)[0].id_
