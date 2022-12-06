# Python program to create Blockchain

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify,request,send_file,send_from_directory
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from blockchains.blockchain import Blockchain
from csv_to_db import ImportCSV
from models import CompanyUsers,ContributorUsers 
from bson.objectid import ObjectId # 
import datetime
import hashlib
import shutil
import os
import io
import gridfs
# Creating the Web
# App using flask
app = Flask(__name__)
jwt = JWTManager(app)
importcsv = ImportCSV("CaesarCoinDB")
caesarfs = gridfs.GridFS(importcsv.gridfs)
app.config['JWT_SECRET_KEY'] = "Peter Piper picked a peck of pickled peppers, A peck of pickled peppers Peter Piper picked, If Peter Piper picked a peck of pickled peppers,Where's the peck of pickled peppers Peter Piper picked" #'super-secret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
# Create the object
# of the class blockchain
blockchain = Blockchain()

# Mining a new block
# TODO Sent by Quota Poster
# TODO Sent by Contributor
# TODO Two Factor Authentication
# TODO Allow each device to make local honey pot to send to
@app.route('/quotapostersignup', methods=['POST'])
@cross_origin()
def quotapostersignup():
	# Parameters: {"company":"Google","email":"amari.lawal05@gmail.com","password":"kya63amari"}
	try:
		data = request.get_json()
		companyid = str(hashlib.sha256(data["company"].encode()).hexdigest())
		data["id"] = ObjectId()
		data["companyid"] = companyid
		user = CompanyUsers(**data)
		signupdata = user.to_bson() 
		
		companyid_exists = importcsv.db.quotaposterusers.find_one({"companyid": companyid})
		if companyid_exists:
			return jsonify({"message": "Email already exists"}) ,400
		elif not companyid_exists:
			importcsv.db.quotaposterusers.insert_one(signupdata)
			access_token = create_access_token(identity=signupdata["companyid"])
			callback = {"status": "success","id": str(signupdata["_id"]),"access_token":access_token}
			return callback,200
	except Exception as ex:
		error_detected = {"error": "error occured","errortype":type(ex), "error": str(ex)}
		return error_detected,400
	

@app.route('/quotapostersignin', methods=['POST'])
@cross_origin()
def quotapostersignin():
	# Login API
	# {"company":"Google","password":"kya63amari"}
	try:
		def provide_access_token(login_details):
			email_exists = list(importcsv.db.quotaposterusers.find({"companyid": login_details["companyid"]}))[0]
			encrypted_password =  hashlib.sha256(login_details["password"].encode('utf-8')).hexdigest()
			if email_exists["password"] == encrypted_password:
				access_token = create_access_token(identity=email_exists["companyid"])
				return access_token
			else:
				return "Wrong password"
		login_details = request.get_json()
		companyid = str(hashlib.sha256(login_details["company"].encode()).hexdigest())
		login_details["companyid"] = companyid
		companyid_exists = importcsv.db.quotaposterusers.find_one({"companyid": companyid})
		if companyid_exists:
			access_token = provide_access_token(login_details)
			if access_token == "Wrong password":
				return jsonify({"message": "The username or password is incorrect."}),400
			else:
				return jsonify({"access_token": access_token}), 200
		return jsonify({"message": "The username or password is incorrect."}),400
	
	except Exception as ex:
		return jsonify({"error": f"{type(ex)} {str(ex)}"})
	# Token: JWT Token
	# Parameters: {"company":"<text>" -> "companyid":"<hash>","password":"<text>"}
	# Return: {"access_token":"<text|token>"}
	

