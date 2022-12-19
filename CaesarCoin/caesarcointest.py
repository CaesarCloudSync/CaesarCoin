import unittest
import requests
import os
class QuotaSetupContributionRequestTest(unittest.TestCase):
    def test_quota_contribution_request(self):
        companyname = "Google"
        contributorname = "palondomus"
        quotaname = "Googleman Text Classification"
        choice = "y"
        quotasigninbool = False
        contributorsigninbool = False 
        quotapostersignupresp  = requests.post("http://127.0.0.1:5000/quotapostersignup",json={"company":companyname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
        quotapostersignup = quotapostersignupresp.json()
        print(quotapostersignup)
        try:
            self.assertEqual(200,  quotapostersignupresp.status_code)
        except AssertionError as aex:
            quotapostersignupresp  = requests.post("http://127.0.0.1:5000/quotapostersignin",json={"company":companyname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
            quotapostersignup = quotapostersignupresp.json()
            self.assertEqual(200,  quotapostersignupresp.status_code)

        
        contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignup",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
        contributorsignup = contributorsignupresp.json()
        try:
            self.assertEqual(200,  contributorsignupresp.status_code)
        except AssertionError as aex:
            contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignin",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
            contributorsignup = contributorsignupresp.json()
            self.assertEqual(200,  contributorsignupresp.status_code)
            

        # quotaprivilege - public | private
        create_quota = requests.post("http://127.0.0.1:5000/create_quota",json={"quotas":[{"quotaprivelege":"public","title":quotaname,"subject":"Need Data for text classifcation","description":"The dataset has to be in text | intent format.","thumbnail":"<img>","dataquota":"300000","databaseurlendpoint":"https://amari.dev"}]},headers={'Authorization': 'Bearer ' + quotapostersignup["access_token"]}).json()
        print(create_quota)
        self.assertNotEqual("error", list(create_quota.keys())[0])
        #self.assertEqual(200,  create_quota.status_code)
        get_quotas = requests.get("http://127.0.0.1:5000/get_quotas",params={"company":companyname}).json()
        print(get_quotas)
        self.assertNotEqual("error", list(get_quotas.keys())[0])
        #self.assertEqual(200,  get_quotas.status_code)
        #print(contributorsignup)
        #print(contributorsignup["access_token"][0])
        store_quota_contribution_request = requests.post("http://127.0.0.1:5000/store_quota_contribution_request",json={"company":companyname,"quota":quotaname},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        
        self.assertNotEqual("error", list(store_quota_contribution_request.keys())[0])
        #self.assertEqual(200,  store_quota_contribution_request.status_code)
        verify_quota_contribution = requests.post("http://127.0.0.1:5000/verify_quota_contribution",json={"contributor":contributorname,"quota_title":quotaname,"choice":choice},headers={'Authorization': 'Bearer ' + quotapostersignup["access_token"]}).json()
        #print(verify_quota_contribution)
        self.assertNotEqual("error", list(verify_quota_contribution.keys())[0])
        #self.assertEqual(200,  verify_quota_contribution.status_code)
        print(verify_quota_contribution)
        print("Quota creation and Contribution unittest Succeeded.")

        filename = "mytorrent"
        #os.system(f"webtorrent create {filename} -o {filename}.torrent")
        #with open(f"test/{filename}.torrent","rb") as f:
        #    torrentfile = f.read()

        #r = requests.post("http://127.0.0.1:5000/upload_torrent_file",files={"torrentfile":torrentfile})
        #print(r.content)
class CaesarStoreMagnetURI(unittest.TestCase):
    def test_store_magnet_uri(self):
        companyname = "Google"
        contributorname = "palondomus"
        quotaname = "Googleman Text Classification"
        files = [{"name":"main.jpeg"}]
        torrent = {"magnetURI":r"magnet:?xt=urn:btih:5054704b0ab85ce6ddbe2a9e8b75e7a60d72f8e3&dn=main.jpeg&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com" }
        contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignup",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
        contributorsignup = contributorsignupresp.json()
        try:
            self.assertEqual(200,  contributorsignupresp.status_code)
        except AssertionError as aex:
            contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignin",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
            contributorsignup = contributorsignupresp.json()
            self.assertEqual(200,  contributorsignupresp.status_code)


        storemagneturitestresp = requests.post("http://localhost:5000/storemagneturi",json={"companyname":companyname,"quotaname":quotaname,"torrentfilename":files[0]["name"],"torrentmagneturi":torrent["magnetURI"]},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        print(storemagneturitestresp)
        self.assertNotEqual("error", list(storemagneturitestresp.keys())[0])
        print(storemagneturitestresp)

        getmagneturitestresp = requests.post("http://localhost:5000/getmagneturi",json={"companyname":companyname,"quotaname":quotaname,"torrentfilename":files[0]["name"]},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        #print(getmagneturitestresp)
        self.assertNotEqual("error", list(getmagneturitestresp.keys())[0])
        print(getmagneturitestresp)
class StartBlockChain(unittest.TestCase):
    def create_block_chain(self):
        contributorname = "palondomus"
        blockchain_password = "kya63amari"
        contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignup",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
        contributorsignup = contributorsignupresp.json()
        try:
            self.assertEqual(200,  contributorsignupresp.status_code)
        except AssertionError as aex:
            contributorsignupresp = requests.post("http://127.0.0.1:5000/contributorsignin",json={"contributor":contributorname,"email":"amari.lawal05@gmail.com","password":"kya63amari"})
            contributorsignup = contributorsignupresp.json()
            self.assertEqual(200,  contributorsignupresp.status_code)
        # Creates the genesis block and create the needed info
        createblockchainresp = requests.post("http://localhost:5000/create_blockchain",json={"blockchain_name":"Caesar Block Chain","blockchain_privilege":"private","blockchain_password":blockchain_password},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        print(createblockchainresp)
        self.assertNotEqual("error", list(createblockchainresp.keys())[0])
        

        # Adds members to the blockchain so that members are authenticated to add blocks to the blockchain
        joinblockchainresp = requests.post("http://localhost:5000/join_blockchain",json={"blockchain_name":"Caesar Block Chain","blockchain_password":blockchain_password},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        print(joinblockchainresp)
        self.assertNotEqual("error", list(joinblockchainresp.keys())[0])
        # Gets the last block for when actually mining the block on the frontend.
        getlastblockchainresp = requests.post("http://localhost:5000/get_last_block",json={"blockchain_name":"Caesar Block Chain","blockchain_password":blockchain_password},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        print(getlastblockchainresp)
        self.assertNotEqual("error", list(getlastblockchainresp.keys())[0])
        # Actually stores the block in the blockchain
        # This will be run every 30 minutes of contributor seeding, or when a contributor uploads a torrent providing a higher transaction reward. The Nonce can maybe compare to the size of the dataset or just be arbitrary.
        storeblockchainresp = requests.post("http://localhost:5000/store_block",json={"blockchain_name":"Caesar Block Chain","blockchain_password":blockchain_password,"block":{"index": 2,"transactions": [{
                "sender": "System",
                    "recipient": "Amari",
                    "amount": 5
                }
            ],
            "timestamp": 1670968816.5094395,
            "previous_hash": "9bf7805a0526daa375cdbb5a211893d666b8720713e5a474c05550be9bad5849",
            "nonce": 157,
            "hash": "00f41aa9b651f032354d05a40b753bca30b51bf32e67268534d8cecfcf43590e"
        }},headers={'Authorization': 'Bearer ' + contributorsignup["access_token"]}).json()
        print(storeblockchainresp)
        self.assertNotEqual("error", list(storeblockchainresp.keys())[0])

        
# TODO Make sure the mining part on the frontend is working.


# TODO Next the user will keep seeding, calculating the nonce and awarding the coin every 5 minutes, this will be a decentralized blockchain that won't need my api, will only stay on the frontend
# TODO Make route that generates more coin to the person who seeds it first, I differentiated this by creating hash using this 
# TODO Once the user chooses to stop seeding on the frontend
# Decentralized Version
# Do all mining on only the frontend and don't store the overrall blockchain
# Centralized Version - Preffered
# Do mining on frontend but then after maybe an 30/1 hour when I am generating the coin send a request to **add** the block to the overall large lockhain that I store. Then I can issue people there wallets. 
if __name__ == '__main__':
    unittest.main()

