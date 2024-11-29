## Below is a Python implementation of a blockchain tailored to manage versions of algorithms,
# including their identity names, lifetimes, expiration dates, a shared policy file, and
# associated regulations.
#
## Key Features
#	1.	Algorithm Structure: Each algorithm stores:
#	•	Identity name
#	•	Version
#	•	Lifetime
#	•	Expiration date
#	•	Policy file
#	•	Associated regulations
#	2.	Blockchain Structure:
#	•	Stores multiple algorithms per block.
#	•	Links blocks cryptographically.
#	3.	Mining and Validation:
#	•	Proof-of-work ensures immutability.
#	•	Validates the chain by verifying hashes.
#	4.	Customizable:
#	•	The difficulty level can be adjusted.
#	•	Add policies and regulations as per need.
#
## Running the Code
#	1.	Save the code into a Python file, e.g., algorithm_blockchain.py.
#	2.	Run it using Python: python algorithm_blockchain.py.
#	3.	Experiment with adding new algorithms and viewing the blockchain’s state.


import hashlib
import time

class Algorithm:
    def __init__(self, identity_name, version, lifetime, expiration_date, policy_file, regulations):
        self.identity_name = identity_name
        self.version = version
        self.lifetime = lifetime
        self.expiration_date = expiration_date
        self.policy_file = policy_file
        self.regulations = regulations

    def __repr__(self):
        return (f"Algorithm(identity_name={self.identity_name}, version={self.version}, "
                f"lifetime={self.lifetime}, expiration_date={self.expiration_date}, "
                f"policy_file={self.policy_file}, regulations={self.regulations})")


class Block:
    def __init__(self, previous_hash, algorithms, timestamp=None):
        self.previous_hash = previous_hash
        self.algorithms = algorithms  # List of algorithms in the block
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.previous_hash) +
            str(self.timestamp) +
            str([str(alg) for alg in self.algorithms]) +
            str(self.nonce)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        return f"Block(hash={self.hash}, algorithms={self.algorithms})"


class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_algorithms = []

    def create_genesis_block(self):
        return Block("0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_algorithm(self, algorithm):
        if not isinstance(algorithm, Algorithm):
            raise ValueError("Invalid algorithm format")
        self.pending_algorithms.append(algorithm)

    def mine_pending_algorithms(self):
        new_block = Block(self.get_latest_block().hash, self.pending_algorithms)
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.pending_algorithms = []

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
    # Create blockchain for algorithms
    algo_blockchain = Blockchain(difficulty=3)

    # Add algorithms
    algo_blockchain.add_algorithm(Algorithm(
        identity_name="Algorithm1",
        version="1.0",
        lifetime="2 years",
        expiration_date="2026-01-01",
        policy_file="policy_v1.json",
        regulations="Regulation A"
    ))

    algo_blockchain.add_algorithm(Algorithm(
        identity_name="Algorithm2",
        version="2.1",
        lifetime="3 years",
        expiration_date="2027-03-01",
        policy_file="policy_v2.json",
        regulations="Regulation B"
    ))

    # Mine pending algorithms
    algo_blockchain.mine_pending_algorithms()

    # Add another set of algorithms
    algo_blockchain.add_algorithm(Algorithm(
        identity_name="Algorithm3",
        version="3.0",
        lifetime="5 years",
        expiration_date="2029-01-01",
        policy_file="policy_v3.json",
        regulations="Regulation C"
    ))

    algo_blockchain.mine_pending_algorithms()

    # Check blockchain validity and display
    print(f"Is Blockchain Valid? {algo_blockchain.is_chain_valid()}")
    print("Blockchain:")
    for block in algo_blockchain.chain:
        print(block)