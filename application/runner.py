from argparse import Namespace

from application.repo_lieutenant import RepoLieutenant
from application.ssh_manager import SSHManager
from application.system_lieutenant import SystemLieutenant
from application.team_lieutenant import TeamLieutenant
from helper import OrganizationHelper
from helper.key_helper import KeyHelper
from helper.repo_helper import RepositoryHelper
from helper.team_helper import TeamHelper
from helper.team_repo_helper import TeamRepositoryHelper
from helper.user_helper import UserHelper
from parser.parser_settings import GHParser

from storage import SQLiteClient


class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()
        self._org_name = 'standa-novak'
        self._print_details = False

        self._load_secrets()

        self._client = SQLiteClient(file_path="mydb.db", password=self._db_pass)
        self._ssh = SSHManager()
        self._helpers = {
            'org': OrganizationHelper(self._client),
            'team': TeamHelper(self._client),
            'repo': RepositoryHelper(self._client),
            'team_repo': TeamRepositoryHelper(self._client),
            'user': UserHelper(self._client),
            'key': KeyHelper(self._client)
        }
        self._repo_lieutenant = RepoLieutenant(self._org_name, self._helpers)
        self._team_lieutenant = TeamLieutenant(self._org_name, self._helpers)
        self._system_lieutenant = SystemLieutenant(self._gh_token)
        self._parser = GHParser()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def command_loop(self):
        while True:
            input_ = input('Command: ').split()
            par = self._parser.parse(input_)
            checks = self.checker(par)
            checks = [c for c in checks if c is not None]
            print(par)
            if checks:
                checks[0](**par.__dict__)
            print()

    def checker(self, args: Namespace):
        return [lieutenant.command_check(args)
                for lieutenant in [self._system_lieutenant, self._repo_lieutenant, self._team_lieutenant]]
