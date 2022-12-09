from api.github_link import GitHubLink
from db.manager import DBManager
import json


class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()
        self._org_name = 'standa-novak'

        self._load_secrets()

        self.db = DBManager(self._db_pass)
        self.gh_link = GitHubLink(self._org_name, self._gh_token)

        self._load_org_info()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def _load_org_info(self):
        msg_type, data = self.gh_link.get_org_info()

        if msg_type == 'ok':
            data = json.loads(data)
            for each in data:
                print(f'Repo list: {each["name"]}')
        else:
            print(f'An error has occurred: {data}')

    def test_run(self):
        pass
        # self.gh_link.check_status()

        ''' displays all tables and types
        for table in self.db.get_all_tables():
            print(table[0])
            for each in self.db.desc_table(table[0]):
                print(each)
            print('\n')
            
        '''


x = CLI()

x.test_run()
