from api.github_link import GitHubLink
from application.ssh_manager import SSHManager
from helper.key_helper import KeyHelper
from helper.org_helper import OrganizationHelper
from helper.repo_helper import RepositoryHelper
from helper.team_helper import TeamHelper
from helper.team_repo_helper import TeamRepositoryHelper
from helper.user_helper import UserHelper
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

        self._client = SQLiteClient(file_path="mydb.db", password=self._db_pass)
        self._gh_link = GitHubLink(self._org_name, self._gh_token)
        self._ssh = SSHManager()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def command_loop(self):
        c_options = {'logout': 1,
                     'status': 2,
                     'repo':
                         {'list': 3,
                          'create': 4,
                          'edit':
                              {'name': 5},
                          'delete': 6},
                     'team':
                         {'create': 7,
                          'edit':
                              {'name': 8},
                          'delete': 9,
                          'link':
                              {'role': 10},
                          'unlink': 11,
                          'user':
                              {'add': 12,
                               'remove': 13}},
                     'ssh':
                         {'generate': 14,
                          'show': 15,
                          'link':
                              {'repo': 16}},
                     'reconcile': 17}
        logging = True
        while logging:
            command = input('Input username and password: ')
            user_name = command.split()[0]
            password = command.split()[1]
            org = self.login(user_name, password)
            if org:
                logging = False

        logged_in = True
        while logged_in:
            command = input()
            if 'help' in command:
                print(c_options)

    def login(self, username, password):
        # TODO : temporary, users can be saved in db, and set as active
        pass_list = self._open_login_info()
        if username in pass_list.keys() and password == pass_list[username]['password']:
            print(f'!Logged in as {username}!')
            return pass_list[username]['organization']

    def c_status(self):
        # Command : 'status', checking if connection is made
        self._gh_link.check_status()

    @staticmethod
    def _open_login_info() -> dict:
        passwords = dict()

        with open("../users.txt", "r") as f:
            for row in f:
                row = row.replace('\n', '').split(' ')
                passwords[row[0]] = {'password': row[1], 'organization': row[2]}

        return passwords
