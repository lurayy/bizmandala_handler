import requests
import json
# base_url = "https://bizmandala.mandalaitsolutions.com/api/v1/"
base_url = 'http://localhost:8000/api/v1/'

class TestClass():

    def __init__(self):
        self.session = requests.Session()
        self.session.get(base_url+'user')
        creds = {
            'username' : 'admin',
            'password' : 'pass'
        }
        print(self.session.cookies['x-csrftoken'])
        x = self.session.post(base_url+'user/',headers={'x-csrftoken':self.session.cookies['x-csrftoken']} ,data=json.dumps(creds))
        print('login : ',x.text)
        print('user details : ', self.session.get(base_url+'user/').text)
    
    def post(self, url, data):
        result = self.session.post(base_url+url, data=json.dumps(data))
        print(result.text)
        return result

    def get(self, url):
        result = self.session.get(base_url+url)
        print(result.text)
        return result

if __name__ == "__main__":
    test = TestClass()
    # test.get('user/')