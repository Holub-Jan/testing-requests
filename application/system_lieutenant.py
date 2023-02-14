from argparse import Namespace

from api.github_link import GitHubLink
from application.generic_lieutenant import GenericLieutenant


class SystemLieutenant(GenericLieutenant):
    # TODO : not complete
    def __init__(self, gh_token):
        super().__init__(org_name='', tables={})
        self._gh_link = GitHubLink(self._org_name, gh_token)
        self.logged_bool = False

    def cmd_login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        # temporary, users can be saved in db, and set as active
        if not self.logged_bool:
            pass_list = self._open_login_info()
            if username in pass_list.keys() and password == pass_list[username]['password']:
                print(f'!Logged in as {username}!')
                self.logged_bool = True
                return pass_list[username]['organization']
        print('User already logged in, please logout first.')

    def cmd_logout(self):
        self.logged_bool = False

    def cmd_status(self):
        # Command : 'status', checking if connection is made
        self._gh_link.check_status()

    def cmd_reconcile(self):
        pass

    @staticmethod
    def cmd_exit():
        exit()

    @staticmethod
    def _open_login_info() -> dict:
        passwords = dict()

        with open("../users.txt", "r") as f:
            for row in f:
                row = row.replace('\n', '').split(' ')
                passwords[row[0]] = {'password': row[1], 'organization': row[2]}

        return passwords

    def command_check(self, args: Namespace):
        kind = args.kind
        if hasattr(self, f"cmd_{kind}"):
            return getattr(self, f"cmd_{kind}")
        return None
