from abc import ABC
from argparse import Namespace


class GenericLieutenant(ABC):
    def __init__(self, org_name: str, table):
        self._org_name = org_name
        self._table = table
        self.kind = None

    def command_check(self, args: Namespace):
        kind = args.kind
        if kind == self.kind:
            verb = args.verb
            if hasattr(self, f"cmd_{verb}"):
                return 1

        return 0
