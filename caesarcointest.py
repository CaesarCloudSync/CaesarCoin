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
            self.assertEqual(200,  quotapostersignupresp.status_code)
            

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
        with open(f"test/{filename}.torrent","rb") as f:
            torrentfile = f.read()

        r = requests.post("http://127.0.0.1:5000/upload_torrent_file",files={"torrentfile":torrentfile})
        print(r.content)

if __name__ == '__main__':
    unittest.main()