@app.route('/contributorsignup', methods=['POST'])
@cross_origin()
def contributorsignup():
	# Token: JWT Token
	# Parameters: {"contributor":"palondomus","email":"amari.lawal@gmail.com","password":"kya63amari"}
	try:
		data = request.get_json()
		contributorid = str(hashlib.sha256(data["contributor"].encode()).hexdigest())
		data["id"] = ObjectId()
		data["contributorid"] = contributorid
		user = ContributorUsers(**data)
		signupdata = user.to_bson() 
		
		contributorid_exists = importcsv.db.contributorusers.find_one({"contributorid": contributorid})
		if contributorid_exists:
			return jsonify({"message": "Email already exists"}) , 400
		elif not contributorid_exists:
			importcsv.db.contributorusers.insert_one(signupdata)
			access_token = create_access_token(identity=signupdata["contributorid"])
			callback = {"status": "success","id": str(signupdata["_id"]),"access_token":access_token}
			return callback,200
	except Exception as ex:
		error_detected = {"error": "error occured","errortype":type(ex), "error": str(ex)}
		return error_detected,400

@app.route('/contributorsignin', methods=['POST'])
@cross_origin()
def contributorsignin():
	# Token: JWT Token
	# Parameters:{"contributor":"palondomus","password":"kya63amari"}
	# Return: {"access_token":"<text|token>"}
	try:
		def provide_access_token(login_details):
			email_exists = list(importcsv.db.contributorusers.find({"contributorid": login_details["contributorid"]}))[0]
			encrypted_password =  hashlib.sha256(login_details["password"].encode('utf-8')).hexdigest()
			if email_exists["password"] == encrypted_password:
				access_token = create_access_token(identity=email_exists["contributorid"])
				return access_token,200
			else:
				return "Wrong password",400
		login_details = request.get_json()
		contributorid = str(hashlib.sha256(login_details["contributor"].encode()).hexdigest())
		login_details["contributorid"] = contributorid
		contributorid_exists = importcsv.db.contributorusers.find_one({"contributorid": contributorid})
		if contributorid_exists:
			access_token = provide_access_token(login_details)
			if access_token == "Wrong password":
				return jsonify({"message": "The username or password is incorrect."}),400
			else:
				return jsonify({"access_token": access_token[0]}), 200
		return jsonify({"message": "The username or password is incorrect."}),400
	
	except Exception as ex:
		return jsonify({"error": f"{type(ex)} {str(ex)}"}),400

# TODO Done by the Quota Poster
@app.route('/create_quota', methods=['POST'])
@cross_origin()
@jwt_required()
def create_quota():
	current_user = get_jwt_identity() 
	if current_user:
		try:
			# TODO Store whether they want send the datasets publicly or privately. 
			# If publicy - will use torrent. if privatly will use dropbox
			# public - Pros | Cons
			# Passive generation of coin for each seeder made for the dataset, so that it can be distributed worldwide
			# Initial contributor will become seeder, then another person can just download it to either use it then become seeder.
			# Flow -> Use dataset -> Become seeder -> Use dataset -> become seeder -> Finally the quota poster will get what they wanted.
			# This means that all datascientists will have accces of the data from all over the world as a shared inititave

			# Private - Pros | Cons
			# If data is confidentital then it can be sent privatel to the quota poster. The contriutor will only generate a fixed one time amount of coin and 
			# others shouldn't have access unless contributor externally distributes.
			# TODO {"company":"<text>","title":"<text>","subject":"<text>","description":"<text>","thumbnail":"<img>","dataquota":"<int>","databaseurlendpoint":"<apiendpoint>"}
			quotaparameters = request.get_json()
			#{"comapny":"","quotas":[{"title":"",""}]}
			companyid = current_user #str(hashlib.sha256(quotaparameters["company"].encode()).hexdigest())
			companyid_exists = importcsv.db.quotaposterusers.find_one({"companyid": companyid})
			if companyid_exists:
				quotaid_exists = importcsv.db.quotas.find_one({"companyid": companyid})
				if quotaid_exists:
					companyquota = list(importcsv.db.quotas.find({"companyid": companyid}))[0]
					#print(companyquota)
					#print(quotaparameters["quotas"][0] )
					hashsetup = quotaparameters["quotas"][0]["title"]
					hashvalue = str(hashlib.sha256(hashsetup.encode()).hexdigest())
					quotaparameters["quotas"][0]["quotahashvalue"] = hashvalue
					del companyquota["_id"]
					if quotaparameters["quotas"][0] in companyquota["quotas"]:
						return {"message":"quota already exists"}
					elif quotaparameters["quotas"][0] not in companyquota["quotas"]:

						companyquota["quotas"].append(quotaparameters["quotas"][0])
						importcsv.db.quotas.replace_one({"companyid": companyid},companyquota)
						return {"message":"quota added"},200


				
				elif not quotaid_exists:
					#del quotaparameters["company"]
					quotaparameters["companyid"] = current_user
					hashsetup = quotaparameters["quotas"][0]["title"]
					hashvalue = str(hashlib.sha256(hashsetup.encode()).hexdigest())
					quotaparameters["quotas"][0]["quotahashvalue"] = hashvalue
					importcsv.db.quotas.insert_one(quotaparameters)
					return {"message":"quota created"},200
			elif not companyid_exists:
				return {"error":f"{current_user} is not quotaposter"},400
		except Exception as ex:
			return {"error":f"{type(ex)},{ex}"},400
		
