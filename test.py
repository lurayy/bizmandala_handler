# import requests
# from erp_handler.settings import docker_ip, docker_port, docker_protocol
# from django.utils.timezone import now
# import dateutil.parser
# from datetime import datetime, timezone

# # print(docker_ip)

# url = '{}://{}:{}/containers/json'.format(docker_protocol, docker_ip, docker_port)
# s = requests.get(url)
# s = s.json()
# # print(s['State'])
# # print(s['State']['StartedAt'])
# # print(s['State']['FinishedAt'])

# # now = datetime.now(timezone.utc)

# # start = dateutil.parser.parse(s['State']['StartedAt'])

# # end = dateutil.parser.parse(s['State']['FinishedAt'])

# # if start > end:
# #     print('running')


# # # print(start - end), data=json.dumps(data)

# # print(now - start)

import requests
import json

# base_url = "http://localhost:8000/api/v1/"
base_url = "https://bizmandala.mandalaitsolutions.com/"
def login():    
    creds = {
        "username":"admin",
        "password":"pass"
    }
    log_in_url = base_url+"user/"

    r = requests.post(log_in_url, data= json.dumps(creds))
    print(r.json())
    token = r.json()["token"]
    print(token)

    headers = {
        "authorization":token,
    }
    sess = requests.get(base_url+"user", headers=headers)
    print(sess.text)
    return headers

def post(data, url):
    sess = requests.post(base_url+url,  data= json.dumps(data))
    # print(sess.json())
    # return (sess.text)
    print(sess.text)


def get(headers, url):
    sess = requests.get(base_url+url, headers=headers)
    return (sess.json())

if __name__ == "__main__":
    # headers = login()
    
    # ------------------------------------------- Data Here ----------------------------------------
    data = {
    "first_name": "Bhsdfasdfuwan",
    "last_name": "Adhikasdfri",
    "username": "bhuwanadhasddfsdf",
    "email": "asdfsadf@gmail.com",
    "password": "asdf",
    "profile": {
        "address": "Pokhara 16 Lamachaur WRC Hostel",
        "phone_number": "9860541599",
        "phone_number2": "+9779860541599",
        "post": "33700",
        "profile_image": None
        }
    }
    post( data, 'api/v1/user/register' )





# import os

# id = 3
# erp_image = 'erp_web_base'
# db_image = 'erp_db_base'
# network_name = "erp_net_"+str(id)
# db_name = "db_"+str(id)
# erp_name = "erp_"+str(id)
# cmd = 'docker network create --attachable {}'.format(network_name)
# os.system(cmd)
# cmd = 'docker run --name {0} --label {0} --network {1} --network-alias=db --hostname db -d {2}'.format(
#     db_name, network_name, db_image)
# os.system(cmd)
# cmd = 'docker run -d --name {0} --label {0} --network {1} --hostname {2} --link {3} {2}'.format(
#     erp_name, network_name, erp_image, db_name)
# os.system(cmd)
# cmd = 'docker exec {} /bin/bash -c "/usr/src/app/seeder.sh"'.format(
#     erp_name)
# os.system(cmd)
