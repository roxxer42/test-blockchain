from crypto.blockchain.blockchain import Blockchain
from flask import Flask, request

# TODO Means that every node init it own blockchain
BLOCKCHAIN = Blockchain()

# Flask setup
NODE = Flask(__name__)
# This import will import the routes. Do not remove!
import crypto.api.node_service

