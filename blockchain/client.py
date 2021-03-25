from Crypto.PublicKey import RSA


class Client:

    def __init__(self):
        """
        Creates a new RSA key pair
        """
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()

    def save_key_to_file(self):
        file = open('myKey.pem', 'wb')
        file.write(self.private_key.exportKey('PEM'))
        file.close()

    def read_key_from_file(self):
        file = open('myKey.pem', 'r')
        return RSA.importKey(file.read())
