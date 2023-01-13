from application.generic_lieutenant import GenericLieutenant
from storage import SQLiteClient


class RepoLieutenant(GenericLieutenant):
    # TODO : Create more pleasing way of printing messages?
    def __init__(self, client: SQLiteClient, org_name: str):
        super().__init__(client, org_name)

    def list(self):
        org_id = self._org_id()
        repo_list = self.org_table.get_details(org_id).repositories
        print(repo_list)

    def create(self, repo_name: str):
        org_id = self._org_id()
        if org_id:
            repo_obj = self.repo_table.get_or_create(repo_name, org_id)
            print(f'Repository created: {repo_obj}')
        else:
            print(f'Organization not found, couldnt create repository: {repo_name}')

    def edit(self, repo_name: str, new_name: str):
        org_id = self._org_id()
        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_id(repo_name) if self.repo_table.exists([repo_query]) else False

        if repo_id:
            repo_obj = self.repo_table.get_or_create(repo_name, org_id)
            repo_obj.name = new_name

            try:
                self.repo_table.update_row_by_id(repo_obj)
                print(f'Repository name changed to {new_name}')
            except Exception as e:
                print(f'Error {e} occurred when updating repository name from {repo_name} to {new_name}')

        else:
            print(f'Repository not found, couldnt edit repository name to {new_name}')

    def delete(self, repo_name: str):
        org_id = self._org_id()
        repo_query = [('name', repo_name), ('org_id', org_id)]
        repo_id = self._repo_id(repo_name) if self.repo_table.exists([repo_query]) else False

        if repo_id:
            self.repo_table.delete_by_ids([repo_id])
            print(f'Repository {repo_name} deleted')
        else:
            print('Repository not found')
