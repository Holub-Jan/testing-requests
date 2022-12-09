import requests


class GitHubLink:

    def __init__(self, org_name, token):
        self.org_name = org_name
        self.token = token

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
        # org name - get db for ord_id
        # all repo names - list repo
        error_check = False
        error_messages = list()

        repo_list_resp, repo_list = self.list_repos()

        if repo_list_resp == 'error':
            error_check = True

        if error_check:
            return 'error', error_messages

        return 'ok', repo_list[1]

    @staticmethod
    def _eval_response(resp):
        if resp.status_code == 400:
            return 'error', f'Status code: {resp.status_code}\nResponse: {resp.text}'
        else:
            return 'ok', [resp.status_code, resp.text]

