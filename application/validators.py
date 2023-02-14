class Validator:
    def __init__(self, tables):
        self._tables = tables

        self._team_table = self._tables.get('team')
        self._repo_table = self._tables.get('repo')
        self._user_table = self._tables.get('user')

        self._error_bool = False

    def validate(self, func):
        def inner(*inner_args, **inner_kwargs):
            print("(validator ran)")

            team_name = inner_kwargs.get('team_name')

            if team_name is not None:
                team_query = [('name', team_name)]

                team_objs = self._team_table.exists(team_query)

                if not team_objs:
                    print('Team name was not found in db.')
                    self._error_bool = True

                else:
                    team_id = team_objs[0].id_
                    add_name = inner_kwargs.get('add')
                    self._add_name(add_name, team_id)

                    remove_name = inner_kwargs.get('remove')
                    self._remove_name(remove_name, team_id)

            repo_name = inner_kwargs.get('repo_name')
            self._repo_name(repo_name)

            if self._error_bool:
                return

            return func(*inner_args, **inner_kwargs)

        return inner

    def _repo_name(self, repo_name):
        if repo_name is not None:
            repo_query = [('name', repo_name)]

            if not self._repo_table.exists(repo_query):
                print('Repository name was not found in db.')
                self._error_bool = True

    def _add_name(self, add_name, team_id):
        if add_name is not None:
            add_query = [('name', add_name), ('team_id', team_id)]

            if self._user_table.exists(add_query):
                print('User name is already in the db.')
                self._error_bool = True

    def _remove_name(self, remove_name, team_id):
        if remove_name is not None:
            remove_query = [('name', remove_name), ('team_id', team_id)]

            if not self._user_table.exists(remove_query):
                print('User name is already in the db.')
                self._error_bool = True
