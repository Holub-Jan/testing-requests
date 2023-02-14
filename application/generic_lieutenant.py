from abc import ABC
from argparse import Namespace

from application.validators import Validator


class GenericLieutenant(ABC):
    def __init__(self, org_name: str, tables):
        self._org_name = org_name
        self._tables = tables
        self.kind = None

        self._org_table = self._tables.get('org')
        self._team_table = self._tables.get('team')
        self._repo_table = self._tables.get('repo')
        self._team_repo_table = self._tables.get('team_repo')
        self._user_table = self._tables.get('user')

        self._validator = Validator(self._tables)

    def command_check(self, args: Namespace):
        kind = args.kind
        if kind == self.kind:
            verb = args.verb
            if verb is not None and hasattr(self, f"cmd_{verb}"):
                return getattr(self, f"cmd_{verb}")
        return None
