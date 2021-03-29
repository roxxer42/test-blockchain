from crypto.blockchain.transaction import Transaction
from crypto.client.client import Client


class Miner:

    def __init__(self):
        self.miner = Client()

    def create_mining_transaction(self, supply_user: Client, reward: int):
        reward_transaction = Transaction(supply_user.public_key, self.miner.public_key, reward)
        reward_transaction.sign_transaction(supply_user.private_key)
        return reward_transaction
