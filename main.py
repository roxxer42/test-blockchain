from blockchain.blockchain import Blockchain
from blockchain.client import Client
from blockchain.transaction import Transaction

if __name__ == '__main__':
    # Examples
    blockchain = Blockchain()

    sender = Client()
    receiver = Client()
    test_transaction = Transaction(sender.public_key, receiver.public_key, 100)
    test_transaction.sign_transaction(sender.private_key)
    test_transaction.verify_transaction()

    blockchain.add_new_transaction(test_transaction)
    blockchain.mine_block()

    balance_sender = blockchain.get_balance_for_address(sender.public_key)
    print(balance_sender)

    print(blockchain.get_block_by_index(0).hash)
    print(blockchain.get_block_by_index(1).previous_hash)
