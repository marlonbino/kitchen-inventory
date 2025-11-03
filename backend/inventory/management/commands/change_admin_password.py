from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Change the admin user password'

    def handle(self, *args, **kwargs):
        try:
            # Find the admin user
            admin_user = User.objects.filter(username='admin').first()
            
            if not admin_user:
                self.stdout.write(self.style.ERROR('Admin user not found!'))
                return
            
            # Set the new password
            admin_user.set_password('p@ssw0rd')
            admin_user.save()
            
            self.stdout.write(self.style.SUCCESS('✓ Admin password changed successfully!'))
            self.stdout.write(self.style.SUCCESS(f'Username: admin'))
            self.stdout.write(self.style.SUCCESS(f'Password: p@ssw0rd'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error changing password: {str(e)}'))

