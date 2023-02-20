class Valid:
    REPO_EXISTS = 'repo_exists'
    REPO_NOT_EXISTS = 'repo_not_exists'

    TEAM_EXISTS = 'team_exists'
    TEAM_NOT_EXISTS = 'team_not_exists'

    TEAM_REPO_EXISTS = 'team_repo_exists'
    TEAM_REPO_NOT_EXISTS = 'team_repo_not_exists'

    USER_EXISTS = 'user_exists'
    USER_NOT_EXISTS = 'user_not_exists'


class Validator:
    def __init__(self, org_name, tables):
        self._tables = tables
        self._org_name = org_name

        self._org_table = self._tables.get('org')
        self._team_table = self._tables.get('team')
        self._repo_table = self._tables.get('repo')
        self._team_repo_table = self._tables.get('team_repo')
        self._user_table = self._tables.get('user')

        self._error_bool = False

    def val_repo(self, check_exists: bool,  **kwargs):
        if check_exists:
            repo_name = kwargs.get('repo_name')
        else:
            repo_name = kwargs.get('name')

        if repo_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', repo_name), ('org_id', org_id)]
            exists = self._repo_table.exists(query)

            if exists == check_exists:
                return True

            print(f'Repository "{repo_name}" already exist.') if exists \
                else print(f'Repository "{repo_name}" does not exist.')
            return False

        print('!! repo_name is argument missing (check validator assignment) !!')
        return False

    def val_team(self, check_exists: bool, **kwargs):
        if check_exists:
            team_name = kwargs.get('team_name')
        else:
            team_name = kwargs.get('name')

        if team_name is not None:
            org_id = self._org_table.get_id(self._org_name)
            query = [('name', team_name), ('org_id', org_id)]
            exists = self._team_table.exists(query)

            if exists == check_exists:
                return True

            print(f'Team "{team_name}" already exist.') if exists \
                else print(f'Team "{team_name}" does not exist.')
            return False

        print('!! team_name is argument missing (check validator assignment) !!')
        return False

    def val_team_repo(self, check_exists: bool, **kwargs):
        repo_name = kwargs.get('repo_name')
        team_name = kwargs.get('team_name')

        if None not in [repo_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            repo_id = self._repo_table.get_id(repo_name, org_id) \
                if self.val_repo(True, repo_name=repo_name) else None
            team_id = self._team_table.get_id(team_name, org_id) \
                if self.val_team(True, team_name=team_name) else None

            if None not in [repo_id, team_id]:
                query = [('team_id', team_id), ('repo_id', repo_id)]
                exists = self._team_repo_table.exists(query)

                if exists == check_exists:
                    return True

                print(f'Repository "{repo_name}" and team "{team_name}" are already linked.') if exists \
                    else print(f'Repository "{repo_name}" and team "{team_name}" are not linked.')
                return False

        print('!! repo_name and/or team_name arguments are missing (check validator assignment) !!')
        return False

    def val_user(self, check_exists: bool, **kwargs):
        if check_exists:
            user_name = kwargs.get('remove')
        else:
            user_name = kwargs.get('add')
        team_name = kwargs.get('team_name')

        if None not in [user_name, team_name]:
            org_id = self._org_table.get_id(self._org_name)
            team_id = self._team_table.get_id(team_name, org_id) \
                if self.val_team(True, team_name=team_name) else None

            if team_id is not None:
                query = [('team_id', team_id), ('name', user_name)]
                exists = self._user_table.exists(query)

                if exists == check_exists:
                    return True

                print(f'User "{user_name}" already exists.') if exists \
                    else print(f'User "{user_name}" does not exists.')
                return False

        print('!! user name and/or team_name arguments are missing (check validator assignment) !!')
        return False
