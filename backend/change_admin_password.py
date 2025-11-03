"""
Simple script to change admin password.
Run this from the backend directory: python change_admin_password.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitchen_inventory.settings')
django.setup()

from django.contrib.auth.models import User

def change_admin_password():
    try:
        # Find admin user
        admin = User.objects.filter(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found!")
            print("Available users:")
            for user in User.objects.all():
                print(f"  - {user.username}")
            return
        
        # Change password
        admin.set_password('p@ssw0rd')
        admin.save()
        
        print("✅ Admin password changed successfully!")
        print(f"Username: admin")
        print(f"Password: p@ssw0rd")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    change_admin_password()

