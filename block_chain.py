from hashlib import sha256
import json
from multiprocessing import Condition
import time

class Node:
    def __init__(self, owner):
        self.branches =[]
        self.owner = owner
        self.main_branch = Blockchain(self.owner)  
        """
        node will compare the branches and select the longest one Using for loop 
        """
    def receive_block(self, block):
        flag=False
        print("inside" + block.transactions[0])
        for i in range(len(self.branches)):
            # print("inside" + str(i) + block.transctions[0])
            # print(self.branches[i].chain[0].owner)
            # print(self.branches[i].chain[0].transactions[0])
            

            if(block.owner)==self.branches[i].chain[0].owner:
                flag=True
                proof = self.branches[i].proof_of_work(block)
                # print("add blk 1")
                self.branches[i].add_block(block, proof)

        if flag == False:
            new_blockchain = Blockchain(block.owner)
            proof = new_blockchain.proof_of_work(block)
            # print("add blk 2")
            new_blockchain.add_block(block, proof)
            # print(flag2)
            # breakpoint()
            self.branches.append(new_blockchain)
        
        print(len(self.branches[0].chain))
        return flag

        
    def get_max_branch(self):
        max_branch = self.branches[0]
        for i in range(1, len(self.branches)):
            if len(max_branch.chain) < len(self.branches[i].chain):
                max_branch =  self.branches[i]
        return max_branch
    
    """ 
    """   
    def verify_max_branch(self,max_b):
        max_branch = max_b
        is_there_max = False
        if len(self.branches) == 1:
            return True
            
        for i in range(len(self.branches)):
            if abs((len(max_branch.chain) - len(self.branches[i].chain)))>=4:
                max_branch = max_branch if  (len(max_branch.chain) > len(self.branches[i].chain)) else   self.branches[i]
                is_there_max = True
        max_b = max_branch
        return is_there_max     

    # check longest chain function
    def choose_longest_chain(self):
        while True:
            max_branch = self.get_max_branch()
            Condition = self.verify_max_branch(max_branch)
            if Condition == True:
                break
        #self.main_branch.extend
        for i in range(len(max_branch.chain)):
            proof = self.main_branch.proof_of_work(max_branch.chain[i])
            # print("add blk 3")
            self.main_branch.add_block(max_branch.chain[i], proof)

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

    def __init__(self, owner):
        self.unconfirmed_transactions = []
        self.chain = []
        self.owner = owner
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 1, "0", self.owner)
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
        # print("inside" + block.transactions[0])

        previous_hash = self.last_block().hash
        # print(previous_hash)
        # print(block.previous_hash)

        if previous_hash != block.previous_hash:
            return False

        # print(self.is_valid_proof(block, proof))
        # breakpoint()

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

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False


        new_block = Block(index=self.last_block().index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=self.last_block().hash, 
                          owner = self.owner)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index

def main():

    # for one miner, and one user create blocks then send it to the user using receive block.
    print("hello world")
    miner1 = Blockchain("miner1")
    user1 = Node("user1")
    #transaction =({"t": "alice sends 100 to bob "}, {"t":"alice sends 100 to z"},{"t":"alice sends 100 to z"}, {"t":"a sends 40 to h"}, {"t":"A sends 50 to z"})
    transaction =["alice sends 100 to bob ", "alice sends 100 to z", "alice sends 100 to z", "a sends 40 to h", "A sends 50 to z"]
    for i in range(5):
        miner1.add_new_transaction(transaction[i])
        block = miner1.mine()
        user1.receive_block(miner1.last_block())

    print(len(user1.branches[0].chain))
    for i in range(len(user1.main_branch.chain)):
        print("user first received block is " + user1.main_branch.chain[i].transactions[0])
    
if __name__ == "__main__":
    main()