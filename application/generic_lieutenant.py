from abc import ABC
from argparse import Namespace

from application.validators import Validator


def validate_inputs(**valid_kwargs):
    def func_wrap(func):
        def inner(*inner_args, **inner_kwargs):
            self = inner_args[0]

            to_validate = valid_kwargs.get('to_validate')
            validated_list = list()

            for cat in to_validate:
                if hasattr(self, f"val_{cat}"):
                    cat_val = getattr(self, f"val_{cat}")(**inner_kwargs)
                    validated_list.append(cat_val)
                else:
                    raise NameError(f'(Validation type) Validation category "{cat}" was not found.')

            if min(validated_list):
                return func(*inner_args, **inner_kwargs)
            error_list = [to_validate[inx] for inx in range(len(validated_list)) if not validated_list[inx]]
            raise NameError(f'(Validation type) Could not validate data for ', ', '.join(error_list))

        return inner
    return func_wrap


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

    def val_repo_exists(self, **kwargs):
        repo_name = kwargs.get('repo_name')

        if repo_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', repo_name), ('org_id', org_id)]
            exists = self._repo_table.exists(query)

            if exists:
                return True

            print(f'Repository "{repo_name}" does not exist.')

        print('!! repo_name is argument missing (check validator assignment) !!')
        return False

    def val_repo_not_exist(self, **kwargs):
        repo_name = kwargs.get('name')

        if repo_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', repo_name), ('org_id', org_id)]
            exists = self._repo_table.exists(query)

            if not exists:
                return True

            print(f'Repository "{repo_name}" exists.')
            return False

        print('!! repo_name is argument missing (check validator assignment) !!')
        return False

    def val_team_exists(self, **kwargs):
        team_name = kwargs.get('team_name')

        if team_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', team_name), ('org_id', org_id)]
            exists = self._team_table.exists(query)

            if exists:
                return True

            print(f'Team "{team_name}" does not exist.')

        print('!! team_name is argument missing (check validator assignment) !!')
        return False

    def val_team_not_exist(self, **kwargs):
        team_name = kwargs.get('name')

        if team_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', team_name), ('org_id', org_id)]
            exists = self._team_table.exists(query)

            if not exists:
                return True

            print(f'Team "{team_name}" exists.')
            return False

        print('!! team_name is argument missing (check validator assignment) !!')
        return False

    def val_team_repo_exists(self, **kwargs):
        repo_name = kwargs.get('repo_name')
        team_name = kwargs.get('team_name')

        if None not in [repo_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            repo_id = self._repo_table.get_id(repo_name, org_id) if self.val_repo_exists(repo_name=repo_name) else None
            team_id = self._team_table.get_id(team_name, org_id) if self.val_team_exists(team_name=team_name) else None

            if None not in [repo_id, team_id]:
                query = [('team_id', team_id), ('repo_id', repo_id)]
                exists = self._team_repo_table.exists(query)

                if exists:
                    return True

                print(f'Repository "{repo_name}" and team "{team_name}" are not linked.')
                return False

        print('!! repo_name and/or team_name arguments are missing (check validator assignment) !!')
        return False

    def val_team_repo_not_exist(self, **kwargs):
        repo_name = kwargs.get('repo_name')
        team_name = kwargs.get('team_name')

        if None not in [repo_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            repo_id = self._repo_table.get_id(repo_name, org_id) if self.val_repo_exists(repo_name=repo_name) else None
            team_id = self._team_table.get_id(team_name, org_id) if self.val_team_exists(team_name=team_name) else None

            if None not in [repo_id, team_id]:
                query = [('team_id', team_id), ('repo_id', repo_id)]
                exists = self._team_repo_table.exists(query)

                if not exists:
                    return True

                print(f'Repository "{repo_name}" and team "{team_name}" are linked currently.')
                return False

        print('!! repo_name and/or team_name arguments are missing (check validator assignment) !!')
        return False

    def val_user_exists(self, **kwargs):
        remove_name = kwargs.get('remove')
        team_name = kwargs.get('team_name')

        if None not in [remove_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            team_id = self._team_table.get_id(team_name, org_id) if self.val_team_exists(team_name=team_name) else None

            if team_id is not None:
                query = [('team_id', team_id), ('name', remove_name)]
                exists = self._team_repo_table.exists(query)

                if exists:
                    return True

                print(f'User "{remove_name}" does not exist.')
                return False

        print('!! remove and/or team_name arguments are missing (check validator assignment) !!')
        return False

    def val_user_not_exist(self, **kwargs):
        add_name = kwargs.get('add')
        team_name = kwargs.get('team_name')

        if None not in [add_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            team_id = self._team_table.get_id(team_name, org_id) if self.val_team_exists(team_name=team_name) else None

            if team_id is not None:
                query = [('team_id', team_id), ('name', add_name)]
                exists = self._team_repo_table.exists(query)

                if not exists:
                    return True

                print(f'User "{add_name}" exists currently.')
                return False

        print('!! add and/or team_name arguments are missing (check validator assignment) !!')
        return False
