import os
from hashlib import sha256
import json
import time

from flask import Flask, request
import requests
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()



@app.route('/chain', methods=['GET'])
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
    app.run(debug=True, port=5000)

