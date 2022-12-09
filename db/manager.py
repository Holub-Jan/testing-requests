import os

from pysqlitecipher import sqlitewrapper


class DBManager:
    def __init__(self, password):
        self._db_path = os.path.realpath('../db/pysqlitecipher.db')
        self.db = sqlitewrapper.SqliteCipher(dataBasePath=self._db_path, checkSameThread=False, password=password)

    def new_table(self, table_name, table_data):
        self.db.createTable(table_name, table_data, makeSecure=True, commit=True)

    def get_table(self, table_name):
        return self.db.getDataFromTable(table_name, raiseConversionError=True, omitID=False)

    def add_to_table(self, table_name, table_data):
        self.db.insertIntoTable(table_name, table_data, commit=True)

    def get_all_tables(self):
        return self.db.getAllTableNames()

    def delete_table(self, table_name):
        # TODO : how do we do this? lib doesnt have delete table function
        pass

    def desc_table(self, table_name):
        return self.db.describeTable(table_name)







