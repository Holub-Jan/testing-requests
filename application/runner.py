from argparse import Namespace

from application.repo_lieutenant import RepoLieutenant
from application.ssh_manager import SSHManager
from application.system_lieutenant import SystemLieutenant
from application.team_lieutenant import TeamLieutenant
from helper.repo_helper import RepositoryHelper
from helper.team_helper import TeamHelper
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
        self._repo_helper = RepositoryHelper(self._client)
        self._repo_lieutenant = RepoLieutenant(self._org_name, self._repo_helper)
        self._team_helper = TeamHelper(self._client)
        self._team_lieutenant = TeamLieutenant(self._org_name, self._team_helper)
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
            checks = [lieutenant.command_check(par)
                      for lieutenant in [self._system_lieutenant, self._repo_lieutenant, self._team_lieutenant]]
            print(checks)

    def checker(self, args: Namespace):
        # TODO
        pass
