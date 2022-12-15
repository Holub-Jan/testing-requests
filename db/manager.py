import os

from pysqlitecipher import sqlitewrapper


class DBManager:
    def __init__(self, password):
        self.password = password
        self._db_path = os.path.realpath('../db/pysqlitecipher.db')
        self.db = sqlitewrapper.SqliteCipher(dataBasePath=self._db_path, checkSameThread=False, password=self.password)

        # self._gen_empty_db()

    def new_table(self, table_name, table_data):
        self.db.createTable(table_name, table_data, makeSecure=True, commit=True)

    def get_table(self, table_name):
        return self.db.getDataFromTable(table_name, raiseConversionError=True, omitID=False)

    def add_to_table(self, table_name, table_data):
        self.db.insertIntoTable(table_name, table_data, commit=True)

    def delete_table_row(self, table_name, row, update_id):
        self.db.deleteDataInTable(table_name, row, commit=True, raiseError=True, updateId=update_id)

    def update_ids(self, table_name):
        self.db.updateIDs(table_name, commit=True)

    def get_all_tables(self):
        return self.db.getAllTableNames()

    def desc_table(self, table_name):
        # Returns table headers and their data types
        return self.db.describeTable(table_name)

    def db_table_check(self, table_name, cols, values):
        # Checks if specific cols of a table have specific values
        table_names, table_data = self.get_table(table_name)
        not_in = True

        for row in table_data:
            row_data = list()
            for col in cols:
                row_data.append(row[table_names.index(col)])

            if row_data == values:
                not_in = False

        return not_in, len(table_data)

    def get_value(self, table_name, in_col, value, out_col):
        # Check if value is present in specific table
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
        self._gen_team_repos_table()
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
            ['org_id', 'INT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_team_repos_table(self):
        table_name = 'teamRepos'
        table_columns = [
            ['name', 'TEXT'],
            ['repo_id', 'INT'],
            ['team_id', 'INT'],
            ['role', 'TEXT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_user_table(self):
        table_name = 'users'
        table_columns = [
            ['name', 'TEXT'],
            ['team_id', 'INT']
        ]
        self.new_table(table_name, table_columns)

    def _gen_key_table(self):
        # TODO : add private key
        table_name = 'keys'
        table_columns = [
            ['name', 'TEXT'],
            ['repo_id', 'INT'],
            ['key', 'TEXT'],
            ['read_only', 'INT'],
        ]
        self.new_table(table_name, table_columns)
