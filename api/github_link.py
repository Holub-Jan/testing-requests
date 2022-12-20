import json

import requests


class GitHubLink:

    def __init__(self, org_name, token):
        self.org_name = org_name
        self.token = token

        # TODO : remove slash, add it elsewhere
        self.url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github+json'}

        self._load_token()

    def list_repos(self):
        url = f'{self.url}orgs/{self.org_name}/repos'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def create_repo(self, data):
        url = f'{self.url}orgs/{self.org_name}/repos'
        response = requests.post(url, headers=self.headers, json=data)

        return self._eval_response(response)

    def rename_repo(self, old_name, new_name):
        data = {'name': new_name}
        url = f'{self.url}repos/{self.org_name}/{old_name}'
        response = requests.patch(url, headers=self.headers, json=data)

        return self._eval_response(response)

    def delete_repo(self):
        response = requests.delete(self.url, headers=self.headers)

        return response

    def _load_token(self):
        self.headers['Authorization'] = f'Bearer {self.token}'

    def check_status(self):
        check = self.list_repos()
        if self.org_name != '':
            if check[0] == 'ok':
                print('Organization exists and connection was made.')
            else:
                print(f'Status code: {check[1][0]}\nMessage: {check[0][1]}')
        else:
            print('Organization not specified!')

    def get_org_info(self):
        # Gathers information about an organization
        error_check = False
        error_messages = list()

        repo_list_resp, repo_list = self.list_repos()
        team_list_resp, team_list = self.list_teams()

        if repo_list_resp == 'error':
            error_check = True
            error_messages.append(repo_list)

        if team_list_resp == 'error':
            error_check = True
            error_messages.append(team_list)

        if error_check:
            return 'error', error_messages

        return 'ok', (repo_list[1], team_list[1])

    def list_teams(self):
        url = f'{self.url}orgs/{self.org_name}/teams'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def get_team_by_name(self, team_name):
        url = f'{self.url}orgs/{self.org_name}/teams/{team_name}'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def check_team_repo_permission(self, team_name, repo_name):
        # Checks specific repo teams permission
        self.headers['Accept'] = 'application/vnd.github.v3.repository+json'
        # TODO : might be issue
        owner = self._get_repo_owner(repo_name)

        url = f'{self.url}orgs/{self.org_name}/teams/{team_name}/repos/{owner}/{repo_name}'
        response = requests.get(url, headers=self.headers)

        msg_type, data = self._eval_response(response)
        permission_data = json.loads(data[1])

        role_name = permission_data['role_name']

        if msg_type == 'ok':
            return msg_type, [data[0], role_name]
        else:
            return msg_type, data

    def create_team(self):
        # TODO : ?
        pass

    def update_team(self):
        # TODO : ?
        pass

    def delete_team(self):
        # TODO : ?
        pass

    def list_team_repos(self, team_name):
        url = f'{self.url}orgs/{self.org_name}/teams/{team_name}/repos'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def list_team_members(self, team_name):
        url = f'{self.url}orgs/{self.org_name}/teams/{team_name}/members'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def list_repo_keys(self, repo_name):
        # TODO : might be an issue
        owner = self._get_repo_owner(repo_name)

        url = f'{self.url}repos/{owner}/{repo_name}/keys'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def create_repo_key(self, repo_name, key_name, public_key, read_only=True):
        # TODO : might be an issue
        owner = self._get_repo_owner(repo_name)
        data = {'title': key_name,
                'key': public_key,
                'read_only': read_only}

        url = f'{self.url}repos/{owner}/{repo_name}/keys'
        response = requests.post(url, headers=self.headers, json=data)

        return self._eval_response(response)

    def _get_repo_owner(self, repo_name):
        repo_data = json.loads(self.list_repos()[1][1])
        owner = False

        for repo in repo_data:
            if repo['name'] == repo_name:
                owner = repo['owner']['login']

        return owner

    @staticmethod
    def _eval_response(resp):
        # TODO : check resp.text to json
        if resp.status_code in [400, 404]:
            return 'error', f'Status code: {resp.status_code}\nResponse: {resp.text}'
        else:
            return 'ok', [resp.status_code, resp.text]
