## Below is an implementation of a blockchain in Python that records datasets and
# the outputs of AI algorithms. This blockchain is designed to ensure transparency,
# traceability, and immutability in the process of recording AI operations.
#
## Key Features
#	1.	AI Operation Details:
#	•	Algorithm Name: Name of the AI algorithm used.
#	•	Dataset: Dataset associated with the operation.
#	•	Output: Result produced by the algorithm.
#	•	Parameters: Parameters used in the algorithm.
#	2.	Mining and Proof-of-Work:
#	•	Ensures immutability of records using a hash-based proof-of-work mechanism.
#	3.	Validation:
#	•	Checks the integrity of the blockchain by validating hashes.
#	4.	Extensibility:
#	•	Add more metadata fields to the AIOperation class as needed.
#
## How to Use
#	1.	Run the Code:
#	•	Save the script as archiver.py.
#	•	Execute with python archiver.py.
#	2.	Add Operations:
#	•	Use add_operation to log datasets and outputs.
#	3.	Validate Blockchain:
#	•	Use is_chain_valid to check the blockchain’s integrity.

import hashlib
import time

class AIOperation:
    def __init__(self, algorithm_name, dataset, output, parameters, timestamp=None):
        """
        Records an AI operation.
        :param algorithm_name: Name of the AI algorithm.
        :param dataset: Dataset used by the algorithm.
        :param output: Output produced by the algorithm.
        :param parameters: Parameters used in the algorithm.
        :param timestamp: Timestamp of the operation.
        """
        self.algorithm_name = algorithm_name
        self.dataset = dataset
        self.output = output
        self.parameters = parameters
        self.timestamp = timestamp or time.time()

    def __repr__(self):
        return (f"AIOperation(algorithm_name={self.algorithm_name}, dataset={self.dataset}, "
                f"output={self.output}, parameters={self.parameters}, timestamp={self.timestamp})")


class Block:
    def __init__(self, previous_hash, operations, timestamp=None):
        """
        Represents a block in the blockchain.
        :param previous_hash: Hash of the previous block.
        :param operations: List of AI operations included in this block.
        :param timestamp: Timestamp of the block creation.
        """
        self.previous_hash = previous_hash
        self.operations = operations
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_content = (
            str(self.previous_hash) +
            str(self.timestamp) +
            str([str(op) for op in self.operations]) +
            str(self.nonce)
        )
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        """
        Mines the block by finding a hash with a specific number of leading zeros.
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

    def __repr__(self):
        return f"Block(hash={self.hash}, operations={self.operations})"


class Blockchain:
    def __init__(self, difficulty=2):
        """
        Initializes the blockchain.
        :param difficulty: Mining difficulty for proof-of-work.
        """
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_operations = []

    def create_genesis_block(self):
        """
        Creates the genesis block.
        """
        return Block("0", [], time.time())

    def get_latest_block(self):
        """
        Returns the latest block in the chain.
        """
        return self.chain[-1]

    def add_operation(self, operation):
        """
        Adds an AI operation to the list of pending operations.
        :param operation: An instance of AIOperation.
        """
        if not isinstance(operation, AIOperation):
            raise ValueError("Invalid operation format")
        self.pending_operations.append(operation)

    def mine_pending_operations(self, miner_address):
        """
        Mines a block with pending operations and rewards the miner.
        :param miner_address: Address of the miner for reward.
        """
        # Reward the miner
        reward_operation = AIOperation(
            algorithm_name="Reward",
            dataset="System Reward",
            output=f"Reward to {miner_address}",
            parameters="",
        )
        self.pending_operations.append(reward_operation)

        # Create a new block
        new_block = Block(self.get_latest_block().hash, self.pending_operations)
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        self.pending_operations = []

    def is_chain_valid(self):
        """
        Validates the blockchain's integrity.
        """
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
    # Initialize the blockchain
    ai_blockchain = Blockchain(difficulty=3)

    # Add AI operations
    ai_blockchain.add_operation(AIOperation(
        algorithm_name="Algorithm1",
        dataset="Dataset1.csv",
        output="Classification Result: [A, B, C]",
        parameters="{'learning_rate': 0.01, 'epochs': 50}"
    ))

    ai_blockchain.add_operation(AIOperation(
        algorithm_name="Algorithm2",
        dataset="Dataset2.csv",
        output="Regression Output: [3.5, 4.1, 5.2]",
        parameters="{'alpha': 0.1, 'max_iter': 100}"
    ))

    # Mine the pending operations
    ai_blockchain.mine_pending_operations(miner_address="Miner1")

    # Add more AI operations
    ai_blockchain.add_operation(AIOperation(
        algorithm_name="Algorithm3",
        dataset="Dataset3.json",
        output="Cluster Centers: [(1,2), (3,4), (5,6)]",
        parameters="{'clusters': 3, 'init': 'k-means++'}"
    ))

    ai_blockchain.mine_pending_operations(miner_address="Miner2")

    # Validate and display the blockchain
    print(f"Is Blockchain Valid? {ai_blockchain.is_chain_valid()}")
    print("Blockchain:")
    for block in ai_blockchain.chain:
        print(block)