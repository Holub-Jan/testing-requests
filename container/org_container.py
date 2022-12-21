from container.generic_container import GenericContainer
from storage import SQLiteClient
from storage.models import Organization
from storage.organization_storage import OrganizationStorage


class OrganizationContainer(GenericContainer):
    def __init__(self, client: SQLiteClient):
        super().__init__(client)
        self.storage = OrganizationStorage(client)

    def get_or_create(self, name: str):
        # Returning org row, if it doesn't exist, it also creates it
        org = self.storage.select_by_name(name)
        if not org:
            new_org = Organization(name=name, active=0)
            self.storage.create(new_org)
        return self.storage.select_by_name(name)