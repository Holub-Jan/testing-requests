from application.generic_lieutenant import GenericLieutenant, validate_inputs
from validators import Validator


class RepoLieutenant(GenericLieutenant):
    def __init__(self, org_name: str, tables):
        super().__init__(org_name, tables)
        self.kind = 'repo'
        self._org_name = org_name

    def cmd_list(self):
        org_id = self._org_table.get_id(self._org_name)
        repo_list = self._org_table.get_details(org_id).repositories
        print(f'Repositories for organization {self._org_name}:')
        for repo in repo_list:
            print(repo)

    @validate_inputs(to_validate=['repo_not_exist'])
    def cmd_create(self, **kwargs):
        repo_name = kwargs.get('name')

        org_id = self._org_table.get_id(self._org_name)

        if org_id is not None:
            repo_obj = self._repo_table.get_or_create(repo_name, org_id)
            print(f'Repository created: {repo_obj}')
        else:
            print(f'Organization not found, couldnt create repository: {repo_name}')

    @validate_inputs(to_validate=['repo_exists', 'repo_not_exist'])
    def cmd_edit(self, **kwargs):
        repo_name = kwargs.get('repo_name')
        new_name = kwargs.get('name')

        org_id = self._org_table.get_id(self._org_name)

        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_table.get_id(repo_name, org_id) if self._repo_table.exists(repo_query) else None

        if repo_id is not None:
            repo_obj = self._repo_table.get_or_create(repo_name, org_id)[0]
            repo_obj.name = new_name

            try:
                self._repo_table.update_row_by_id(repo_obj)
                print(f'Repository name changed to {new_name}')
            except Exception as e:
                print(f'Error {e} occurred when updating repository name from {repo_name} to {new_name}')

        else:
            print(f'Repository not found, couldnt edit repository name to {new_name}')

    @validate_inputs(to_validate=['repo_exists'])
    def cmd_delete(self, **kwargs):
        repo_name = kwargs.get('repo_name')

        org_id = self._org_table.get_id(self._org_name)
        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_table.get_id(repo_name, org_id) if self._repo_table.exists(repo_query) else None

        if repo_id is not None:
            self._repo_table.delete_by_ids([repo_id])
            print(f'Repository {repo_name} deleted')
        else:
            print('Repository not found')
