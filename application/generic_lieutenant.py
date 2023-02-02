from abc import ABC
from argparse import Namespace

from helper.generic_helper import GenericHelper


def hello(func):
    def inner(*inner_args, **inner_kwargs):
        print("Hello")
        return func(*inner_args, **inner_kwargs)
    return inner


class GenericLieutenant(ABC):
    def __init__(self, org_name: str, tables):
        self._org_name = org_name
        self._tables = tables
        self.kind = None

    def command_check(self, args: Namespace):
        kind = args.kind
        if kind == self.kind:
            verb = args.verb
            # TODO : if verb is none musime vratit none a neco s tim udelat dal
            if hasattr(self, f"cmd_{verb}"):
                return getattr(self, f"cmd_{verb}")
        return None
