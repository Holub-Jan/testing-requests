import uuid
from typing import Type, List, Tuple

from storage.models import TableModel
from storage.sqlite_client import SQLiteClient


def _generate_id() -> str:
    # Unused
    return str(uuid.uuid4())


class GenericStorage:

    def __init__(self, table_name: str, cls_type: Type, client: SQLiteClient):
        if not issubclass(cls_type, TableModel):
            raise RuntimeError('Class type is not table model sub class.')
        self._table_name = table_name
        self.client = client
        self.db = self.client.client()
        self.cls_type = cls_type
        self.client.create_table_if_not_exists(table_name, cls_type)

    def create(self, obj):
        # Creates new row from an object into the table
        obj_data = obj.dict()
        insert_values = []
        col_list = self.db.describeTable(self._table_name)
        for col_name in col_list:
            insert_values.append(obj_data[col_name[0]]) if col_name[0] != "ID" else None
        self.db.insertIntoTable(self._table_name, insert_values)

    def select_all(self):
        # Returns a list of objects for each row in the table
        cols, values = self.db.getDataFromTable(self._table_name)
        result = []
        for val in values:
            d = self._row_to_class_instance(cols, val)
            result.append(d)
        return result

    def select_by_id(self, id_: int):
        # Returns an object by row ID, if row doesn't exist, return None
        table_cols, table_data = self.db.getDataFromTable(self._table_name)
        for row in table_data:
            if row[0] == id_:
                return self._row_to_class_instance(table_cols, row)

        return None

    def _row_to_class_instance(self, row_col, row_data):
        # Returns an object with row data
        row_col = [c for c in row_col if c != "ID"]

        d = {'id_': row_data[0]}
        for i in range(len(row_col)):
            d[row_col[i]] = row_data[i + 1]

        return self.cls_type(**d)  # *d = (test_name, 123) , **d = (name=test_name, num=123)

    def select_by_query(self, query: List[Tuple]) -> list:
        # Returns object inputted data matches a row in selected columns, else return None
        table_cols, table_data = self.db.getDataFromTable(self._table_name)
        results = []
        for row in table_data:
            if all([row[table_cols.index(q[0])] == q[1] for q in query]):
                row_object = self._row_to_class_instance(table_cols, row)
                results.append(row_object)
        return results

    def delete_by_id(self, id_: int, update_id: bool = True):
        # Delete row by id if it exists
        table_cols, table_data = self.db.getDataFromTable(self._table_name)
        ids = [row[table_cols.index['ID']] for row in table_data]
        if id_ in ids:
            self.db.deleteDataInTable(tableName=self._table_name, iDValue=id_, updateId=update_id)
            return True  # Do I need this?

        return False

    def update_ids(self):
        # Update ids in the table
        self.db.updateIDs(self._table_name, commit=True)

    def update_column_by_id(self, id_: int, col_name: str, col_value: str):
        # Update row by id if it exists
        table_cols, table_data = self.db.getDataFromTable(self._table_name)
        ids = [row[table_cols.index['ID']] for row in table_data]
        if id_ in ids:
            self.db.updateInTable(tableName=self._table_name, iDValue=id_, colName=col_name, colValue=col_value)
            return True  # Do I need this?

        return False
