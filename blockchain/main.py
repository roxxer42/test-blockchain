from blockchain import Blockchain
from client import Client
from transaction import Transaction

if __name__ == '__main__':
    # Examples
    blockchain = Blockchain()
    blockchain.mine_block()

    sender = Client()
    receiver = Client()
    test_transaction = Transaction(sender.public_key, receiver.public_key, 100)
    test_transaction.sign_transaction(sender.private_key)
    print(test_transaction.signature)

    test_transaction.verify_transaction()
