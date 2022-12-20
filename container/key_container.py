from container.generic_container import GenericContainer
from storage import SQLiteClient
from storage.key_storage import KeyStorage
from storage.models import Key


class KeyContainer(GenericContainer):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = KeyStorage(client)

    def get_or_create(self, name: str, repo_id: int, private_key: str, public_key: str, read_only: int):
        # Returning org row, if it doesn't exist, it also creates it
        org = self.storage.select_by_data([('name', name), ('repo_id', repo_id)])
        if not org:
            new_org = Key(name=name,
                          repo_id=repo_id,
                          private_key=private_key,
                          public_key=public_key,
                          read_only=read_only)
            self.storage.create(new_org)
        return self.storage.select_by_name(name)
