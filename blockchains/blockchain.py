import hashlib
import datetime
import json
class Blockchain:
	# This function is created
	# to create the very first
	# block and set its hash to "0"
	def __init__(self):
		self.chain = []
		# TODO Read chain from json file
		# TODO Store the mining difficulty somwhere in the/a json file
		self.difficulty = 5
		self.pending_transactions = []
		self.reward = 10
		self.difficultyIncrement = 0
		self.hashval = ""
		self.mine_block("Genesis",proof=1, previous_hash='0')

	def calculateHashMine(self, data, timeStamp, difficultyIncrement):
		data = str(data) + str(timeStamp) + str(difficultyIncrement)
		data = data.encode()
		hash = hashlib.sha256(data)
		return hash.hexdigest()
		
	@property
	def last_block(self):
		return self.chain[-1]

	def new_transaction(self, sender, recipient, amount):
		transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
		self.pending_transactions.append(transaction)
		return self.last_block['index'] + 1

	# This function is created
	# to add further blocks
	# into the chain
	def mine_block(self,minerRewardAddress,proof,previous_hash):
		reward_transaction = {
            'sender': "System",
            'recipient': minerRewardAddress,
            'amount': self.reward
        }
		#rewardTrans = Transaction(,minerRewardAddress,self.reward)
		timeStamp = str(datetime.datetime.now())
		#if transaction_mode == 0:
			# TODO Data quota collection mining algorithm, provide minimum quota to mine
		self.pending_transactions.append(reward_transaction)
		#if transaction_mode == 1: # In transaction mode.
			# TODO Calculate cryptographic hash to obtain the transaction.
		difficultyCheck = "9" * self.difficulty
		self.hashval = self.calculateHashMine(self.pending_transactions, timeStamp,self.difficultyIncrement)
		while self.hashval[:self.difficulty] != difficultyCheck:
			self.hashval = self.calculateHashMine(self.pending_transactions, timeStamp,self.difficultyIncrement)
			self.difficultyIncrement = self.difficultyIncrement + 1 
		

			pass
		
		block = {'index': len(self.chain) + 1,
				'timestamp': timeStamp,
				'transactions': self.pending_transactions,
				'proof': proof,
				'previous_hash': previous_hash}

		self.pending_transactions = []
		self.chain.append(block)
		return block
	
	# This function is created
	# to display the previous block
	def print_previous_block(self):
		return self.chain[-1]
	
	# This is the function for proof of work
	# and used to successfully mine the block
	def proof_of_work(self, previous_proof):
		new_proof = 1
		check_proof = False
		
		while check_proof is False:
			hash_operation = hashlib.sha256(
				str(new_proof**2 - previous_proof**2).encode()).hexdigest()
			if hash_operation[:5] == '00000':
				check_proof = True
			else:
				new_proof += 1
				
		return new_proof

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		#print(encoded_block)
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1
		
		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False
			
			previous_proof = previous_block['proof']
			proof = block['proof']
			hash_operation = hashlib.sha256(
				str(proof**2 - previous_proof**2).encode()).hexdigest()
			
			if hash_operation[:5] != '00000':
				return False
			previous_block = block
			block_index += 1
		
		return True
	def getBalance(self,walletAddress):
		balance = 0
		for block in self.chain:
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
	def mine_procedure(self,minerRewardAddress):
		previous_block = self.print_previous_block()
		previous_proof = previous_block['proof']
		proof = self.proof_of_work(previous_proof)
		previous_hash = self.hash(previous_block)
		block = self.mine_block(minerRewardAddress,proof, previous_hash)
		response = {'message': 'A block is MINED',
			'index': block['index'],
			'timestamp': block['timestamp'],
			'transactions': block["transactions"],
			'proof': block['proof'],
			'previous_hash': block['previous_hash']}
		return response
if __name__ == "__main__":
	print(type(hash("Hello")))
	blockchain = Blockchain()
	st = datetime.datetime.now()
	t1 = blockchain.new_transaction("Satoshi", "Mike", 5)
	t2 = blockchain.new_transaction("Mike", "Satoshi", 1)
	t3 = blockchain.new_transaction("Satoshi", "Hal Finney", 5)
	print(t1)


	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	response = blockchain.mine_procedure("Hal Finney")
	#print(response)
	balance = blockchain.getBalance("Hal Finney")
	print(f"Satoshi Balance: {balance}")



	end = datetime.datetime.now()
	print(end- st)