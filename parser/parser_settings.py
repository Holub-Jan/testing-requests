import argparse


class GHParser:
    def __init__(self):
        self._main_parser = argparse.ArgumentParser()

        self._load_settings()

    def _load_settings(self):
        kind_subparser = self._main_parser.add_subparsers(dest="kind")

        # System keywords
        kind_subparser.add_parser("exit")

        login_parser = kind_subparser.add_parser("login")
        login_parser.add_argument("--username", action='store', type=str)
        login_parser.add_argument("--password", action='store', type=str)

        # Repo keywords
        repo_parser = kind_subparser.add_parser("repo")
        repo_verb_subparser = repo_parser.add_subparsers(dest="verb")

        repo_verb_subparser.add_parser("list")

        repo_create_parser = repo_verb_subparser.add_parser("create")
        repo_create_parser.add_argument("name", action="store")

        repo_edit_parser = repo_verb_subparser.add_parser("edit")
        repo_edit_parser.add_argument("repo_name", action="store")
        repo_edit_parser.add_argument("--name", action='store', type=str)

        repo_delete_parser = repo_verb_subparser.add_parser("delete")
        repo_delete_parser.add_argument("repo_name", action="store")

        # Team keywords
        team_parser = kind_subparser.add_parser("team")
        team_verb_subparser = team_parser.add_subparsers(dest="verb")

        team_verb_subparser.add_parser("list")

        team_create_parser = team_verb_subparser.add_parser("create")
        team_create_parser.add_argument("name", action="store")

        team_delete_parser = team_verb_subparser.add_parser("delete")
        team_delete_parser.add_argument("team_name", action="store")

        team_edit_parser = team_verb_subparser.add_parser("edit")
        team_edit_parser.add_argument("team_name", action="store")
        team_edit_parser.add_argument("--name", action='store', type=str)

        team_link_parser = team_verb_subparser.add_parser("link")
        team_link_parser.add_argument("team_name", action="store")
        team_link_parser.add_argument("repo_name", action='store')
        team_link_parser.add_argument("--role", action='store', type=str)

        team_unlink_parser = team_verb_subparser.add_parser("unlink")
        team_unlink_parser.add_argument("team_name", action="store")
        team_unlink_parser.add_argument("repo_name", action='store')

        user_add_parser = team_verb_subparser.add_parser("user_add")
        user_add_parser.add_argument("team_name", action="store")
        user_add_parser.add_argument("--add", action='store', type=str)

        user_remove_parser = team_verb_subparser.add_parser("user_remove")
        user_remove_parser.add_argument("team_name", action="store")
        user_remove_parser.add_argument("--remove", action='store', type=str)

    def parse(self, args):
        return self._main_parser.parse_args(args)

