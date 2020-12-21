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

# import requests
# import json

# base_url = "http://localhost:8000/api/v1/"
# # base_url = "https://bizmandala.mandalaitsolutions.com/"
# def login():    
#     creds = {
#         "username":"admin",
#         "password":"pass"
#     }
#     log_in_url = base_url+"user/"
#     r = requests.post(log_in_url, data= json.dumps(creds))
#     print(r.text)
#     token = r.json()["token"]
#     print(token)

#     headers = {
#         "authorization":token,
#     }
#     sess = requests.get(base_url+"user", headers=headers)
#     print(sess.text)
#     return headers

# def post(data, headers, url):
#     sess = requests.post(base_url+url, headers=headers, data= json.dumps(data))
#     print(headers, url)
#     # print(sess.json())
#     # return (sess.text)
#     print(sess.text)


# def get(headers, url):
#     sess = requests.get(base_url+url, headers=headers)
#     return (sess.json())

# if __name__ == "__main__":
#     headers = login()
#     # ------------------------------------------- Data Here ----------------------------------------
#     data = {
#         'hours': 720,
#         'number_of_erps' : 2,
#         'pure_total_amount' : 1440000,
#         'paid_amount' :  1440000,
#         'bill_amount' : 1440000,
#         'discount_amount' : 0,
#         'discount_note' : 0,
#         'payment_verification' : {},
#         'extend_credit' : None
#     }
#     post(data, headers, 'purchase/')





import os
import docker

client = docker.from_env()

id = 3
erp_image = 'lurayy/erp_web_base'
db_image = 'lurayy/erp_db_base'
network_name = "erp_net_"+str(id)
db_name = "db_"+str(id)
erp_name = "erp_"+str(id)

client.networks.create(network_name, driver='bridge')
client.containers.run(db_image, name=db_name, labels=[db_name], hostname=db_name, detach=True, network=network_name)
container = client.containers.run(erp_image, detach=True, name=erp_name, labels=[erp_name], network=network_name, hostname=erp_name)
print(container)

x = container.exec_run(cmd='/bin/bash -c "/usr/src/app/seeder.sh"')
print(x)
container.logs()
# cmd = 'docker network create --attachable {}'.format(network_name)
# os.system(cmd)
# cmd = 'docker run --name {0} --label {0} --network {1} --network-alias=db --hostname db -d {2}'.format(
#     db_name, network_name, db_image)
# os.system(cmd)
# cmd = 'docker run -d --name {0} --label {0} --network {1} --hostname {2} --link {3} {2}'.format(
#     erp_name, network_name, erp_image, db_name)
# os.system(cmd)
# print(cmd)
# cmd = 'docker exec {} /bin/bash -c "/usr/src/app/seeder.sh"'.format(
#     erp_name)
# os.system(cmd)
