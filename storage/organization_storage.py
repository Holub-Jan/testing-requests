from storage.generic_storage import GenericStorage
from storage.models import Organization
from storage.sqlite_client import SQLiteClient


class OrganizationStorage(GenericStorage):
    def __init__(self, client: SQLiteClient):
        super().__init__("organization", Organization, client)

    def select_by_name(self, name: str):
        # Returns org row if it matches the input name, else None
        # Question : can I move this to generic storage?
        table_cols, table_data = self.db.getDataFromTable(self._table_name)
        name_idx = table_cols.index('name')
        for row in table_data:
            if row[name_idx] == name:
                return self._row_to_class_instance(table_cols, row)

        return None
