from apps.users.models import CustomUser

CustomUser.objects.create_superuser(
    username="admin",
    password="admin123",
    is_staff=True,
    is_superuser=True
)
