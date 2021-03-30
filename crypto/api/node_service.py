import json

from crypto.config.setup import BLOCKCHAIN, NODE


@NODE.route('/getBlocks/', methods=['GET'])
def get_current_blockchain():
    all_blocks = BLOCKCHAIN.get_all_blocks
    blocks_to_json = []
    for block in all_blocks:
        blocks_to_json.append(block.to_dict())
    return json.dumps(blocks_to_json)
