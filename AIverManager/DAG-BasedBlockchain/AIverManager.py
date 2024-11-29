## Below is a Python implementation of a DAG-based blockchain
# for managing AIadapters. Each aladapter is represented as a node in the DAG.
# The DAG maintains dependencies between AIadapter versions, along with metadata
# like identity name, lifetime, expiration date, policy files, and regulations.
##
# Key Features
# 	1.	AIadapter Metadata:
# 		- Identity Name: Unique name of the algorithm.
# 		- Version: Version number of the algorithm.
# 		- Lifetime: Duration of the algorithm’s validity.
# 		- Expiration Date: Expiration date of the algorithm.
# 		- Policy File: Shared policy file name.
# 		- Regulations: Rules and policies governing the algorithm.
# 	2.	DAG Structure:
# 		- Nodes represent individual algorithm versions.
# 		- Each node can reference one or more parent nodes, ensuring dependency tracking.
# 	3.	Validation:
# 		- Ensures the graph is acyclic.
# 		- Verifies parent dependencies exist before adding new nodes.
# 	4.	Extensibility:
# 		- New metadata fields can be added to Aladapter as needed.
# 		- DAG structure can be used for advanced dependency analysis.

import hashlib
import time
from typing import List, Dict


class Aladapter:
    def __init__(self, identity_name, version, lifetime, expiration_date, policy_file, regulations):
        """
        Represents an aladapter in the DAG blockchain.
        :param identity_name: Unique name of the aladapter.
        :param version: Version of the aladapter.
        :param lifetime: Lifetime of the aladapter.
        :param expiration_date: Expiration date of the aladapter.
        :param policy_file: Shared policy file for the aladapter.
        :param regulations: Regulations associated with the aladapter.
        """
        self.identity_name = identity_name
        self.version = version
        self.lifetime = lifetime
        self.expiration_date = expiration_date
        self.policy_file = policy_file
        self.regulations = regulations
        self.timestamp = time.time()

    def __repr__(self):
        return (f"Aladapter(identity_name={self.identity_name}, version={self.version}, "
                f"lifetime={self.lifetime}, expiration_date={self.expiration_date}, "
                f"policy_file={self.policy_file}, regulations={self.regulations}, "
                f"timestamp={self.timestamp})")


class DAGNode:
    def __init__(self, aladapter, parent_hashes):
        """
        Represents a node in the DAG blockchain.
        :param aladapter: Aladapter object.
        :param parent_hashes: List of hashes of parent nodes.
        """
        self.aladapter = aladapter
        self.parent_hashes = parent_hashes
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculates the hash for this node based on its content.
        """
        content = (
            str(self.aladapter.identity_name) +
            str(self.aladapter.version) +
            str(self.aladapter.lifetime) +
            str(self.aladapter.expiration_date) +
            str(self.aladapter.policy_file) +
            str(self.aladapter.regulations) +
            str(self.timestamp) +
            ''.join(self.parent_hashes)
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def __repr__(self):
        return (f"DAGNode(hash={self.hash}, aladapter={self.aladapter}, "
                f"parent_hashes={self.parent_hashes})")


class DAGBlockchain:
    def __init__(self):
        """
        Initializes the DAG blockchain.
        """
        self.nodes = []  # List of all DAG nodes
        self.edges = {}  # Adjacency list for the DAG

    def add_node(self, aladapter, parent_hashes):
        """
        Adds a new node to the DAG blockchain.
        :param aladapter: Aladapter object.
        :param parent_hashes: List of hashes of parent nodes.
        """
        # Ensure all parent hashes exist
        for parent_hash in parent_hashes:
            if parent_hash not in {node.hash for node in self.nodes}:
                raise ValueError(f"Parent hash {parent_hash} does not exist in the DAG.")

        # Create the new node
        new_node = DAGNode(aladapter, parent_hashes)
        self.nodes.append(new_node)

        # Update the DAG structure
        for parent_hash in parent_hashes:
            if parent_hash not in self.edges:
                self.edges[parent_hash] = []
            self.edges[parent_hash].append(new_node.hash)

        return new_node

    def validate_dag(self):
        """
        Validates the DAG to ensure there are no cycles.
        """
        visited = set()
        stack = set()

        def visit(node_hash):
            if node_hash in stack:
                return False  # Cycle detected
            if node_hash in visited:
                return True

            stack.add(node_hash)
            visited.add(node_hash)
            for child_hash in self.edges.get(node_hash, []):
                if not visit(child_hash):
                    return False
            stack.remove(node_hash)
            return True

        for node in self.nodes:
            if not visit(node.hash):
                return False
        return True

    def __repr__(self):
        return f"DAGBlockchain(nodes={self.nodes})"


# Example Usage
if __name__ == "__main__":
    # Initialize the DAG blockchain
    dag_blockchain = DAGBlockchain()

    # Create initial nodes (genesis nodes with no parents)
    algo1 = Aladapter("Aladapter1", "1.0", "2 years", "2026-01-01", "policy_v1.json", "Regulation A")
    node1 = dag_blockchain.add_node(algo1, [])

    algo2 = Aladapter("Aladapter", "1.0", "3 years", "2027-01-01", "policy_v2.json", "Regulation B")
    node2 = dag_blockchain.add_node(algo2, [])

    # Add dependent nodes
    algo3 = Aladapter("Aladapter1", "2.0", "2 years", "2028-01-01", "policy_v1.json", "Regulation A")
    node3 = dag_blockchain.add_node(algo3, [node1.hash])

    algo4 = Aladapter("Aladapter2", "2.0", "3 years", "2029-01-01", "policy_v2.json", "Regulation B")
    node4 = dag_blockchain.add_node(algo4, [node2.hash])

    # Add a node depending on multiple parents
    algo5 = Aladapter("CombinedAladapter", "1.0", "5 years", "2030-01-01", "policy_combined.json", "Regulation C")
    node5 = dag_blockchain.add_node(algo5, [node3.hash, node4.hash])

    # Validate the DAG
    print(f"Is DAG valid? {dag_blockchain.validate_dag()}")

    # Display the DAG blockchain
    print("DAG Blockchain:")
    for node in dag_blockchain.nodes:
        print(node)
