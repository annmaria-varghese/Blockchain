import hashlib
import json
from time import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  # For mining
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
class Blockchain:
    difficulty = 2  # Simple mining difficulty

    def __init__(self):
        self.unconfirmed_transactions = []  # Pending transactions
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0")
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not proof.startswith('0' * Blockchain.difficulty):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        new_block = Block(index=self.last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time(),
                          previous_hash=self.last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
if __name__ == "__main__":
    blockchain = Blockchain()

    print("Adding transactions...")
    blockchain.add_new_transaction({"sender": "Alice", "recipient": "Bob", "amount": 50})
    blockchain.add_new_transaction({"sender": "Bob", "recipient": "Charlie", "amount": 25})

    print("Mining...")
    blockchain.mine()

    print("Adding more transactions...")
    blockchain.add_new_transaction({"sender": "Charlie", "recipient": "Alice", "amount": 10})
    blockchain.mine()

    print("\nBlockchain:")
    for block in blockchain.chain:
        print(f"Index: {block.index}, Transactions: {block.transactions}, Hash: {block.hash[:10]}...")
