import os
from hashlib import sha256
import json
import time

from flask import Flask, request
from flask_cors import cross_origin
import requests


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        A function to generate genesis block and appends it to
        the chain. The block has index 0, previous_hash as 0, and
        a valid hash.
        """
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
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
        previous_hash = self.last_block.hash

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

    def add_new_transaction(self,sender,recipient,amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        return new_block.index
    def getBalance(self,walletAddress):
        balance = 0
        with open("blockchain.json","r") as f:
            chain = json.load(f)["chain"]
        print(chain)
        for block in chain:
            if block["previous_hash"] == "" :
                #dont check the first block
                continue 
			#print(block)
            for transaction in block["transactions"]:
                if transaction["sender"] == walletAddress:
                    balance -= transaction["amount"]
                if transaction["recipient"] == walletAddress:
                    balance += transaction["amount"]
        return balance


app = Flask(__name__)
blockchain = Blockchain()



@app.route('/chain', methods=['GET'])
@cross_origin()
def get_chain():

    chain_data = []
    if "blockchain.json" in os.listdir():
        with open("blockchain.json","r") as f:
            blockchain_file = json.load(f)
        return blockchain_file
    elif "blockchain.json" not in os.listdir():
        for ind,block in enumerate(blockchain.chain):
            chain_data.append(block.__dict__)
        return {"length": len(chain_data),"chain": chain_data}
    
    
    
@app.route('/mine_block', methods=['POST'])
@cross_origin()
def mine_block():
    minerinfo  = request.get_json()
    try:
        miner = minerinfo["miner"]
        reward = 5 #minerinfo["amount"]
    except KeyError as kex:
        return {"error":r"miner:<miner>,amount:<amount>"}
    blockchain.add_new_transaction("System",miner,reward)
    blockchain.mine()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    blockchain_response = {"length": len(chain_data),"chain": chain_data}
    with open("blockchain.json","w+") as f:
        json.dump(blockchain_response,f)
    return json.dumps(blockchain_response)


@app.route('/make_transaction', methods=['POST'])
@cross_origin()
def make_transaction():
    senderinfo  = request.get_json()
    try:
        sender = senderinfo["sender"]
        recipient = senderinfo["recipient"]
        amount = senderinfo["amount"]
    except KeyError as kex:
        return {"error":r"sender:<sender>,recipient:<recipient>,amount:<amount>"}
    blockchain.add_new_transaction(sender,recipient,amount)
    return {"message":"transaction has been made."}

@app.route('/get_balance', methods=['POST'])
@cross_origin()
def get_balance():
    userinfo  = request.get_json()
    try:
        userbalancename = userinfo["user"]

    except KeyError as kex:
        return {"error":r"sender:<sender>,recipient:<recipient>,amount:<amount>"}
    balance = blockchain.getBalance(userbalancename)
    print(balance)
    return {"balance":{userbalancename:balance}}



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)

