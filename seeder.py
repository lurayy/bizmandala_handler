from user_handler.models import UserBase, Profile


from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.create_superuser('admin', 'admin@myproject.com', 'pass')
admin.first_name = 'Hero'
admin.last_name = 'Admin'
admin.save()
Profile.objects.create(user=admin, address='pokhara', phone_number='234',phone_number2='234234',post='hero')