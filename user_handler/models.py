from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class UserBase(AbstractUser):
    is_active = models.BooleanField(default=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta(object):
        unique_together = ('email',)


def image_directory_path(instance, filename):
    return 'image/user_{0}/profile_image.jpg'.format(instance.user.username)

class Profile(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    phone_number2 = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to= image_directory_path, null=True, blank=True)
    post = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.user)