from datetime import datetime

from Crypto.Hash import SHA256
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15


class Transaction:

    def __init__(self, sender: RsaKey, recipient: RsaKey, amount: int):
        """
        Creates a new transaction
        :param sender: Public key of the sender
        :param recipient: Public key of the recipient
        :param amount: Amount to send
        """
        self.sender = sender
        self.recipient = recipient
        self.signature = None
        self.amount = amount
        self.timestamp = datetime.now()

    def encoded_transaction(self):
        return (str(self.sender) + str(self.recipient) + str(self.amount)).encode('utf-8')

    def sign_transaction(self, private_key: RsaKey):
        """
        Signs a transaction and sets the signature parameter for the given transaction
        :param private_key: Private key to sign the transaction
        """
        encoded_transaction = SHA256.new(self.encoded_transaction())
        self.signature = pkcs1_15.new(private_key).sign(encoded_transaction)

    def verify_transaction(self):
        """
        Checks if the signature of a transaction is valid
        :return: True if the transaction was signed correctly and
        false if the signature is not valid
        """
        transaction_to_verify = SHA256.new(self.encoded_transaction())
        try:
            pkcs1_15.new(self.sender).verify(transaction_to_verify, self.signature)
            return True
        except (ValueError, TypeError):
            return False

    def check_if_transaction_is_valid(self):
        if self.signature is None:
            return False
        return self.verify_transaction()

    def hash_transaction(self):
        """
        Hashes a transaction for mining a block
        :return: Returns a SHA256 hashed transaction
        :rtype: SHA256Hash
        """
        new_hash_object = SHA256.new()
        new_hash_object.update(self.encoded_transaction())
        return new_hash_object
