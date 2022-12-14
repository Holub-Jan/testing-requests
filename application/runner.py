from api.github_link import GitHubLink
from db.manager import DBManager
import json


class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()
        self._org_name = 'standa-novak'
        self._print_details = False

        self._load_secrets()

        self.db = DBManager(self._db_pass)
        self.gh_link = GitHubLink(self._org_name, self._gh_token)

        #self._load_org_info()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def _load_org_info(self):
        # Checking data from GitHub about selected organization
        org_id, org_missing = self._check_org(self._org_name)
        self._added_check('Organization', self._org_name, org_missing)

        msg_type, msg = self.gh_link.get_org_info()

        col = 'name'

        if msg_type == 'ok':
            repo_list, teams_list = msg

            clean_repo_list = json.loads(repo_list)
            for repo in clean_repo_list:
                repo_name = repo[col]
                not_in = self._check_repo(repo_name, org_id)

                self._added_check('Repository', repo_name, not_in)

            clean_team_list = json.loads(teams_list)
            for team in clean_team_list:
                team_name = team[col]
                team_id, not_in = self._check_team(team_name, org_id)

                self._added_check('Team', team_name, not_in)

                for item, value in self._check_team_repos(team_name).items():
                    self._added_check('Team repository', item, value)

                for item, value in self._check_team_members(team_name, team_id).items():
                    self._added_check('Users', item, value)

            print(f'## Organization {self._org_name} loaded. ##')
        else:
            print(f'An error has occurred: {msg}')

    def _check_org(self, org_name):
        # Checks if repository is in database, if not present, it is added
        # Returns bool value and ID
        col = 'name'
        table_name = 'organizations'
        not_in, table_len = self.db.db_table_check(table_name, [col], [org_name])

        if not_in:
            data = [org_name, 0]
            self.db.add_to_table(table_name, data)

            return table_len, not_in

        else:
            org_id = self.db.get_value(table_name, 'name', org_name, 'ID')

            return org_id, not_in

    def _check_repo(self, repo_name, org_id):
        # Checks if repository is in database, if not present, it is added and returns bool value
        col = 'name'
        table_name = 'repositories'
        not_in, table_len = self.db.db_table_check(table_name, [col], [repo_name])

        if not_in:
            data = [repo_name, org_id]
            self.db.add_to_table(table_name, data)

        return not_in

    def _check_team(self, team_name, org_id):
        col = 'name'
        table_name = 'teams'
        not_in, table_len = self.db.db_table_check(table_name, [col], [team_name])

        if not_in:
            data = [team_name, org_id]
            self.db.add_to_table(table_name, data)

            return table_len, not_in
        else:
            team_id = self.db.get_value('teams', col, team_name, 'ID')
            return team_id, not_in

    def _check_team_repos(self, team_name):
        resp_type, resp = self.gh_link.list_team_repos(team_name)
        team_id = self.db.get_value('teams', 'name', team_name, 'ID')
        table_name = 'teamRepos'

        team_repos_states = dict()

        if resp_type == 'ok':
            resp_code, team_repo_list = resp
            clean_team_repo_list = json.loads(team_repo_list)

            for repo in clean_team_repo_list:
                repo_name = repo['name']
                repo_id = self.db.get_value('repositories', 'name', repo_name, 'ID')
                role = self.gh_link.check_team_repo_permission(team_name, repo_name)[1][1]

                cols = ['name', 'repo_id', 'team_id']
                row_data = [repo_name,
                            repo_id,
                            team_id,
                            role]

                not_in, table_len = self.db.db_table_check(table_name, cols, row_data[:-1])

                if not_in:
                    self.db.add_to_table(table_name, row_data)

                team_repos_states[team_name] = not_in

        return team_repos_states

    def _check_team_members(self, team_name, team_id):
        msg_type, (msg_code, user_list) = self.gh_link.list_team_members(team_name)
        user_states = dict()
        clean_user_list = json.loads(user_list)

        for user in clean_user_list:
            data = [user['login'], team_id]
            not_in, table_len = self.db.db_table_check('users', ['name', 'team_id'], data)

            if not_in:
                self.db.add_to_table('users', data)

            user_states[user['login']] = not_in

        return user_states

    def _set_active_org(self, new_org):
        # TODO : create function for setting active org
        self._org_name = new_org

    def test_run(self):
        """ In case of deleting table rows
        self.db.delete_table_row('users', 0, False)
        self.db.delete_table_row('users', 1, False)
        self.db.update_ids('users')
        """
        print(self.gh_link.list_repo_keys('test-repository'))
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

    def _added_check(self, unit, name, check_bool):
        if self._print_details:
            if check_bool:
                print(f'{name} was added to the database as {unit}.\n')
            else:
                print(f'{unit} "{name}" is in db.\n')


if __name__ == "__main__":
    x = CLI()

    x.test_run()
