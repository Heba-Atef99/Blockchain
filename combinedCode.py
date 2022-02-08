from hashlib import sha256
import json
import time

class node:
    def __init__(self):
        self.branches =[]
        self.mainbranch = self.Blockchain()  
        """
        node will compare the branches and select the longest one Using for loop 
        """
    def receive_block(self):
        """
        
        """

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, owner):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.owner = owner

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self, power):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.power = power
    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0", "first")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)


    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        previous_hash = self.last_block().hash

        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, owner):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
         
        if not self.unconfirmed_transactions and self.power < 10:
            if self.power < 10:
                print("more power needed")
            return False

        
        new_block = Block(index=self.last_block().index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=self.last_block().hash, 
                           owner = owner)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.power = self.power - 10
        self.unconfirmed_transactions = []
        return new_block.index
def main():
    miner1 = Blockchain(50)
    miner2 = Blockchain(30)
    chain1 = [] # no need for both, as we can access the chain from miner.chain
    chain2 = []
    mainbranch = []
    transaction =["alice sends 100 to bob ", "liz sends 100 to z", "carla sends 50 to z", "a sends 40 to h", "A sends 50 to z","h sends 50 to n"]
    for i in range(len(transaction)):
        if miner1.power < 10:
            break
        else:
            miner1.add_new_transaction(transaction[i])
            miner1.mine("miner1")
            chain1.append( miner1.last_block())
            print("miner 1 enetered block " + str(i) + " is " + miner1.last_block().transactions[0])
            #print("power 1  is: " + str(miner1.power))
    for i in range(len(transaction)):
        if miner2.power < 10:
            break
        else:
            miner2.add_new_transaction(transaction[i])
            miner2.mine("miner2")
            chain2.append( miner1.last_block())
            print("miner 2  enetered block " + str(i) + " is " + miner2.last_block().transactions[0])
            #print("power 2  is: " + str(miner2.power))
    if len(miner1.chain) > len(miner2.chain):
        print("miner1 is the winner")
        mainbranch = miner1.chain
        for i in range(len(miner1.chain)):
            print(miner1.chain[i])

if __name__ == "__main__":
    main()