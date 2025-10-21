#!/usr/bin/env python3
"""
Verify test user password hash
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password
password = "TestPass123!"

# Hash from database
stored_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIWXQXqJUe"

# Verify
is_valid = pwd_context.verify(password, stored_hash)

print(f"Password: {password}")
print(f"Hash: {stored_hash}")
print(f"Valid: {is_valid}")

if is_valid:
    print("\n✅ Password verification successful!")
    print("\nYou can login with:")
    print("  Email: test@smartai.com")
    print("  Password: TestPass123!")
else:
    print("\n❌ Password verification failed!")
    print("Creating new hash...")
    new_hash = pwd_context.hash(password)
    print(f"New hash: {new_hash}")
