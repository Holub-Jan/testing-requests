from application.generic_lieutenant import GenericLieutenant
from helper.team_helper import TeamHelper
from storage import SQLiteClient


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

    def cmd_create(self, **kwargs):
        team_name = kwargs.get('name')
        org_id = self._org_table.get_id(self._org_name)

        if org_id is not None:
            team_obj = self._team_table.get_or_create(team_name, org_id)
            print(f'Team created: {team_obj}')
        else:
            print(f'Organization not found, couldnt create team {team_name}')

    def cmd_edit(self, **kwargs):
        team_name = kwargs.get('team_name')
        new_name = kwargs.get('name')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        if team_id is not None:
            team_obj = self._team_table.get_or_create(team_name, org_id)
            team_obj.name = new_name

            try:
                self._team_table.update_row_by_id(team_obj)
                print(f'Team name edited from {team_name} to {new_name}')
            except Exception as e:
                print(f'Error {e} occurred when updating team name from {team_name} to {new_name}')

        else:
            print(f'Team not found, couldnt edit team name from {team_name} to {new_name}')

    def cmd_delete(self, **kwargs):
        team_name = kwargs.get('team_name')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        if team_id is not None:
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

        else:
            print(f'Team not found, couldnt delete team: {team_name}')

    def cmd_link(self, **kwargs):
        team_name = kwargs.get('team_name')
        repo_name = kwargs.get('repo_name')
        role = kwargs.get('role')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_table.get_id(repo_name, org_id) if self._repo_table.exists(repo_query) else None

        if team_id is not None and repo_id is not None:
            self._team_repo_table.get_or_create(team_name, team_id, repo_id, role)
            print(f'Repository {repo_name} linked with {team_name} team.')

        else:
            print(f'Team or Repository not found, couldnt create a link')

    def cmd_unlink(self, **kwargs):
        team_name = kwargs.get('team_name')
        repo_name = kwargs.get('repo_name')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_table.get_id(repo_name, org_id) if self._repo_table.exists(repo_query) else None

        if team_id is not None:
            team_repo_query = [('team_id', team_id), ('repo_id', repo_id)]
            team_repo_role = self._team_repo_table.get_role(team_repo_query)
            team_repo_id = self._team_repo_table.get_id(repo_name, team_id, repo_id, team_repo_role) \
                if self._team_repo_table.exists(team_repo_query) else None

            if team_repo_id is not None:
                self._team_repo_table.delete_by_ids([team_repo_id])
                print(f'Repository {repo_name} unlinked from {team_name}')
            else:
                print(f'Team Repository {repo_name} was not found!')
        else:
            print(f'Team {team_name} was not found!')

    def cmd_user_add(self, **kwargs):
        team_name = kwargs.get('team_name')
        user_name = kwargs.get('add')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        user_query = [('name', user_name), ('team_id', team_id)]
        user_exists = self._user_table.exists(user_query)

        if not user_exists:
            if team_id is not None:
                self._user_table.get_or_create(user_name, team_id)
                print(f'User {user_name} added to {team_name}')
            else:
                print(f'Team not found, couldnt add the user {user_name}')

        else:
            print(f'User {user_name} does not exist!')

    def cmd_user_remove(self, **kwargs):
        team_name = kwargs.get('team_name')
        user_name = kwargs.get('remove')

        org_id = self._org_table.get_id(self._org_name)

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_table.get_id(team_name, org_id) if self._team_table.exists(team_query) else None

        user_query = [('name', user_name), ('team_id', team_id)]
        user_id = self._user_table.get_id(user_name, team_id) if self._user_table.exists(user_query) else None

        if user_id is not None:
            self._user_table.delete_by_ids([user_id])
            print(f'User {user_name} was removed from the team {team_name}')
        else:
            print(f'User {user_name} not found')

    def _remove_team_users(self, users):
        pass

    def _remove_team_repos(self, repos):
        pass