# TODO Fetched for Quota on website
@app.route('/get_quotas', methods=['GET'])
@cross_origin()
def get_quotas():
	#current_user = get_jwt_identity() 
	#if current_user:
	company = request.args.get("company")
	try:
		companyid = str(hashlib.sha256(company.encode()).hexdigest())
		quotaid_exists = importcsv.db.quotas.find_one({"companyid": companyid})
		if quotaid_exists:
			companyquota = list(importcsv.db.quotas.find({"companyid": companyid}))[0]
			#print(companyquota)
			del companyquota["_id"]
			return companyquota,200
		elif not quotaid_exists:
			return {"error":"quotas doesn't exist"},200
		
	except Exception as ex:
		return {"error":f"{type(ex)},{ex}"},400

	# TODO {"companyid":"<hash>","company":"<text>","title":"<text>","subject":"<text>","description":"<text>","thumbnail":"<img>","dataquota":"<int>","databaseurlendpoint":"<apiendpoint>"}
	# TODO return {"company":"<text>","title":"<text>","subject":"<text>","description":"<text>","thumbnail":"<img>","dataquota":"<int>"}

	pass
# TODO Sent by Contributor
@app.route('/store_quota_contribution_request', methods=['POST'])
@cross_origin()
@jwt_required()
def store_quota_contribution_request():
	current_user = get_jwt_identity() 
	if current_user:
		try:
			quota_request = request.get_json()
			companyid = str(hashlib.sha256(quota_request["company"].encode()).hexdigest())
			quota_title = str(hashlib.sha256(quota_request["quota"].encode()).hexdigest())
			
			quota_poster_exists = importcsv.db.quotaposterusers.find_one({"companyid": companyid})
			if quota_poster_exists:
				quota_request_exists = importcsv.db.quota_contribution_requests.find_one({"companyid": companyid})
				if quota_request_exists:
					quota_request_db = importcsv.db.quota_contribution_requests.find({"companyid": companyid})[0]
					try:
						if current_user in quota_request_db["quotas"][quota_title]:
							return {"message":"quota contribution from this user already exists for this company."}
						elif current_user not in quota_request_db["quotas"][quota_title]:
							quota_request_db["quotas"][quota_title].append(current_user)
							importcsv.db.quota_contribution_requests.replace_one({"companyid": companyid},quota_request_db)
							return {"message":"quota contribution request add."},200
					except KeyError as kex:
						# Maybe do it so that it checks from the quota collection.
						quota_request_db["quotas"].update({quota_title:[current_user]})
						importcsv.db.quota_contribution_requests.replace_one({"companyid": companyid},quota_request_db)
						return {"message":"new quota title added"},200		
				
				elif not quota_request_exists:
					importcsv.db.quota_contribution_requests.insert_one({"companyid":companyid,"quotas":{quota_title:[current_user]}})
					return {"message":"quota contribution request created."},200
			elif not quota_poster_exists:
				return {"message":"company doesn't exist"},200		

		except Exception as ex:
			return {"error":f"{type(ex)},{ex}"},400

	# {"companyid"}
	# Token: JWT Token
	# Parameters: {"companyid":"<hash>","userid":"<hash>",}
	# Store DB - pending_quota_requests: {"companyid":"<hash>","userid":"<hash>","permision":"pending"}

