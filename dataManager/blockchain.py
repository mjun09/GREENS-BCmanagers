## Here’s a simple implementation of a blockchain in Python
# that allows storing a large amount of data as transactions.
# Each block contains multiple transactions, and
# the blockchain validates and stores the blocks in a linked manner
# using cryptographic hashes.
#
## Key Features:
#	1.	Transactions: Each transaction stores sender, recipient, and data.
#	2.	Blocks: Each block includes a list of transactions, a timestamp, and
#       	    links to the previous block using a hash.
#	3.	Mining: Simple proof-of-work mechanism using a difficulty level.
#	4.	Validation: Ensures the chain’s integrity by checking hashes.
#
## How to Run:
#	1.	Save the code into a Python file, e.g., blockchain.py.
#	2.	Run it using Python: python blockchain.py.
#	3.	Add more transactions, adjust the difficulty, or experiment with the mining process.

import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, data):
        self.sender = sender
        self.recipient = recipient
        self.data = data

    def __repr__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, data={self.data})"

class Block:
    def __init__(self, previous_hash, transactions, timestamp=None):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.previous_hash) +
            str(self.timestamp) +
            str([str(tx) for tx in self.transactions]) +
            str(self.nonce)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        return f"Block(hash={self.hash}, transactions={self.transactions})"

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block("0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise ValueError("Invalid transaction format")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        # Reward for mining
        self.pending_transactions.append(Transaction("System", miner_address, "Mining Reward"))

        new_block = Block(self.get_latest_block().hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False

        return True

    def __repr__(self):
        return f"Blockchain(chain={self.chain})"


# Example usage
if __name__ == "__main__":
    # Create blockchain
    my_blockchain = Blockchain(difficulty=3)

    # Add transactions
    my_blockchain.add_transaction(Transaction("Alice", "Bob", "Data block 1"))
    my_blockchain.add_transaction(Transaction("Bob", "Charlie", "Data block 2"))

    # Mine pending transactions
    my_blockchain.mine_pending_transactions("Miner1")

    # Add more transactions and mine again
    my_blockchain.add_transaction(Transaction("Charlie", "Alice", "Data block 3"))
    my_blockchain.mine_pending_transactions("Miner2")

    # Check the blockchain's validity and display it
    print(f"Is Blockchain Valid? {my_blockchain.is_chain_valid()}")
    print("Blockchain:")
    for block in my_blockchain.chain:
        print(block)