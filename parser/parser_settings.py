import argparse


class GHParser:
    def __init__(self):
        self._main_parser = argparse.ArgumentParser()

        self._load_settings()

    def _load_settings(self):
        kind_subparser = self._main_parser.add_subparsers(dest="kind")
        kind_subparser.add_parser("exit")
        repo_parser = kind_subparser.add_parser("repo")
        repo_verb_subparser = repo_parser.add_subparsers(dest="verb")

        repo_verb_subparser.add_parser("list")

        repo_create_parser = repo_verb_subparser.add_parser("create")
        repo_create_parser.add_argument("name", action="store")

        repo_edit_parser = repo_verb_subparser.add_parser("edit")
        repo_edit_parser.add_argument("old_name", action="store")
        repo_edit_parser.add_argument("--new_name", action='store', type=str)

        login_parser = kind_subparser.add_parser("login")
        login_parser.add_argument("--username", action='store', type=str)
        login_parser.add_argument("--password", action='store', type=str)

    def parse(self, args):
        return self._main_parser.parse_args(args)

