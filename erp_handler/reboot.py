from erp.models import ERP
import docker

def reboot_sync():
    client = docker.from_env()
    
    erps = ERP.objects.filter(is_active=True)
    for erp in erps:
        if erp.is_running:
            container = client.get(erp.container_id)
            print(container.status)
