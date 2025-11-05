"""
Generate a secure SECRET_KEY for Django production deployment.
Run this script and copy the generated key to your .env file.
"""
from django.core.management.utils import get_random_secret_key

print("\n" + "="*60)
print("DJANGO SECRET KEY GENERATOR")
print("="*60)
print("\nYour new SECRET_KEY:")
print("-"*60)
print(get_random_secret_key())
print("-"*60)
print("\nIMPORTANT:")
print("1. Copy the key above")
print("2. Paste it in your .env file: SECRET_KEY=your-key-here")
print("3. Keep this key SECRET - never commit it to git!")
print("4. Use a different key for production vs development")
print("="*60 + "\n")

