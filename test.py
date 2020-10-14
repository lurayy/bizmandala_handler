# import os 

# erp_image = 'erp_web_base'
# db_image = 'erp_db_base'

# network_name = "erp_net_3"
# db_name = "db_3"
erp_name = "erp_3"

# cmd = 'docker network create --attachable {}'.format(network_name)
# x = os.system(cmd)
# print("id = ",x)
# cmd = 'docker run --name {0} --label {0} --network {1} --network-alias=db --hostname db -d {2}'.format(db_name, network_name, db_image)
# x = os.system(cmd)
# print("id = ",x)

# cmd = 'docker run -d --name {0} --label {0} --network {1} --hostname {2} --link {3} {2}'.format(erp_name, network_name, erp_image, db_name)
# x = os.system(cmd)
# print("id = ",x)
# cmd = 'docker exec {} /bin/bash -c "/usr/src/app/seeder.sh"'.format(erp_name)
# x = os.system(cmd)
# print("id = ",x)
import requests


url = "{}://{}:{}/containers/json".format('http','127.0.0.1', '2375', ) 
print(url)
params = 'filters={"name":["db_3"]}'
res = requests.get(url, params=params)
# get containers from returned json
containers = res.json()
print(containers)
# print(containers)
# instantiate empty list of containers
container = containers[0]
# iterate container list to grab only needed fields
# to keep payload small
print(container['Id'][:12])
url = "{}://{}:{}/containers/{}/stop".format('http','127.0.0.1', '2375', container['Id']) 
res = requests.post(url)
print(res.text)

#     # append 
#     containers_list.append(
#         {
#             'id': container['Id'],
#             'name': container['Names'][0],
#             'state': container['State'],
#             'status': container['Status'],
#         }
#     )
# print(containers_list)
