from crypto.blockchain.transaction import Transaction
from crypto.client.client import Client


class Token:

    def __init__(self):
        self.name = "RarCoin"
        self.total_supply = 1000
        self.init_user = Client()
        self.supply_user = Client()

    def create_supply_transaction(self):
        transaction = Transaction(self.init_user.public_key, self.supply_user.public_key, self.total_supply)
        transaction.sign_transaction(self.init_user.private_key)
        return transaction
