import os

from pysqlitecipher import sqlitewrapper


class DBManager:
    def __init__(self, password):
        self.password = password
        self._db_path = os.path.realpath('../db/pysqlitecipher.db')
        self.db = sqlitewrapper.SqliteCipher(dataBasePath=self._db_path, checkSameThread=False, password=self.password)

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

    def db_table_check(self, table_name, col, value):
        # TODO : if needed, add function for checking multiple variables
        table_names, table_data = self.get_table(table_name)
        not_in = True
        for row in table_data:
            if row[table_names.index(col)] == value:
                not_in = False

        return not_in, len(table_data)

    def get_value(self, table_name, in_col, value, out_col):
        table_names, table_data = self.get_table(table_name)
        not_in = True

        for row in table_data:
            if row[table_names.index(in_col)] == value:
                not_in = row[table_names.index(out_col)]

        return not_in

    def _gen_empty_db(self):
        self._gen_org_table()
        self._gen_repo_table()
        self._gen_team_table()
        self._gen_key_table()
        self._gen_user_table()

    def _gen_org_table(self):
        table_name = 'organizations'
        table_columns = [
            ['name', 'TEXT'],
            ['active', 'INT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_repo_table(self):
        table_name = 'repositories'
        table_columns = [
            ['name', 'TEXT'],
            ['org_id', 'INT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_team_table(self):
        table_name = 'teams'
        table_columns = [
            ['name', 'TEXT'],
            ['repo_id', 'INT'],
            ['role', 'TEXT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_key_table(self):
        table_name = 'users'
        table_columns = [
            ['name', 'TEXT'],
            ['team_id', 'INT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_user_table(self):
        table_name = 'keys'
        table_columns = [
            ['name', 'TEXT'],
            ['repo_id', 'INT']
        ]
        self.new_table(table_name, table_columns)