#	pass
# TODO Sent by Quota Poster
@app.route('/verify_quota_contribution', methods=['POST'])
@cross_origin()
@jwt_required()
def verify_quota_contribution():
	current_user = get_jwt_identity() 
	if current_user:
		try:
			quota_choice = request.get_json()
			contributor = str(hashlib.sha256(quota_choice["contributor"].encode()).hexdigest())
			choice = quota_choice["choice"].lower()
			quota_title = str(hashlib.sha256(quota_choice["quota_title"].encode()).hexdigest())
			quota_request_exists = importcsv.db.quota_contribution_requests.find_one({"companyid": current_user})
			if quota_request_exists:
				quota_request_db = importcsv.db.quota_contribution_requests.find({"companyid": current_user})[0]
				if contributor in quota_request_db["quotas"][quota_title]:
					# Acceptence part
					if choice == "y":
						quota_accepted_exists = importcsv.db.quotas_accepted.find_one({"companyid": current_user})
						if not quota_accepted_exists:
							importcsv.db.quotas_accepted.insert_one({"companyid":current_user,quota_title:{"contributors":[contributor]}})
							quota_request_db["quotas"][quota_title].remove(contributor)
							importcsv.db.quota_contribution_requests.replace_one({"companyid": current_user},quota_request_db)
							return {"message":"contributor was created"},200
						elif quota_accepted_exists:						
							try:
								quota_accepted_db = importcsv.db.quotas_accepted.find({"companyid": current_user})[0]
								if contributor not in quota_accepted_db[quota_title]["contributors"]:
									quota_accepted_db[quota_title]["contributors"].append(contributor)
									importcsv.db.quotas_accepted.replace_one({"companyid": current_user},quota_accepted_db)
									quota_request_db["quotas"][quota_title].remove(contributor)
									importcsv.db.quota_contribution_requests.replace_one({"companyid": current_user},quota_request_db)
									return {"message":"contributor was accepted."},200
								elif contributor in quota_accepted_db[quota_title]["contributors"]:
									return {"message":"contributor already accepted."},200
							except KeyError as kex:
								return {"error":"quota does not exist"},200
					# Rejection Part
					elif choice == "n":
						quotas_rejected_exists = importcsv.db.quotas_rejected.find_one({"companyid": current_user})
						if not quotas_rejected_exists:
							importcsv.db.quotas_rejected.insert_one({"companyid":current_user,quota_title:{"contributors":[contributor]}})
							quota_request_db["quotas"][quota_title].remove(contributor)
							importcsv.db.quota_contribution_requests.replace_one({"companyid": current_user},quota_request_db)
							return {"message":"contributor rejection was created"},200
						elif quotas_rejected_exists:		
							try:
								quota_rejected_db = importcsv.db.quotas_rejected.find({"companyid": current_user})[0]
								if contributor not in quota_rejected_db[quota_title]["contributors"]:
									quota_rejected_db[quota_title]["contributors"].append(contributor)
									importcsv.db.quotas_rejected.replace_one({"companyid": current_user},quota_rejected_db)
									quota_request_db["quotas"][quota_title].remove(contributor)
									importcsv.db.quota_contribution_requests.replace_one({"companyid": current_user},quota_request_db)
									return {"message":"contributor was rejected."},200
								elif contributor in quota_rejected_db[quota_title]["contributors"]:
									return {"message":"contributor already rejected."},200
							except KeyError as kex:
								return {"error":"quota does not exist"},200


						#importcsv.db.quotas_rejected.insert_one({"companyid":current_user,quota_title:{"contributors":[contributor]}})
						#quota_request_db["quotas"][quota_title].remove(contributor)
						#importcsv.db.quota_contribution_requests.replace_one({"companyid": current_user},quota_request_db)
						#return {"message":"quota was rejected."},200

				elif contributor not in quota_request_db["quotas"][quota_title]:
					return {"message":"quota doesn't exist"},200
			elif not quota_request_exists:
				return {"message":"company doesn't exist"},200
		except Exception as ex:
			return {"error":f"{type(ex)},{ex}"},400

	# Remove DB pending_quota_requests: {"companyid":"<hash>","userid":"<hash>","permision":"pending"}
	# Store DB accepted_quotas: {"companyid":"<hash>","userid":"<hash>","permision":"accepted"}
