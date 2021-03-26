from unittest import TestCase

from crypto.blockchain.transaction import Transaction
from crypto.client.client import Client


class TestTransactionSigning(TestCase):

    def setUp(self):
        self.user_1 = Client()
        self.user_2 = Client()

    def test_verify_transaction_correct(self):
        transaction = Transaction(self.user_1.public_key, self.user_2.public_key, 100)
        transaction.sign_transaction(self.user_1.private_key)
        self.assertTrue(transaction.verify_transaction())

    def test_verify_transaction_no_signature(self):
        transaction = Transaction(self.user_1.public_key, self.user_2.public_key, 100)
        self.assertFalse(transaction.verify_transaction())

    def test_verify_transaction_fake_transaction(self):
        transaction = Transaction(self.user_1.public_key, self.user_2.public_key, 100)
        fake_signing_user = Client()
        transaction.sign_transaction(fake_signing_user.private_key)
        self.assertFalse(transaction.verify_transaction())
