import os

from pysqlitecipher import sqlitewrapper


class DBManager:
    def __init__(self, password):

        self.db = sqlitewrapper.SqliteCipher(dataBasePath=os.path.realpath('../db/pysqlitecipher.db'), checkSameThread=False, password=password)

    def new_table(self, table_name, table_data):
        self.db.createTable(table_name, table_data, makeSecure=True, commit=True)

    def get_table(self, table_name):
        return self.db.getDataFromTable(table_name, raiseConversionError=True, omitID=False)

    def add_to_table(self, table_name, table_data):
        self.db.insertIntoTable(table_name, table_data, commit=True)







