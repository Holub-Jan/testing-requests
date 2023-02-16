from application.generic_lieutenant import GenericLieutenant, validate_inputs


class TeamLieutenant(GenericLieutenant):
    def __init__(self, org_name: str, tables):
        super().__init__(org_name, tables)
        self.kind = 'team'

    def cmd_list(self):
        org_id = self._org_table.get_id(self._org_name)
        team_list = self._org_table.get_details(org_id).teams

        for team in team_list:
            repos = self._team_table.get_details(team.name, team.id_).repositories
            rep_lst = list()
            for repo in repos:
                repo_name = self._repo_table.get_name(repo.repo_id)
                rep_lst.append(f'Repo name: {repo_name}')

            users = self._team_table.get_details(team.name, team.id_).users
            user_lst = list()
            for user in users:
                user_name = self._user_table.get_name(user.id_, user.team_id)
                user_lst.append(f'User name: {user_name}')

            print(team, rep_lst, user_lst)

    @validate_inputs(to_validate=['team_not_exist'])
    def cmd_create(self, **kwargs):
        team_name = kwargs.get('name')
        org_id = self._org_table.get_id(self._org_name)

        team_obj = self._team_table.get_or_create(team_name, org_id)
        print(f'Team created: {team_obj}')

    @validate_inputs(to_validate=['team_exists', 'team_not_exist'])
    def cmd_edit(self, **kwargs):
        team_name = kwargs.get('team_name')
        new_name = kwargs.get('name')

        org_id = self._org_table.get_id(self._org_name)

        team_obj = self._team_table.get_or_create(team_name, org_id)
        team_obj.name = new_name
        self._team_table.update_row_by_id(team_obj)

    @validate_inputs(to_validate=['team_exists'])
    def cmd_delete(self, **kwargs):
        team_name = kwargs.get('team_name')

        org_id = self._org_table.get_id(self._org_name)
        team_id = self._team_table.get_id(team_name, org_id)

        repos = self._team_table.get_details(team_name, team_id).repositories
        team_repos_lst = list()
        for repo in repos:
            repo_id = self._repo_table.get_id(repo.name, org_id)
            team_repo_id = self._team_repo_table.get_id(team_id, repo_id)
            team_repos_lst.append(team_repo_id)

        users = self._team_table.get_details(team_name, team_id).users
        user_lst = list()
        for user in users:
            user_id = self._user_table.get_id(user.name, team_id)
            user_lst.append(user_id)

        self._team_repo_table.delete_by_ids(team_repos_lst)
        # todo: also ssh keys remove once implemented
        self._user_table.delete_by_ids(user_lst)
        self._team_table.delete_by_ids([team_id])
        print(f'Team deleted: {team_name}')

    @validate_inputs(to_validate=['team_exists', 'repo_exists', 'team_repo_not_exist'])
    def cmd_link(self, **kwargs):
        team_name = kwargs.get('team_name')
        repo_name = kwargs.get('repo_name')
        role = kwargs.get('role')

        org_id = self._org_table.get_id(self._org_name)
        team_id = self._team_table.get_id(team_name, org_id)
        repo_id = self._repo_table.get_id(repo_name, org_id)

        self._team_repo_table.get_or_create(team_name, team_id, repo_id, role)
        print(f'Repository {repo_name} linked with {team_name} team.')

    @validate_inputs(to_validate=['team_exists', 'repo_exists', 'team_repo_exists'])
    def cmd_unlink(self, **kwargs):
        team_name = kwargs.get('team_name')
        repo_name = kwargs.get('repo_name')

        org_id = self._org_table.get_id(self._org_name)
        team_id = self._team_table.get_id(team_name, org_id)
        repo_id = self._repo_table.get_id(repo_name, org_id)

        team_repo_query = [('team_id', team_id), ('repo_id', repo_id)]
        team_repo_role = self._team_repo_table.get_role(team_repo_query)
        team_repo_id = self._team_repo_table.get_id(repo_name, team_id, repo_id, team_repo_role)

        self._team_repo_table.delete_by_ids([team_repo_id])
        print(f'Repository {repo_name} unlinked from {team_name}')

    @validate_inputs(to_validate=['team_exists', 'user_not_exist'])
    def cmd_user_add(self, **kwargs):
        team_name = kwargs.get('team_name')
        user_name = kwargs.get('add')

        org_id = self._org_table.get_id(self._org_name)
        team_id = self._team_table.get_id(team_name, org_id)

        self._user_table.get_or_create(user_name, team_id)
        print(f'User {user_name} added to {team_name}')

    @validate_inputs(to_validate=['team_exists', 'user_exists'])
    def cmd_user_remove(self, **kwargs):
        team_name = kwargs.get('team_name')
        user_name = kwargs.get('remove')

        org_id = self._org_table.get_id(self._org_name)
        team_id = self._team_table.get_id(team_name, org_id)
        user_id = self._user_table.get_id(user_name, team_id)

        self._user_table.delete_by_ids([user_id])
        print(f'User {user_name} was removed from the team {team_name}')
