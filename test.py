import os 

erp_image = 'erp_web_base'
db_image = 'erp_db_base'

network_name = "erp_net_3"
db_name = "db_3"
erp_name = "erp_3"

cmd = 'docker network create --attachable {}'.format(network_name)
os.system(cmd)
cmd = 'docker run --name {0} --label {0} --network {1} --network-alias=db --hostname db -d {2}'.format(db_name, network_name, db_image)
os.system(cmd)

cmd = 'docker run -d --name {0} --label {0} --network {1} --hostname {2} --link {3} {2}'.format(erp_name, network_name, erp_image, db_name)
os.system(cmd)
cmd = 'docker exec {} /bin/bash -c "/usr/src/app/seeder.sh"'.format(erp_name)
os.system(cmd)
