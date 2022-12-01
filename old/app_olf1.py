# Python program to create Blockchain

# For timestamp
import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask_cors import cross_origin
from blockchainsks import Blockchain

# Creating the Web
# App using flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/', methods=['GET'])
def husseycoin():
    return "This is the Hussey Coin Block Chain"

@app.route('/mine_block', methods=['GET'])
def mine_block():
	#response = {'message': 'A block is MINED',
    #				'index': block['index'],
	#			'timestamp': block['timestamp'],
	#			'proof': block['proof'],
	#			'previous_hash': block['previous_hash']}
	return jsonify({"message":"Mined"}), 200
@app.route("/make_payment",methods=["POST"])

# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
	#response = {'chain': blockchain.chain,
	#			'length': len(blockchain.chain)}
	return jsonify({"meesage":"chain"}), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
	#valid = blockchain.chain_valid(blockchain.chain)
	valid = "hi"
	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
