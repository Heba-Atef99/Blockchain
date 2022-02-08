from ast import And
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
    difficulty = 4
    #print("N: " +str(difficulty) )

    def __init__(self, power, owner):
        self.unconfirmed_transactions = []
        self.chain = []
        self.owner = owner
        self.newchain=[]
        self.counter = 0
        self.speed = 0
        self.create_genesis_block()
        self.power = power
        self.branching_status=False
    
            
    def get_max_branch(self):
        max_branch = self.newchain[0]
        for i in range(1, len(self.newchain)):
            if len(max_branch) < len(self.newchain[i]):
                max_branch =  self.newchain[i]
        return max_branch
 
    def verify_max_branch(self,max_b):
        max_branch = max_b
        is_there_max = False
        if len(self.newchain) == 1:
            return True
            
        for i in range(len(self.newchain)):
            if abs((len(max_branch) - len(self.newchain[i])))>=4:
                max_branch = max_branch if  (len(max_branch) > len(self.newchain[i])) else   self.newchain[i]
                is_there_max = True
        max_b = max_branch
        return is_there_max  

    def choose_longest_chain(self):
        
        max_branch = self.get_max_branch()
        Condition = self.verify_max_branch(max_branch)
        if Condition == True:       
           #self.main_branch.extend
           self.chain.extend(max_branch)
           self.newchain=[]
                 

    def recieve_block(self,block):
        if self.branching_status:
            foundchain=False
            for c in self.newchain:
                if c[-1].owner==block.owner:
                    block.previous_hash = c[-1].hash
                    proof = self.proof_of_work(block)      
                    self.add_block_newchain(block,proof,c)
                    foundchain=True
                    break

            if foundchain==False:
                ch = self.newchain[1]
                block.previous_hash = ch[-1].hash
                proof = self.proof_of_work(block)      
                self.add_block_newchain(block,proof,self.newchain[1])    
            self.choose_longest_chain()
        else:
            if block.index > self.last_block().index:
                proof = self.proof_of_work(block)      
                self.add_block(block, proof)

            else:
              self.branching_status=True
              if len(self.newchain) == 0:
                    ch=[]
                    block.previous_hash = self.chain[block.index-1].hash
                    proof = self.proof_of_work(block)      
                    self.add_block_newchain(block, proof, ch)
                    self.newchain.append(ch)
                    
                    sh=[]
                    for i in range(block.index,len(self.chain)):
                        sh.append(self.chain[i])
                        
                    del self.chain[block.index:len(self.chain)]
                    self.newchain.append(sh)
                  
    def broadcast(self,block,group):
        for i in range(len(group)):
            current_chain=group[i]
            if block.owner!=current_chain.owner:
                current_chain.recieve_block(block)
        
        # for i in range(len(group)):
        #     current_chain=group[i]
        #     if block.owner!=current_chain.owner or block.index>current_chain.last_block().index or current_chain.chain[block.index].transactions !=block.transactions:
        #         current_chain.recieve_block(block)

   
    def add_block_newchain(self, block, proof, newchain):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of latest block
          in the chain match.
        """
        if len(self.newchain) == 0 :
            # block.previous_hash = self.chain[block.index-1].hash
            previous_hash = self.chain[block.index-1].hash
        
        else:
            # block.previous_hash = newchain[-1].hash
            previous_hash = newchain[-1].hash
        
        if previous_hash != block.previous_hash:
            # print("previous_hash" + previous_hash)
            # print("block.previous_hash" + block.previous_hash)
            return False

        # print("jjjjjj")

        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        newchain.append(block)
        
        return True

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], 0, "0", "first")
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
        #print("the computed hash is: " + computed_hash)
        #print("the block nonce is: " + str(block.nonce))
        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self, owner, index):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
         
        if not self.unconfirmed_transactions and self.power < 10:
            if self.power < 10:
               print("more power needed")
            return False

        
        new_block = Block(index=index,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=self.last_block().hash, 
                           owner = owner)
        start = time.time()
        proof = self.proof_of_work(new_block)
        end = time.time()
        #print("The time taken to solve the Puzzle in Sec: " + str(end - start))
        if index == self.last_block().index + 1:     
            self.add_block(new_block, proof)

        else:
            # new_block.previous_hash = 
            self.recieve_block(new_block)

        self.power = self.power - 10
        self.unconfirmed_transactions = []
        return new_block

# function to calculate the speed
def calculate_speed(counter, power):
    speed = counter / power # msh 3arfa htkon kda wla power / speed
    return speed

def main():
    miner1 = Blockchain(40, "miner1")
    miner2 = Blockchain(40, "miner2")
    miner3_attacker = Blockchain(60, "miner3_attacker")
    group=[]
    group.append(miner1)
    group.append(miner2)
    group.append(miner3_attacker)
    transaction = ["Alice sends 100 to Bob ", "Liz sends 100 to Nermeen", "Carla sends 50 to Alaa", "Hager sends 40 to Ahmed", "Hadeer sends 50 to Salma","Heba sends 50 to Mariam"]

    for i in range(len(transaction)):
        """
        if miner1.power < 10:
            break

        else:
            if i % 2 != 0:
                miner1.add_new_transaction(transaction[i])
                miner1.mine("miner1", miner1.last_block().index+1)
                miner1.broadcast(miner1.last_block(),group)
                # print("miner 1 enetered block " + str(i+1) + " is " + miner1.last_block().transactions[0])

            else:
                miner2.add_new_transaction(transaction[i])
                miner2.mine("miner2", miner2.last_block().index+1)
                miner2.broadcast(miner2.last_block(),group)
                # print("miner 2 enetered block " + str(i+1) + " is " + miner2.last_block().transactions[0])
        """
        if i % 2 != 0 and miner1.power > 10:
            miner1.add_new_transaction(transaction[i])
            miner1.mine("miner1", miner1.last_block().index+1)
            miner1.broadcast(miner1.last_block(),group)
            # print("miner 1 enetered block " + str(i+1) + " is " + miner1.last_block().transactions[0])
            miner1.counter = miner1.counter + 1

        else:
            if miner2.power < 10:
                break
            else:
                miner2.add_new_transaction(transaction[i])
                miner2.mine("miner2", miner2.last_block().index+1)
                miner2.broadcast(miner2.last_block(),group)
                # print("miner 2 enetered block " + str(i+1) + " is " + miner2.last_block().transactions[0])
                miner2.counter = miner2.counter + 1
    miner3_attacker.add_new_transaction("Hadeer sends 1000 to Salma")
    new_block = miner3_attacker.mine("miner3_attacker", 5)
    miner3_attacker.broadcast(new_block, group)

    for i in range(5):
        if miner3_attacker.power > 10:
            miner3_attacker.add_new_transaction("Hadeer sends"+ str(100*i+50)+"to Salma")
            new_block = miner3_attacker.mine("miner3_attacker", i+6)
            miner3_attacker.broadcast(new_block, group)
            miner3_attacker.counter = miner3_attacker.counter + 1
        else:
            break
    #miner3_attacker.choose_longest_chain()
    i = 0
    miner1.speed = calculate_speed(miner1.counter, miner1.power)
    miner2.speed = calculate_speed(miner2.counter, miner2.power)
    miner3_attacker.speed = calculate_speed(miner3_attacker.counter, miner3_attacker.power)
    print("miner1 speed is " + str(miner1.speed))
    print("miner2 speed is " + str(miner2.speed))
    #print("attacker counter is: " + str(miner3_attacker.counter) )
    #print("attacker power is: " + str(miner3_attacker.power) )
    print("miner3_attacker speed is " + str(miner3_attacker.speed))

    for b in miner1.chain:
        if i == 0 : 
            i = 1
            continue
         
        print("miner 1 Main chain block is " + b.transactions[0] + "with index " + str(b.index))

    print("****************************")
    # for ch in miner1.newchain:
    #     for b in ch:
    #         print("miner 1 branch " + str(i) + " block is " + b.transactions[0] + "with index " + str(b.index))

    #         i = 2
        #print("***********lllllll*****************")

    #print("\n")
    #########################################
    i = 0
    for b in miner2.chain:
        if i == 0 : 
            i = 1
            continue
         
        print("miner 2 Main chain block is " + b.transactions[0] + "with index " + str(b.index))

    print("****************************")
    for ch in miner2.newchain:
        for b in ch:
            print("miner 2 branch " + str(i) + " block is " + b.transactions[0] + "with index " + str(b.index))

            i = 2
        #print("***********lllllll*****************")

    #print("\n")
    #########################################
    i = 0
    for b in miner3_attacker.chain:
        if i == 0 : 
            i = 1
            continue
         
        print("miner 3 Main chain block is " + b.transactions[0] + "with index " + str(b.index))

    print("****************************")
    # for ch in miner3_attacker.newchain:
    #     for b in ch:
    #         print("miner 3 branch " + str(i) + " block is " + b.transactions[0] + "with index " + str(b.index))

    #         i = 2
        #print("***********lllllll*****************")
    # cc= miner3_attacker.get_max_branch(); 
    # for b in cc: 
    #     print("cc " + b.transactions[0] + "with index " + str(b.index))

if __name__ == "__main__":
    main()