from pydantic import BaseModel
from container.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Organization
from storage.organization_storage import OrganizationStorage
from storage.repository_storage import RepositoryStorage
from storage.team_storage import TeamStorage


class OOrganization(BaseModel):
    name: str
    repositories: list
    teams: list


class OrganizationHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self._org_storage = OrganizationStorage(client)
        self._repo_storage = RepositoryStorage(client)
        self._team_storage = TeamStorage(client)

    def get_or_create(self, name: str):
        # Returning org row, if it doesn't exist, it also creates it
        query = [('name', name)]
        org = self._org_storage.select_by_query(query)
        if not org:
            new_org = Organization(name=name, active=0)
            self._org_storage.create(new_org)
        return self._org_storage.select_by_query(query)

    def get_details(self, name: str, org_id: int) -> OOrganization:
        query = [('org_id', org_id)]
        repos = self._repo_storage.select_by_query(query)
        teams = self._team_storage.select_by_query(query)

        org = OOrganization(name=name, repositories=repos, team=teams)
        return org
