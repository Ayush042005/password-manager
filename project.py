import secrets
import string
import re
import json
import sys
from cryptography.fernet import Fernet
import hashlib

def main():
    """Main function - Password Manager Menu"""
    print("Password Manager")
    print("=" * 50)

    # Initialize or load master password
    if not verify_master_password():
        print("Authentication failed!")
        sys.exit(1)

    while True:
        print("\n Menu:")
        print("1. Generate Password")
        print("2. Check Password Strength")
        print("3. Store Password")
        print("4. Retrieve Password")
        print("5. List All Services")
        print("6. Exit")

        choice = input("\nSelect option (1-6): ").strip()

        if choice == "1":
            handle_generate()
        elif choice == "2":
            handle_check_strength()
        elif choice == "3":
            handle_store()
        elif choice == "4":
            handle_retrieve()
        elif choice == "5":
            handle_list_services()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option!!")

def generate_password(length=16, use_symbols=True, use_numbers=True, use_uppercase=True):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    chars = string.ascii_lowercase

    if use_uppercase:
        chars += string.ascii_uppercase
    if use_numbers:
        chars += string.digits
    if use_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = []
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_numbers:
        password.append(secrets.choice(string.digits))
    if use_symbols:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))

    # Add lowercase
    password.append(secrets.choice(string.ascii_lowercase))

    # fill remaining length
    remaining = length - len(password)
    password.extend(secrets.choice(chars) for _ in range(remaining))

    # shuffle to randomize positions
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
def check_password_strength(password):
    if not password:
        return {"score": 0, "rating": "Invalid"}

    score = 0
    # length scoring (up to 40 points)
    length = len(password)
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 20
    else:
        score += length * 2
    # character variety (15 points each)
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'\d', password):
        score += 15
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 15
    # Determine rating
    if score >= 80:
        rating = "Very Strong"
    elif score >= 60:
        rating = "Strong"
    elif score >= 40:
        rating = "Medium"
    else:
        rating = "Weak"

    return {"score": score, "rating": rating}


def validate_service_name(service):
    if not service or not service.strip():
        return False

    if len(service) > 50:
        return False

    # allow alphanumeric, spaces, hyphens, underscores
    if not re.match(r'^[a-zA-Z0-9\s_-]+$', service):
        return False
    return True

def verify_master_password():
    try:
        with open('.master', 'r') as f:
            stored_hash = f.read()
        print("\n Authentication Required")
        master = input("Enter master password:")
        if hash_password(master) != stored_hash:
            return False
        print("Access granted!\n")
        return True

    except FileNotFoundError:
        print("\n First time setup!")
        master = input("Create master password: ")
        confirm = input("Confirm master password: ")

        if master != confirm:
            print("Passwords don't match!")
            return False

        with open('.master', 'w') as f:
            f.write(hash_password(master))

        print("Master password created!\n")
        return True

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_encryption_key():
    try:
        with open('.key', 'rb') as f:
            return f.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('.key', 'wb') as f:
            f.write(key)
        return key

def handle_generate():
    try:
        print("\n Password Generator")
        print("-" * 40)
        length_input = input("Password length (default 16): ").strip()
        length = int(length_input) if length_input else 16

        use_symbols = input("Include symbols? (Y/n): ").strip().lower() != 'n'
        use_numbers = input("Include numbers? (Y/n): ").strip().lower() != 'n'
        use_uppercase = input("Include uppercase? (Y/n): ").strip().lower() != 'n'

        password = generate_password(length, use_symbols, use_numbers, use_uppercase)
        strength = check_password_strength(password)

        print(f"\n Generated Password: {password}")
        print(f" Strength: {strength['rating']} ({strength['score']}/100)")

    except ValueError as e:
        print(f" Error: {e}")


def handle_check_strength():
    print("\n Password Strength Checker")
    print("-" * 40)
    password = input("Enter password to check: ")
    strength = check_password_strength(password)
    print(f"\n Strength: {strength['rating']} ({strength['score']}/100)")


def handle_store():
    print("\n Store New Password")
    print("-" * 40)
    service = input("Service name (e.g., Gmail, Netflix): ").strip()

    if not validate_service_name(service):
        print(" Invalid service name!")
        return

    username = input("Username/Email: ").strip()
    password = input("Password: ")

    # encryption and storing
    key = get_encryption_key()
    fernet = Fernet(key)

    data = load_passwords()
    data[service.lower()] = {
        "username": username,
        "password": fernet.encrypt(password.encode()).decode()
    }
    save_passwords(data)

    print(f"Password stored for {service}")

def handle_retrieve():
    """Handle password retrieval"""
    print("\n Retrieve Password")
    print("-" * 40)
    service = input("Service name: ").strip().lower()

    data = load_passwords()

    if service not in data:
        print(f" No password found for '{service}'")
        return
    key = get_encryption_key()
    fernet = Fernet(key)

    entry = data[service]
    decrypted_password = fernet.decrypt(entry["password"].encode()).decode()

    print(f" Service: {service.title()}")
    print(f" Username: {entry['username']}")
    print(f" Password: {decrypted_password}")


def handle_list_services():
    data = load_passwords()

    if not data:
        print("\n No passwords stored yet!")
        return
    print(f"\n Stored Services ({len(data)} total):")
    print("-" * 40)
    for i, service in enumerate(sorted(data.keys()), 1):
        print(f"  {i}. {service.title()}")

def load_passwords():
    try:
        with open('passwords.enc', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_passwords(data):
    with open('passwords.enc', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
