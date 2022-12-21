from container.generic_helper import GenericHelper
from storage import SQLiteClient
from storage.models import Team
from storage.team_storage import TeamStorage


class TTeam:
    name: str
    repositories: []
    users: []


class TeamHelper(GenericHelper):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = TeamStorage(client)

    def get_or_create(self, name: str, org_id: int):
        # Returning team row, if it doesn't exist, it also creates it
        query = [('name', name), ('org_id', org_id)]
        team = self.storage.select_by_data(query)
        if not team:
            new_team = Team(name=name, org_id=org_id)
            self.storage.create(new_team)
        return self.storage.select_by_data(query)
