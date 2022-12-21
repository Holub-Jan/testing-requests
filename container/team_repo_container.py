from container.generic_container import GenericContainer
from storage import SQLiteClient
from storage.models import TeamRepository
from storage.team_repository_storage import TeamRepositoryStorage


class TeamRepositoryContainer(GenericContainer):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = TeamRepositoryStorage(client)

    def get_or_create(self, name: str, team_id: int, repo_id: int, role: str):
        # Returning team repository row, if it doesn't exist, it also creates it
        query = [('name', name), ('team_id', team_id), ('repo_id', repo_id)]
        team_repo = self.storage.select_by_data(query)
        if not team_repo:
            new_team_repo = TeamRepository(name=name, team_id=team_id, repo_id=repo_id, role=role)
            self.storage.create(new_team_repo)
        return self.storage.select_by_data(query)
