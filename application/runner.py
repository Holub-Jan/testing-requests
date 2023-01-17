from api.github_link import GitHubLink
from application.repo_lieutenant import RepoLieutenant
from application.ssh_manager import SSHManager
from application.team_lieutenant import TeamLieutenant

from storage import SQLiteClient
from parser.cat_arg_parse import CatArgParse


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
        self._repo_lieutenant = RepoLieutenant(self._client, self._org_name)
        self._team_lieutenant = TeamLieutenant(self._client, self._org_name)
        self._arg_parse = CatArgParse()

        self._load_args()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]

    def command_loop(self):
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
                self._arg_parse.get_help()
            else:
                command_list = command.split()
                parsed = self._arg_parse.return_cats(command_list)
                print(parsed)

    def login(self, username, password):
        # TODO : temporary, users can be saved in db, and set as active
        pass_list = self._open_login_info()
        if username in pass_list.keys() and password == pass_list[username]['password']:
            print(f'!Logged in as {username}!')
            return pass_list[username]['organization']

    def c_status(self):
        # Command : 'status', checking if connection is made
        self._gh_link.check_status()

    def _load_args(self):
        self._arg_parse.edit_or_add_category(cat_key='logout', inputs=0)
        self._arg_parse.edit_or_add_category(cat_key='repo', inputs=0)
        self._arg_parse.edit_or_add_category(cat_key='list', inputs=0, parent='repo')
        self._arg_parse.edit_or_add_category(cat_key='create', inputs=1, parent='repo')
        self._arg_parse.edit_or_add_category(cat_key='edit', inputs=1, parent='repo')
        self._arg_parse.edit_or_add_category(cat_key='delete', inputs=1, parent='repo')
        self._arg_parse.edit_or_add_category(cat_key='name', inputs=1, parent='edit')

    @staticmethod
    def _open_login_info() -> dict:
        passwords = dict()

        with open("../users.txt", "r") as f:
            for row in f:
                row = row.replace('\n', '').split(' ')
                passwords[row[0]] = {'password': row[1], 'organization': row[2]}

        return passwords
