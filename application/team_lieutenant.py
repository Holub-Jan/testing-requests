from application.generic_lieutenant import GenericLieutenant
from storage import SQLiteClient


class TeamLieutenant(GenericLieutenant):
    # TODO : Create more pleasing way of printing messages?
    def __init__(self, client: SQLiteClient, org_name: str):
        super().__init__(client, org_name)

    def list(self):
        org_id = self._org_id()
        team_list = self.org_table.get_details(org_id).teams
        print(team_list)

    def create(self, team_name: str):
        org_id = self._org_id()
        if org_id:
            team_obj = self.team_table.get_or_create(team_name, org_id)
            print(f'Team created: {team_obj}')
        else:
            print(f'Organization not found, couldnt create team {team_name}')

    def edit(self, team_name: str, new_name: str):
        org_id = self._org_id()
        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        if team_id:
            team_obj = self.team_table.get_or_create(team_name, org_id)
            team_obj.name = new_name

            try:
                self.team_table.update_row_by_id(team_obj)
                print(f'Team name edited from {team_name} to {new_name}')
            except Exception as e:
                print(f'Error {e} occurred when updating team name from {team_name} to {new_name}')

        else:
            print(f'Team not found, couldnt edit team name from {team_name} to {new_name}')

    def delete(self, team_name: str):
        org_id = self._org_id()
        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        if team_id:
            self.team_table.delete_by_ids([team_id])
            print(f'Repository deleted: {team_name}')
        else:
            print(f'Team not found, couldnt delete team: {team_name}')

    def link(self, team_name: str, repo_name: str, role: str):
        # TODO : create team linking func
        org_id = self._org_id()

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_id(repo_name) if self.repo_table.exists([repo_query]) else False

        if team_id and repo_id:
            self.team_repo_table.get_or_create(f'{repo_name}', team_id, org_id, role)
            print(f'Repository {repo_name} linked with {team_name} team.')

        else:
            print(f'Team or Repository not found, couldnt create a link')

    def unlink(self, team_name, repo_name):
        org_id = self._org_id()

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        team_repo_query = [('name', repo_name), ('team_id', team_id), ('org_id', org_id)]
        team_repo_role = self.team_repo_table.get_role(team_repo_query)
        team_repo_id = self._team_repo_id(repo_name, team_id, org_id, team_repo_role) \
            if self.team_repo_table.exists([team_repo_query]) else False

        if team_repo_id:
            self.team_table.delete_by_ids([team_repo_id])
            print(f'Repository {repo_name} unlinked from {team_name}')
        else:
            print(f'Team or Repository not found, couldnt proceed')

    def user_add(self, team_name, user_name):
        org_id = self._org_id()

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        if team_id:
            self.user_table.get_or_create(user_name, team_id)
            print(f'User {user_name} added to {team_name}')
        else:
            print(f'Team not found, couldnt add the user {user_name}')

    def user_remove(self, team_name, user_name):
        org_id = self._org_id()

        team_query = [('name', team_name), ('org_id', org_id)]
        team_id = self._team_id(team_name) if self.team_table.exists([team_query]) else False

        user_query = [('name', user_name), ('team_id', team_id)]
        user_id = self._user_id(user_name, team_id) if self.user_table.exists([user_query]) else False

        if user_id:
            self.user_table.delete_by_ids([user_id])
            print(f'User {user_name} was removed from the team {team_name}')
        else:
            print(f'User {user_name} not found')
