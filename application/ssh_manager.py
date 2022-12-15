import os

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


class SSHManager:
    def __init__(self):
        # save to db only
        self._default_file_location = '\\'.join(os.path.realpath('').split('\\')[:3]) + '\\.ssh'
        self._file_location = self._default_file_location

    def gen_ssh_key(self, key_name):
        private_key, public_key = self._gen_new_keys()

        self._save_new_keys(key_name, private_key, public_key)

    def change_file_location(self, file_location):
        self._file_location = file_location

    def location_to_default(self):
        self._file_location = self._default_file_location

    def _gen_new_keys(self):
        # TODO : add additional options for encoding?
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )

        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )

        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.OpenSSH,
            crypto_serialization.PublicFormat.OpenSSH
        )

        return private_key.decode(), public_key.decode()

    def _save_new_keys(self, key_name, private_key, public_key):
        # TODO : checking if key_name already exists? or elsewhere
        with open(f'{self._file_location}\\{key_name}', 'w', encoding='utf-8') as f:
            f.write(private_key)

        with open(f'{self._file_location}\\{key_name}.pub', 'w', encoding='utf-8') as f:
            f.write(public_key)

    def run(self):
        self.gen_ssh_key('test_key_name')


ssh = SSHManager()
ssh.run()
