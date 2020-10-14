from django.db import models
from user_handler.models import UserBase
import os
import uuid
import requests
from erp_handler.settings import docker_ip, docker_port, docker_protocol

def get_container_data(container_name):
    url = '{}://{}:{}/containers/json'.format(docker_protocol, docker_ip, docker_port)
    params = 'filters={"name":["{}"]}'.format(container_name)
    res = requests.get(url, params=params)
    return res.json()

def container_creation(uuid):
    try:
        erp_image = 'erp_web_base'
        db_image = 'erp_db_base'
        network_name = "erp_net_"+str(uuid)
        db_name = "db_"+str(uuid)
        erp_name = "erp_"+str(uuid)
        cmd = 'docker network create --attachable {}'.format(network_name)
        os.system(cmd)
        cmd = 'docker run --name {0} --label {0} --network {1} --network-alias=db --hostname db -d {2}'.format(
            db_name, network_name, db_image)
        os.system(cmd)
        cmd = 'docker run -d --name {0} --label {0} --network {1} --hostname {2} --link {3} {2}'.format(
            erp_name, network_name, erp_image, db_name)
        os.system(cmd)
        cmd = 'docker exec {} /bin/bash -c "/usr/src/app/seeder.sh"'.format(
            erp_name)
        os.system(cmd)
        return False
    except Exception as exp:
        return exp

class ERP(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    address = models.TextField(max_length=255)

    is_running = models.BooleanField(default=False)
    has_container = models.BooleanField(default=False)

    container_id = models.TextField(blank=True, null=True)
    db_container_id = models.TextField(blank=True, null=True)
    network_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.company} {self.user}'

    def create_container(self):
        if self.has_container:
            raise Exception("Container already exsists.")
        x = container_creation(self.uuid)
        if x:
            raise Exception(str(x))
        name = 'erp_'+str(self.uuid)
        network_name = 'erp_net_'+str(self.uuid)
        container = get_container_data(name)[0]
        self.container_id = container['Id'] 
        self.ip = container['NetworkSettings']['Networks'][network_name]['IPAddress']
        self.link =  container['NetworkSettings']['Networks'][network_name]['IPAddress']
        self.network_id = container['NetworkSettings']['Networks'][network_name]['NetworkID']
        self.db_container_id = get_container_data('db_'+str(uuid))[0]['Id']
        
        self.is_running = True
        self.has_container = True
        self.save()
    
    def stop_container(self):
        try:
            url = '{}://{}:{}/containers/{}/stop'.format(docker_protocol, docker_ip, docker_port, self.container_id)
            requests.post(url)
            url = '{}://{}:{}/containers/{}/stop'.format(docker_protocol, docker_ip, docker_port, self.db_container_id)
            requests.post(url)
            return True
        except:
            return False
    
    def start_container(self):
        try:
            url = '{}://{}:{}/containers/{}/start'.format(docker_protocol, docker_ip, docker_port, self.container_id)
            requests.post(url)
            url = '{}://{}:{}/containers/{}/start'.format(docker_protocol, docker_ip, docker_port, self.db_container_id)
            requests.post(url)
            return True
        except:
            return False
    
    def delete_container(self):
        try:
            url = '{}://{}:{}/containers/{}'.format(docker_protocol, docker_ip, docker_port, self.container_id)
            requests.delete(url)
            url = '{}://{}:{}/containers/{}'.format(docker_protocol, docker_ip, docker_port, self.db_container_id)
            requests.delete(url)
            url = '{}://{}:{}/networks/{}'.format(docker_protocol, docker_ip, docker_port, self.network_id)
            requests.delete(url)
            self.is_running = False
            self.has_container = False
            self.container_id = None
            self.db_container_id = None
            self.network_id = None
            self.link = None
            self.ip = None
            return True
        except:
            return False
     
    

