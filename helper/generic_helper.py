from abc import abstractmethod, ABC

from storage import SQLiteClient, OrganizationStorage
from storage.key_storage import KeyStorage
from storage.repository_storage import RepositoryStorage
from storage.team_repository_storage import TeamRepositoryStorage
from storage.team_storage import TeamStorage
from storage.user_storage import UserStorage


class GenericHelper(ABC):
    def __init__(self, client: SQLiteClient):
        self._repo_storage = RepositoryStorage(client)
        self._key_storage = KeyStorage(client)
        self._team_storage = TeamStorage(client)
        self._org_storage = OrganizationStorage(client)
        self._user_storage = UserStorage(client)
        self._team_repo_storage = TeamRepositoryStorage(client)

    @abstractmethod
    def get_or_create(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_by_ids(self, *args, **kwargs):
        pass

    @abstractmethod
    def exists(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_row_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_id(self, *args, **kwargs):
        pass
