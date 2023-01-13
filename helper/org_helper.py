from typing import List, Optional, Tuple

from pydantic import BaseModel
from helper.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Organization


class OOrganization(BaseModel):
    repositories: Optional[list]
    teams: Optional[list]


class OrganizationHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)

    def get_or_create(self, name: str):
        # Returning org row, if it doesn't exist, it also creates it
        query = [('name', name)]
        org_exists = self.exists(query)
        if not org_exists:
            new_org = Organization(name=name, active=0)
            self._org_storage.create(new_org)
        return self._org_storage.select_by_query(query)

    def get_details(self, org_id: int) -> OOrganization:
        query = [('org_id', org_id)]
        repos = self._repo_storage.select_by_query(query)
        teams = self._team_storage.select_by_query(query)

        org = OOrganization(repositories=repos, team=teams)
        return org

    def delete_by_ids(self, ids_: List[int]):
        for id_ in ids_:
            self._org_storage.delete_by_id(id_, False)

        self._org_storage.update_ids()

    def update(self):
        # todo create update method
        pass

    def exists(self, query: List[Tuple]):
        return self._org_storage.select_by_query(query)
