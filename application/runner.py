class CLI:
    def __init__(self):
        self._gh_token = str()
        self._db_pass = str()

        self._load_secrets()

    def _load_secrets(self):
        f = open("../secrets.txt", "r")
        token_line = f.readline()
        pass_line = f.readline()
        f.close()

        self._gh_token = token_line.split(' ')[1][:-1]
        self._db_pass = pass_line.split(' ')[1]


x = CLI()
