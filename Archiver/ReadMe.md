<archiver.py> is an a python script for a blockchain that records datasets and the outputs of AI algorithms. This blockchain is designed to ensure transparency, traceability, and immutability in the process of recording AI operations.

Key Features
1.    AI Operation Details:
        - Algorithm Name: Name of the AI algorithm used.
        - Dataset: Dataset associated with the operation.
        - Output: Result produced by the algorithm.
        - Parameters: Parameters used in the algorithm.
2.    Mining and Proof-of-Work:
        - Ensures immutability of records using a hash-based proof-of-work mechanism.
3.    Validation:
        - Checks the integrity of the blockchain by validating hashes.
4.    Extensibility:
        - Add more metadata fields to the AIOperation class as needed.

How to Use
1.    Run the Code:
        - Save the script as archiver.py.
        - Execute with python archiver.py.
2.    Add Operations:
        - Use add_operation to log datasets and outputs.
3.    Validate Blockchain:
        - Use is_chain_valid to check the blockchain’s integrity.
