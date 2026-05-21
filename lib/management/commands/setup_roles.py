from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up role-based permissions'
    
    def handle(self, *args, **kwargs):
        """
        Assign permissions based on roles:
        
        Admin:     All permissions
        Librarian: Can add/change/delete/view books, can ban books
        Member:    Can view books only
        """
        
        # Get permissions
        add_book = Permission.objects.get(codename='add_book')
        change_book = Permission.objects.get(codename='change_book')
        delete_book = Permission.objects.get(codename='delete_book')
        view_book = Permission.objects.get(codename='view_book')
        can_ban_book = Permission.objects.get(codename='can_ban_book')
        
        # TODO: Assign to librarians
        librarians = User.objects.filter(role='librarian')
        for user in librarians:
            # Clear existing permissions
            user.user_permissions.clear()
            
            # Add librarian permissions
            user.user_permissions.add(
                add_book,
                change_book,
                delete_book,
                view_book,
                can_ban_book
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'Set up permissions for librarian: {user.username}')
            )
        
        # TODO: Assign to members
        members = User.objects.filter(role='member')
        for user in members:
            user.user_permissions.clear()
            user.user_permissions.add(view_book)
            
            self.stdout.write(
                self.style.SUCCESS(f'Set up permissions for member: {user.username}')
            )
        
        # TODO: Admins get all permissions (superuser)
        admins = User.objects.filter(role='admin')
        for user in admins:
            user.is_superuser = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Made admin superuser: {user.username}')
            )