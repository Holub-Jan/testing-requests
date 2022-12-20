from storage.generic_storage import GenericStorage
from storage.models import Organization
from storage.sqlite_client import SQLiteClient


class OrganizationStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("organization", Organization, client)
