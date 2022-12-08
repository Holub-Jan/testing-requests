from db.manager import DBManager


class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()

        self._load_secrets()
        self.db = DBManager(self._db_pass)

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def test_run(self):
        new_table_data = [
            ["rollno", "INT"],
            ["name", "TEXT"],
        ]

        insert_list = [1, "john"]
        #self.db_entity.new_table('newtable', new_table_data)
        #self.db.add_to_table('newtable', insert_list)

        print(self.db.get_table('newtable'))


x = CLI()

x.test_run()
