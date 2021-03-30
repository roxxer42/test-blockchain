from crypto.blockchain.transaction import Transaction
from crypto.client.client import Client
from crypto.config.setup import BLOCKCHAIN, NODE

if __name__ == '__main__':
    blockchain = BLOCKCHAIN
    NODE.run()

    sender = Client()
    receiver = Client()
    test_transaction = Transaction(sender.public_key, receiver.public_key, 100)
    test_transaction.sign_transaction(sender.private_key)
    test_transaction.verify_transaction()

    blockchain.add_new_transaction(test_transaction)
    blockchain.mine_block()

    balance_sender = blockchain.get_balance_for_address(sender.public_key)
    print(balance_sender)
