from api.github_link import GitHubLink
from application.ssh_manager import SSHManager
from container.key_helper import KeyHelper
from container.org_helper import OrganizationHelper
from container.repo_helper import RepositoryHelper
from container.team_helper import TeamHelper
from container.team_repo_helper import TeamRepositoryHelper
from container.user_helper import UserHelper
from db.manager import DBManager
import json

from storage import SQLiteClient


class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()
        self._org_name = 'standa-novak'
        self._print_details = False

        self._load_secrets()

        # self._db = DBManager(self._db_pass)
        self._client = SQLiteClient(file_path="mydb.db", password=self._db_pass)
        self._gh_link = GitHubLink(self._org_name, self._gh_token)
        self._ssh = SSHManager()

        self.org_table = OrganizationHelper(self._client)
        self.repo_table = RepositoryHelper(self._client)
        self.team_table = TeamHelper(self._client)
        self.team_repo_table = TeamRepositoryHelper(self._client)
        self.user_table = UserHelper(self._client)
        self.key_table = KeyHelper(self._client)

        #self._load_org_info()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def load_org(self):
        # TODO : create system for checking current organization
        """
        1. gh_link check if org exists
        2. check if in db
        3. gh_link get org repos
        4. check if repos in db and not in gh
        5. gh_link get repo keys
        6. check if keys in db and not in db
        7. gh_link get org teams
        8. check if teams in db and not in gh
        9. gh_link get team repos
        10. check if team repos in db and not in gh
        11. gh_link get team users
        12. check if team users in db and not in gh
        """
        # Loading organization information, creates it if it doesn't exist
        org_id, org_object = self.org_table.get_or_create(self._org_name)

        # Get information about organization from GitHub
        # TODO : gh link need re-fragmenting, output unknown
        msg_type, msg = self._gh_link.get_org_info()

    def _load_org_info(self):
        # Checking data from GitHub about selected organization
        org_id, org_missing = self._check_org(self._org_name)
        self._added_check('Organization', self._org_name, org_missing)

        msg_type, msg = self._gh_link.get_org_info()

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
        not_in, table_len = self._db.db_table_check(table_name, [col], [org_name])

        if not_in:
            data = [org_name, 0]
            self._db.add_to_table(table_name, data)

            return table_len, not_in

        else:
            org_id = self._db.get_value(table_name, 'name', org_name, 'ID')

            return org_id, not_in

    def _check_repo(self, repo_name, org_id):
        # Checks if repository is in database, if not present, it is added and returns bool value
        col = 'name'
        table_name = 'repositories'
        not_in, table_len = self._db.db_table_check(table_name, [col], [repo_name])

        if not_in:
            data = [repo_name, org_id]
            self._db.add_to_table(table_name, data)

        return not_in

    def _check_team(self, team_name, org_id):
        col = 'name'
        table_name = 'teams'
        not_in, table_len = self._db.db_table_check(table_name, [col], [team_name])

        if not_in:
            data = [team_name, org_id]
            self._db.add_to_table(table_name, data)

            return table_len, not_in
        else:
            team_id = self._db.get_value('teams', col, team_name, 'ID')
            return team_id, not_in

    def _check_team_repos(self, team_name):
        resp_type, resp = self._gh_link.list_team_repos(team_name)
        team_id = self._db.get_value('teams', 'name', team_name, 'ID')
        table_name = 'teamRepos'

        team_repos_states = dict()

        if resp_type == 'ok':
            resp_code, team_repo_list = resp
            clean_team_repo_list = json.loads(team_repo_list)

            for repo in clean_team_repo_list:
                repo_name = repo['name']
                repo_id = self._db.get_value('repositories', 'name', repo_name, 'ID')
                role = self._gh_link.check_team_repo_permission(team_name, repo_name)[1][1]

                cols = ['name', 'repo_id', 'team_id']
                row_data = [repo_name,
                            repo_id,
                            team_id,
                            role]

                not_in, table_len = self._db.db_table_check(table_name, cols, row_data[:-1])

                if not_in:
                    self._db.add_to_table(table_name, row_data)

                team_repos_states[team_name] = not_in

        return team_repos_states

    def _check_team_members(self, team_name, team_id):
        msg_type, (msg_code, user_list) = self._gh_link.list_team_members(team_name)
        user_states = dict()
        clean_user_list = json.loads(user_list)

        for user in clean_user_list:
            data = [user['login'], team_id]
            not_in, table_len = self._db.db_table_check('users', ['name', 'team_id'], data)

            if not_in:
                self._db.add_to_table('users', data)

            user_states[user['login']] = not_in

        return user_states

    def _set_active_org(self, new_org):
        # TODO : create function for setting active org
        self._org_name = new_org

    def gen_ssh_key(self, key_name, repo_id=None, read_only=0):
        private_key, public_key = self._ssh.gen_ssh_key()

        data = [key_name, repo_id, private_key, public_key, read_only]

    def _added_check(self, unit, name, check_bool):
        if self._print_details:
            if check_bool:
                print(f'{name} was added to the database as {unit}.\n')
            else:
                print(f'{unit} "{name}" is in db.\n')

