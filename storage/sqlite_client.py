from typing import Type

from pysqlitecipher.sqlitewrapper import SqliteCipher


class SQLiteClient:
    def __init__(self, file_path: str, password: str):
        self._db = SqliteCipher(
            dataBasePath=file_path,
            checkSameThread=False,
            password=password
        )
        self.inner_types = {
            int: 'INT',
            str: 'TEXT'
        }

    def client(self) -> SqliteCipher:
        return self._db

    def create_table_if_not_exists(self, table_name: str, type_: Type):
        # Create table if it doesn't exist
        exists = self._db.checkTableExist(table_name)
        if not exists:
            columns = []
            if hasattr(type_, '__fields__'):
                for f in [tf for tf in type_.__fields__ if tf != "id_"]:
                    t = type_.__fields__[f].type_
                    columns.append([f, self.inner_types[t]])
                self._db.createTable(table_name, columns)
            else:
                raise RuntimeError(f"Unable to create table from unsupported class {type_.__name__}")
