from django.db import models
from user_handler.models import UserBase
import os
import uuid
import requests
from erp_handler.settings import docker_ip, docker_port, docker_protocol
from os import path
import json
from commerce.models import Credit

class PortMan(models.Model):
    server_name = models.CharField(max_length=255, default = "0.0.0.0")
    current_port = models.PositiveIntegerField(default='9000')
    available_ports = models.TextField(default='[]')

    def get_port(self):
        ports = json.loads(self.available_ports)
        if len(ports) > 0:
            x = ports.pop(len(ports)-1)
            self.available_ports = json.dumps(ports)
            self.save()
        else:
            x = self.current_port
            self.current_port = self.current_port + 1
            self.save()
        return x
    
    def port_freed(self, port):
        ports = json.loads(self.available_ports)
        ports.append(port)
        self.available_ports = json.dumps(ports)
        self.save()


def get_container_data(name):
    url = '{}://{}:{}/containers/json?all=1'.format(docker_protocol, docker_ip, docker_port)
    params = 'filters={"name":["'+str(name)+'"]}'
    res = requests.get(url, params=params)
    return res.json()
    
def container_creation(id):
    try:
        erp_image = 'erp_web_base'
        db_image = 'erp_db_base'
        network_name = "erp_net_"+str(id)
        db_name = "db_"+str(id)
        erp_name = "erp_"+str(id)
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
    credit = models.OneToOneField(Credit, on_delete=models.PROTECT, related_name="erp")

    container_id = models.TextField(blank=True, null=True)
    db_container_id = models.TextField(blank=True, null=True)
    network_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True)
    port = models.PositiveIntegerField(default=9000, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.company} {self.user}'

    def create_container(self):
        id = self.id
        x = None
        x = container_creation(id)
        if x:
            raise Exception(str(x))
        network_name = 'erp_net_'+str(id)
        container = get_container_data('erp_'+str(id))[0]
        self.container_id = container['Id'] 
        self.ip = container['NetworkSettings']['Networks'][network_name]['IPAddress']
        self.network_id = container['NetworkSettings']['Networks'][network_name]['NetworkID']
        self.db_container_id = get_container_data('db_'+str(id))[0]['Id']
        self.save()
        try:
            port_man = PortMan.objects.all()[0]
        except:
            raise Exception("Port man is not setup.")
        port = port_man.get_port()
        server_name = port_man.server_name
        self.port = port
        self.link =  nginx_config(self, server_name, port)
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
        url = '{}://{}:{}/containers/{}/start'.format(docker_protocol, docker_ip, docker_port, self.db_container_id)
        requests.post(url)
        url = '{}://{}:{}/containers/{}/start'.format(docker_protocol, docker_ip, docker_port, self.container_id)
        requests.post(url)
        id = self.id
        erp_name = "erp_"+str(id)
        cmd = 'docker exec {} /bin/bash service nginx start'.format(erp_name)
        os.system(cmd)
        network_name = 'erp_net_'+str(id)
        container = get_container_data('erp_'+str(id))[0]
        
        if (self.ip != container['NetworkSettings']['Networks'][network_name]['IPAddress']):
            print('update nginx')
            try:
                port_man = PortMan.objects.all()[0]
            except:
                raise Exception("Port man is not setup.")
            server_name = port_man.server_name
            self.link =  nginx_config(self, server_name, self.port)
            self.save()
            self.save()
        return True

    
    def delete_container(self):
        try:
            url = '{}://{}:{}/containers/{}'.format(docker_protocol, docker_ip, docker_port, self.container_id)
            requests.delete(url)
            url = '{}://{}:{}/containers/{}'.format(docker_protocol, docker_ip, docker_port, self.db_container_id)
            requests.delete(url)
            url = '{}://{}:{}/networks/{}'.format(docker_protocol, docker_ip, docker_port, self.network_id)
            requests.delete(url)
            url = '{}://{}:{}/volumes/prune'.format(docker_protocol, docker_ip, docker_port)
            requests.post(url)
            location = '/etc/nginx/sites-enabled/erp_{}'.format(self.id)
            os.remove(location)
            self.container_id = None
            self.db_container_id = None
            self.network_id = None
            self.link = None
            self.ip = None
            try:
                port_man = PortMan.objects.all()[0]
            except:
                raise Exception("Port man is not setup.")
            port_man.port_freed(self.port)
            return True
        except:
            return False

def nginx_config(erp, server_name, port):
    location = '/etc/nginx/sites-enabled/erp_{}'.format(erp.id)
    if path.exists(location):
        os.remove(location)
    with open(location, 'w') as nginx_config_file:
        nginx_config_file.writelines([
            'upstream erp_backend_{} '.format(erp.id),
            '{',
            '    server {};'.format(erp.ip),
            '}',
            'server {',
            '    listen {};'.format(port),
            '    server_name {};'.format(server_name),
            '    charset utf-8;',
            '    client_max_body_size 128M;',
            '    location / {',
            '        proxy_pass http://erp_backend_{};'.format(erp.id),
            '    }',
            '    location /ws {',
            '        proxy_pass http://erp_backend_{};'.format(erp.id),
            '        proxy_http_version 1.1;',
            '        proxy_set_header Upgrade $http_upgrade;',
            '        proxy_set_header Connection "upgrade";',
            '        proxy_redirect off;',
            '        proxy_set_header Host $host;',
            '        proxy_set_header X-Real-IP $remote_addr;',
            '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;',
            '        proxy_set_header X-Forwarded-Host $server_name;',
            '    }',
            '}'
        ])
    os.system('nginx -s reload')
    return f'{server_name}:{port}'
