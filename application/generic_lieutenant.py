from abc import ABC
from argparse import Namespace

from application.validators import Validator, Valid


def validate_inputs(**valid_kwargs):
    def func_wrap(func):
        def inner(*inner_args, **inner_kwargs):
            validator = inner_args[0].validator

            to_validate = valid_kwargs.get('to_validate')
            validated_list = list()

            validators = {
                Valid.REPO_EXISTS: lambda: validator.val_repo(True, **inner_kwargs),
                Valid.REPO_NOT_EXISTS: lambda: validator.val_repo(False, **inner_kwargs),

                Valid.TEAM_EXISTS: lambda: validator.val_team(True, **inner_kwargs),
                Valid.TEAM_NOT_EXISTS: lambda: validator.val_team(False, **inner_kwargs),

                Valid.TEAM_REPO_EXISTS: lambda: validator.val_team_repo(True, **inner_kwargs),
                Valid.TEAM_REPO_NOT_EXISTS: lambda: validator.val_team_repo(False, **inner_kwargs),

                Valid.USER_EXISTS: lambda: validator.val_user(True, **inner_kwargs),
                Valid.USER_NOT_EXISTS: lambda: validator.val_user(False, **inner_kwargs)
            }

            for cat in to_validate:
                if cat in validators:
                    cat_val = validators[cat]()
                    validated_list.append(cat_val)
                else:
                    raise NameError(f'(Validation type) Validation category "{cat}" was not found.')

            if all(validated_list):
                return func(*inner_args, **inner_kwargs)
            error_list = [to_validate[inx] for inx in range(len(validated_list)) if not validated_list[inx]]
            raise RuntimeError(f'(Validation type) Could not validate data for ' + ', '.join(error_list))

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

        self.validator = Validator(self._org_name, self._tables)

    def command_check(self, args: Namespace):
        kind = args.kind
        if kind == self.kind:
            verb = args.verb
            if verb is not None and hasattr(self, f"cmd_{verb}"):
                return getattr(self, f"cmd_{verb}")
        return None
