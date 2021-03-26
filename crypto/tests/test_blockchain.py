from unittest import TestCase

from crypto.blockchain.block import Block
from crypto.blockchain.blockchain import Blockchain
from crypto.blockchain.transaction import Transaction
from crypto.client.client import Client


class TestBlockchain(TestCase):

    def setUp(self):
        self.test_blockchain = Blockchain()

        # Test block
        self.test_block_index = 100
        self.test_block_prev_hash = "00123456ab"
        self.test_block_merkle_root = "ffabff123",

        # Test transaction with signing
        self.send_user_1 = Client()
        self.receive_user_2 = Client()
        self.test_block_transaction = Transaction(self.send_user_1.public_key, self.receive_user_2.public_key, 100)
        self.test_block_transaction.sign_transaction(self.send_user_1.private_key)
        self.test_block_transaction_list = [self.test_block_transaction]

        self.test_block = Block(
            self.test_block_index,
            self.test_block_prev_hash,
            self.test_block_merkle_root,
            self.test_block_transaction_list,
            0
        )

    def test_genesis_block_creation(self):
        transaction_hash = self.test_blockchain.hash_transactions(self.test_block_transaction_list)

        genesis_test_blockchain = Blockchain()
        genesis_test_blockchain.create_genesis_bock(self.send_user_1, self.receive_user_2)
        # There are two blocks, the last one should be the genesis block which is created above
        last_block = genesis_test_blockchain.get_last_block

        self.assertEqual(last_block.index, 0)
        self.assertEqual(last_block.previous_hash, "0000000000000000000000000000000000000000000000000000000000000000")
        self.assertEqual(last_block.merkle_root, transaction_hash)
        self.assertEqual(len(last_block.transactions), 1)
        self.assertEqual(last_block.transactions[0].amount, 100)

    def test_mine_block(self):
        self.test_blockchain.add_new_transaction(self.test_block_transaction)
        self.assertEqual(len(self.test_blockchain.open_transactions), 1)

        self.test_blockchain.mine_block()

        self.assertEqual(len(self.test_blockchain.chain), 2)
        self.assertEqual(len(self.test_blockchain.open_transactions), 0)
        self.assertEqual(len(self.test_blockchain.get_last_block.transactions), 1)
        self.assertEqual(self.test_blockchain.get_last_block.transactions[0].amount, 100)

    def test_proof_of_work(self):
        proof_calc_nonce = self.test_blockchain.proof_of_work(self.test_block)
        proof_calc_hash = self.test_block.hash

        # During the creation of a block a hash is created.
        # With the nonce given by the proof of work algorithm,
        # the hash should be the same
        block_to_compare = Block(
            self.test_block_index,
            self.test_block_prev_hash,
            self.test_block_merkle_root,
            self.test_block_transaction_list,
            proof_calc_nonce
        )

        # If the hash of a block starts with '00' the nonce should not be changed
        nonce_block_to_compare = self.test_blockchain.proof_of_work(block_to_compare)

        self.assertEqual(block_to_compare.hash, proof_calc_hash)
        self.assertEqual(nonce_block_to_compare, proof_calc_nonce)

    def test_example_blockchain_multiple_blocks(self):
        gen_block = self.test_blockchain.get_last_block

        # first block after genesis
        self.test_blockchain.add_new_transaction(self.test_block_transaction)
        self.test_blockchain.mine_block()

        middle_block = self.test_blockchain.get_last_block
        middle_block_hash = self.test_blockchain.get_last_block.hash
        self.assertEqual(middle_block.previous_hash, gen_block.hash)
        self.assertEqual(middle_block.index, 1)
        self.assertEqual(len(middle_block.transactions), 1)
        self.assertEqual(len(self.test_blockchain.open_transactions), 0)
        self.assertTrue(middle_block.timestamp > gen_block.timestamp)

        # second block after gensis
        test_user_1 = Client()
        test_user_2 = Client()
        new_transaction_1 = Transaction(test_user_1.public_key, test_user_2.public_key, 100)
        new_transaction_1.sign_transaction(test_user_1.private_key)
        new_transaction_2 = Transaction(test_user_1.public_key, test_user_2.public_key, 1)
        new_transaction_2.sign_transaction(test_user_1.private_key)
        self.test_blockchain.add_new_transaction(new_transaction_1)
        self.test_blockchain.add_new_transaction(new_transaction_2)

        self.test_blockchain.mine_block()

        last_block = self.test_blockchain.get_last_block
        self.assertNotEqual(last_block.hash, middle_block_hash)
        self.assertEqual(last_block.previous_hash, middle_block_hash)
        self.assertEqual(len(last_block.transactions), 2)
        self.assertEqual(len(self.test_blockchain.chain), 3)
        self.assertTrue(last_block.timestamp > middle_block.timestamp)

    def test_balance_of_address(self):
        test_user_1 = Client()
        test_user_2 = Client()
        test_user_3 = Client()

        new_transaction_1 = Transaction(test_user_1.public_key, test_user_2.public_key, 100)
        new_transaction_1.sign_transaction(test_user_1.private_key)

        new_transaction_2 = Transaction(test_user_1.public_key, test_user_2.public_key, 10)
        new_transaction_2.sign_transaction(test_user_1.private_key)

        new_transaction_3 = Transaction(test_user_2.public_key, test_user_3.public_key, 50)
        new_transaction_3.sign_transaction(test_user_2.private_key)

        new_transaction_4 = Transaction(test_user_3.public_key, test_user_1.public_key, 20)
        new_transaction_4.sign_transaction(test_user_3.private_key)

        self.test_blockchain.add_new_transaction(new_transaction_1)
        self.test_blockchain.add_new_transaction(new_transaction_2)
        self.test_blockchain.add_new_transaction(new_transaction_3)
        self.test_blockchain.add_new_transaction(new_transaction_4)
        self.test_blockchain.mine_block()

        self.assertEqual(self.test_blockchain.get_balance_for_address(test_user_1.public_key), -90)
        self.assertEqual(self.test_blockchain.get_balance_for_address(test_user_2.public_key), 60)
        self.assertEqual(self.test_blockchain.get_balance_for_address(test_user_3.public_key), 30)
