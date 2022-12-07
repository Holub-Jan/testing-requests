import requests
import json


class GitHubRepo:

    def __init__(self, org_name):
        self.org_name = org_name
        self.url = str()
        self.headers = {'Accept': 'application/vnd.github+json'}
        self.data = dict()
        self.params = dict()

        self.request = None

        self._load_token()

    def list_repos(self):
        self.url = f'https://api.github.com/orgs/{self.org_name}/repos'
        self.request = requests.get(self.url, headers=self.headers)

        return self.status_code(), self.text_response()

    def create_repo(self):
        self.request = requests.put(self.url, headers=self.headers, data=self.data)

        return self.status_code(), self.text_response()

    def rename_repo(self):
        self.request = requests.post(self.url, headers=self.headers, data=self.data)

        return self.status_code(), self.text_response()

    def delete_repo(self):
        self.request = requests.delete(self.url, headers=self.headers)

        return self.status_code(), self.text_response()

    def set_headers(self, headers):
        self.headers = json.dumps(headers)

    def set_data(self, data):
        self.data = json.dumps(data)

    def set_params(self, params):
        self.params = json.dumps(params)

    def json_response(self):
        return json.loads(self.request.text)

    def text_response(self):
        return self.request.text

    def status_code(self):
        return self.request.status_code

    def _load_token(self):
        f = open("secrets.txt", "r")
        token = f.readline()
        f.close()

        self.headers['Authorization'] = f'Bearer {token}'


request = GitHubRepo('standa-novak')

resp_code, resp = request.list_repos()

print(resp_code)
print(resp)
