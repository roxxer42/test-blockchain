import hashlib
import json

from Crypto.PublicKey.RSA import RsaKey

from crypto.blockchain.block import Block
from crypto.blockchain.transaction import Transaction
from crypto.token.token import Token


class Blockchain:

    def __init__(self):
        self.open_transactions = []
        self.chain = []
        self.token = Token()
        self.create_genesis_bock(self.token.create_supply_transaction())

    def create_genesis_bock(self, start_transaction: Transaction):
        """
        Creates a genesis block which will be the first block of the blockchain
        """
        # First index
        genesis_block_index = 0
        # There is no previous block so this hash is just a dummy
        genesis_block_prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        # Initial transaction because there have to be at least one transaction per block
        hashed_transactions = self.hash_transactions([start_transaction])

        # Initial nonce
        genesis_block_nonce = 0

        genesis_block = Block(
            genesis_block_index,
            genesis_block_prev_hash,
            hashed_transactions,
            [start_transaction],
            genesis_block_nonce)
        self.chain.append(genesis_block)

    def add_block_to_chain(self, new_block: Block):
        """
        Adds a new block to the blockchain
        :param new_block: Block which will be added to the blockchain
        """
        self.chain.append(new_block)

    def add_new_transaction(self, transaction: Transaction):
        """
        Adds a valid transaction to the opened transactions
        :param transaction: Transaction which will be added to the unprocessed transactions
        """
        if transaction.check_if_transaction_is_valid() and \
                self.check_balance_of_address(transaction.sender.public_key(), transaction.amount):
            self.open_transactions.append(transaction)

    def hash_transactions(self, transactions: [Transaction]):
        """
        Returns a hash of the current opened transactions
        Hashes each transaction and then build a hash over all hashes
        :param transactions: List of transactions which should be hashed
        :return: Hash of the transactions in hex.
        :rtype: str
        """
        hashed_transactions = []
        for tx in transactions:
            hashed_transactions.append(tx.hash_transaction().hexdigest())
        return hashlib.sha256(json.dumps(hashed_transactions).encode('utf-8')).hexdigest()

    def mine_block(self):
        """
        Starts to mine a new block if at least one transaction is in the opened transactions.
        At first, the opened transactions have to be hashed.
        If the proof of work was successfully the block will be added to the blockchain.
        Resets the opened transactions.
        """

        if len(self.open_transactions) == 0:
            return

        last_block = self.get_last_block
        new_block_index = last_block.index + 1
        new_previous_hash = last_block.hash
        new_hashed_transaction_root = self.hash_transactions(self.open_transactions)

        # Creates the new block with a references the hash of the current last block of the blockchain
        # The nonce will be starting at 0
        new_block = Block(new_block_index,
                          new_previous_hash,
                          new_hashed_transaction_root,
                          self.open_transactions,
                          0)

        self.proof_of_work(new_block)
        self.add_block_to_chain(new_block)
        # reset open transaction
        self.open_transactions = []

    def proof_of_work(self, block: Block):
        """
        Proof of work algorithm. At the moment, there is no difficulty.
        Increments the nonce until the first position of a hashed block is equal to 00
        :param block: Block which should be mined
        """
        computed_hash = block.hash
        while not computed_hash.startswith('00'):
            block.nonce += 1
            computed_hash = block.hash_block()
        block.hash = computed_hash
        return block.nonce

    def check_balance_of_address(self, public_key, amount):
        """
        Checks if the balance of an address is enough to perform a transaction
        :param public_key: Address to check
        :param amount: Amount to perform a transaction
        :return: True if balance is enough otherwise False
        """
        current_amount = self.get_balance_for_address(public_key)
        if current_amount >= amount:
            return True
        else:
            return False

    def get_balance_for_address(self, public_key: RsaKey):
        """
        Calculates the balance for a specific address.
        Be careful with the runtime O(n^2).
        :param public_key: The address for checking the balance
        :return: Balance of the given address
        :rtype: int
        """
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                amount = tx.amount
                if tx.recipient == public_key:
                    balance += amount
                if tx.sender == public_key:
                    balance -= amount
        return balance

    @property
    def get_last_block(self):
        """
        :return: Last block of the blockchain
        """
        return self.chain[-1]

    @property
    def get_full_blockchain(self):
        """
        :return: All blocks of the blockchain
        """
        return self.chain

    def get_block_by_index(self, index):
        """
        :return: A specific block of the blockchain by an index
        """
        return self.chain[index]
