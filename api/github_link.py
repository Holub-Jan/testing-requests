import requests
import json


class GitHubRepo:

    def __init__(self, org_name, token):
        self.org_name = org_name
        self.token = token

        self.url = 'https://api.github.com/'
        self.headers = {'Accept': 'application/vnd.github+json'}

        self._load_token()

    def list_repos(self):
        url = self.url + f'orgs/{self.org_name}/repos'
        response = requests.get(url, headers=self.headers)

        return self._eval_response(response)

    def create_repo(self, data):
        url = self.url + f'orgs/{self.org_name}/repos'
        response = requests.post(url, headers=self.headers, json=data)

        return self._eval_response(response)

    def rename_repo(self, data):
        response = requests.post(self.url, headers=self.headers, json=data)

        return response

    def delete_repo(self):
        response = requests.delete(self.url, headers=self.headers)

        return response

    def _load_token(self):
        self.headers['Authorization'] = f'Bearer {self.token}'

    @staticmethod
    def _eval_response(resp):
        if resp.status_code == 400:
            return 'error', f'Status code: {resp.status_code}\nResponse: {resp.text}'
        else:
            return 'ok', [resp.status_code, resp.text]


#request = GitHubRepo('standa-novak')
