from abc import ABC
from argparse import Namespace

from helper.generic_helper import GenericHelper


class GenericLieutenant(ABC):
    def __init__(self, org_name: str, tables):
        self._org_name = org_name
        self._tables = tables
        self.kind = None

    def command_check(self, args: Namespace):
        kind = args.kind
        if kind == self.kind:
            verb = args.verb
            if hasattr(self, f"cmd_{verb}"):
                return getattr(self, f"cmd_{verb}")
        return None
