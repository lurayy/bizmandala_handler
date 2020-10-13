from django.db import models
from user_handler.models import UserBase

class ERP(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    address = models.TextField(max_length=255)

    is_running = models.BooleanField(default=False)
    has_container = models.BooleanField(default=False)
    container_id = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True) 
    ip = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.company} {self.user}'