# Upload data to mine endpoint using multipart -> -> get response
# TODO This is done by the main contributor
@app.route('/upload_torrent_file', methods=['POST'])
@cross_origin()
def upload_torrent_file():
	direct = "CaesarTorrents"

	if request.method == 'POST':
		f = request.files['torrentfile']
		if direct in os.listdir():
			shutil.rmtree(direct)
		if direct not in os.listdir():
			os.mkdir(direct)
		buffer_filename = secure_filename(f.filename)
		f.save(os.path.join(direct, buffer_filename))

		with open(f"{direct}/{f.filename}","rb") as fb:
			data = fb.read()
		caesarfs.put(data,filename=f.filename)

		return {"message":"caesar torrent file was uploaded."}#send_from_directory(direct,f.filename) #send_file(f"{direct}/{f.filename}",as_attachment=True)
		
	# {"current_user(jwt)":"contributor","company":"","quota","","torrentfile":"<torrentfile>"}
	# Store torrent file in database
	# Coin will be generated after the torrent file has been torrented.
@app.route('/download_torrent_file', methods=['POST'])
@cross_origin()
def download_torrent_file():
	direct = "CaesarTorrentsDownload"

	if request.method == 'POST':
		torrentdetails = request.get_json()
		if direct in os.listdir():
			shutil.rmtree(direct)
		if direct not in os.listdir():
			os.mkdir(direct)
		filedata = importcsv.gridfs.fs.files.find_one({"filename":torrentdetails["torrentfile"]})
		my_id = filedata["_id"]
		output_Data = caesarfs.get(my_id).read()
		output = open(f"{direct}/{torrentdetails['torrentfile']}","wb")
		output.write(output_Data)
		output.close()
		print("download completed")

		return send_from_directory(direct,torrentdetails['torrentfile']) #send_file(f"{direct}/{f.filename}",as_attachment=True)
		
	# {"current_user(jwt)":"contributor","company":"","quota","","torrentfile":"<torrentfile>"}
	# Store torrent file in database
	# Coin will be generated after the torrent file has been torrented.

# TODO This is done by the quota poster
@app.route('/start_torrent', methods=['POST'])
@cross_origin()
@jwt_required()
def start_torrent():

	try:
		#seeder_info = request.get_json() # {"current_user(jwt)":"<contributor>","company":"","quota":"","torrentfile(name)":""}
		#importcsv.gridfs.fs
		#importcsv.db.quotatorrentpending.f
		pass
		
		
	except Exception as ex:
		return {"error":f"{type(ex)},{ex}"}
	# Store to pendingtorrents collection
	# TODO Long term worker - A long term script worker uses the webtorrent to get the torrentfile from the database and starts torrenting.
	# When it has finished the torrent the larger reward transaction is added to the blockchain then mined for the main contributor and other contributors. 
	# Then they can see the balance of the wallet

	pass

# TODO This is done by the contributor others
@app.route('/set_torrent_seeder', methods=['POST'])
@cross_origin()
@jwt_required()
def set_torrent_seeder():
	#seeder_info = request.get_json() # {"current_user(jwt)":"<contributor>","company":"","quota","" -> "<torrent file linked to quota in database>"}

	pass

@app.route('/send_data_quota', methods=['POST'])
@cross_origin()
def send_data_quota():
	pass



# Run the flask server locally
app.run(debug=True,host='127.0.0.1', port=5000)
