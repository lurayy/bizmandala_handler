# import requests
# from erp_handler.settings import docker_ip, docker_port, docker_protocol
# from django.utils.timezone import now
# import dateutil.parser
# from datetime import datetime, timezone

# print(docker_ip)

# url = '{}://{}:{}/containers/{}/json'.format(docker_protocol, docker_ip, docker_port, '0b03b5a26ffe')
# s = requests.get(url)
# s = s.json()
# print(s['State'])
# print(s['State']['StartedAt'])
# print(s['State']['FinishedAt'])

# now = datetime.now(timezone.utc)

# start = dateutil.parser.parse(s['State']['StartedAt'])

# end = dateutil.parser.parse(s['State']['FinishedAt'])

# if start > end:
#     print('running')


# # print(start - end), data=json.dumps(data)

# print(now - start)

import requests
import json

base_url = "http://localhost:8000/api/v1/"

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

def call(headers, data, url):
    sess = requests.get(base_url+url, headers=headers)
    print(sess.text)

if __name__ == "__main__":
    headers = login()
    
    # ------------------------------------------- Data Here ----------------------------------------
    data = {}
    url = 'user'
    call(headers, data, url)