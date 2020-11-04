from user_handler.models import UserBase, Profile
from commerce.models import Setting
from erp.models import PortMan

from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.create_superuser('admin', 'admin@myproject.com', 'pass')
admin.first_name = 'Hero'
admin.last_name = 'Admin'
admin.save()
Profile.objects.create(user=admin, address='pokhara', phone_number='234',phone_number2='234234',post='hero')
Setting.objects.create(
    unitary_price = 1000
)

PortMan.objects.create(
    server_name = '0.0.0.0',
    current_port = 9000
)