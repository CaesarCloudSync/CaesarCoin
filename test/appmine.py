@app.route('/send_data_quota', methods=['POST'])
@cross_origin()
def send_data_quota():

	pass
# TODO Sent by company saying whether the data is okay or not
@app.route('/data_quota_quality_verified', methods=['POST'])
@cross_origin()
def data_quota_quality_verified():
	# TODO Multipart sending

	pass
@app.route('/mine_data_quota_block', methods=['POST'])
@cross_origin()
def mine_block():
	# TODO Multipart sending
	# send to company
	try:
		caesarcryptoname = request.get_json()
		response = blockchain.mine_procedure(caesarcryptoname["caesarcryptoname"],transaction_mode=0)
		return jsonify(response), 200
	except Exception as ex:
		return jsonify({"error":f"{type(ex)},{ex}"}),400
@app.route('/make_transaction', methods=['POST'])
@cross_origin()
def make_transaction():
	try:
		caesarcryptodata = request.get_json()
		t1 = blockchain.new_transaction(caesarcryptodata["sender"], caesarcryptodata["recipient"], 5)
		response = blockchain.mine_procedure(caesarcryptodata["recipient"],transaction_mode=1)
		return jsonify(response), 200
	except Exception as ex:
		return jsonify({"error":f"{type(ex)},{ex}"}),400
@app.route('/get_balance', methods=['GET'])
@cross_origin()
def get_balance():
	# JWT Token
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200
# Display blockchain in json format
# Admin: Permission
@app.route('/get_chain', methods=['GET'])
@cross_origin()
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200


# Check validity of blockchain
@app.route('/valid', methods=['GET'])
@cross_origin()
def valid():
	valid = blockchain.chain_valid(blockchain.chain)
	
	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200