import hashlib
from datetime import datetime

from crypto.blockchain.transaction import Transaction


class Block:

    def __init__(self, index: int, previous_hash: str, merkle_root: str, transactions: [Transaction], nonce: int):
        self.index = index
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.hash_block()
        self.timestamp = datetime.now()

    def hash_block(self):
        """
        Creates the hash of a block. Does not use the transactions
        because the merkleRoot is already the hash of the transactions.
        :return: Hash of the block
        :rtype: str
        """
        h = hashlib.sha256()
        h.update(
            str(self.index).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.merkle_root).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )
        return h.hexdigest()

    def to_dict(self):
        dict_transactions = []
        for tx in self.transactions:
            dict_transactions.append(tx.to_dict())

        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "transactions": dict_transactions,
            "nonce": self.nonce,
            "timestamp": str(self.timestamp)
        }
