from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, created = Group.objects.get_or_create(
            name="profile_manager",            
        )
        premission_profile = Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )
        
        # добавление разрешения группе
        group.permissions.add(premission_profile)
        
        # добавление группы в группы пользователя 
        user.groups.add(group)
        
        # добавление разрешения пользователю
        user.user_permissions.add(permission_logentry)
        
        group.save()
        user.save()