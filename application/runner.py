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
        org_id = self._check_org(self._org_name)
        msg_type, repo_list, teams_list = self.gh_link.get_org_info()

        if msg_type == 'ok':
            clean_repo_list = json.loads(repo_list)
            col = 'name'
            for table in clean_repo_list:
                print(f'Repository name: {table[col]}')
                not_in, table_len = self.db.db_table_check('repositories', col, table[col])
                repo_id = self._check_repo(table[col], org_id)

                if not_in:
                    print(f'Repository is not in db.'
                          f'\n[ {table[col]} ] added'
                          f'\n- Table ID: {repo_id}'
                          f'\n- Organization ID: {org_id}\n')
                else:
                    print(f'Repository [ {table[col]} ] is in db.\n')
        else:
            print(f'An error has occurred: {repo_list}')

    def _check_org(self, org_name):
        col = 'name'
        table_name = 'organizations'
        not_in, table_len = self.db.db_table_check(table_name, col, org_name)

        if not_in:
            data = [org_name, 0]
            self.db.add_to_table(table_name, data)

            return table_len

        else:
            org_id = self.db.get_value(table_name, 'name', org_name, 'ID')

            return org_id

    def _check_repo(self, repo_name, org_id):
        col = 'name'
        table_name = 'repositories'
        not_in, table_len = self.db.db_table_check(table_name, col, repo_name)

        if not_in:
            data = [repo_name, org_id]
            self.db.add_to_table(table_name, data)

            return table_len

        else:
            repo_id = self.db.get_value(table_name, 'name', repo_name, 'ID')

            return repo_id

    def _set_active_org(self):
        # TODO : create function for setting active org
        pass

    def _check_teams(self, org_name):
        # TODO : not done
        col = 'name'
        table_name = 'teams'
        not_in, table_len = self.db.db_table_check(table_name, col, org_name)

        if not_in:
            data = [org_name, 0]
            self.db.add_to_table(table_name, data)

            return table_len

        else:
            org_id = self.db.get_value(table_name, 'name', org_name, 'ID')

            return org_id

    def test_run(self):
        print(self.gh_link.check_team_repo_permission('test-team', 'renamed-repo'))

        print()
        for table in self.db.get_all_tables():
            print(self.db.get_table(table[0]))
        # self.gh_link.check_status()

        ''' displays all tables and types
        for table in self.db.get_all_tables():
            print(table[0])
            for each in self.db.desc_table(table[0]):
                print(each)
            print('\n')
            
        '''


if __name__ == "__main__":
    x = CLI()

    x.test_run()
