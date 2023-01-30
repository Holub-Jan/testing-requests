from application.generic_lieutenant import GenericLieutenant
from helper.repo_helper import RepositoryHelper
from storage import SQLiteClient


class RepoLieutenant(GenericLieutenant):
    # TODO : Create more pleasing way of printing messages?
    def __init__(self, org_name: str, table: RepositoryHelper):
        super().__init__(org_name, table)
        self.kind = 'repo'

    def cmd_list(self):
        org_id = self._org_id()
        repo_list = self._table.get_details(org_id).repositories
        print(repo_list) # todo

    def cmd_create(self, repo_name: str):
        org_id = self._org_id()
        if org_id:
            repo_obj = self._table.get_or_create(repo_name, org_id)
            print(f'Repository created: {repo_obj}')
        else:
            print(f'Organization not found, couldnt create repository: {repo_name}')

    def cmd_edit(self, repo_name: str, new_name: str):
        org_id = self._org_id()
        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_id(repo_name) if self._table.exists([repo_query]) else False

        if repo_id:
            repo_obj = self._table.get_or_create(repo_name, org_id)
            repo_obj.name = new_name

            try:
                self._table.update_row_by_id(repo_obj)
                print(f'Repository name changed to {new_name}')
            except Exception as e:
                print(f'Error {e} occurred when updating repository name from {repo_name} to {new_name}')

        else:
            print(f'Repository not found, couldnt edit repository name to {new_name}')

    def cmd_delete(self, repo_name: str):
        org_id = self._org_id()
        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_id(repo_name) if self._table.exists([repo_query]) else False

        if repo_id:
            self._table.delete_by_ids([repo_id])
            print(f'Repository {repo_name} deleted')
        else:
            print('Repository not found')
