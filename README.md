# MY PROJECT TITLE IS PASSWORD MANAGER
#### THE VIDEO DEMO'S URL IS :
#### DESCRIPTION OF THE PROGRAM:
   This python is designed for the user to save all the user's passwords in one place locally
   so that in times of need user can retrieve those passwords easily. It provides the user
   functionalities which are generate ,check ,store , retrieve the password. the detail breakdown
   is as follows:

## Modules and Functions used:
  **modules import** <br>
     secrets: Used to generate cryptographically strong random numbers for password creation, ensuring the output cannot be predicted (unlike the standard random module).
     cryptography.fernet: A third-party library used for symmetric encryption. It handles the encryption of passwords before they are saved to the JSON file and decrypts them when retrieved.
     json: Handles the serialization and deserialization of the data, allowing the program to read and write the password vault as a structured JSON object.
     re: The Regular Expression module is used in validate_service_name to ensure input sanitization and in check_password_strength to detect specific character types (uppercase, digits, symbols).
     sys: Used to perform system-level operations, specifically sys.exit(1) to terminate the program securely if authentication fails.

   **Funtions used** <br>
     main(): The entry point of the program. It initializes the authentication check and runs the while loop that powers the interactive command-line menu.
     secrets.choice(): Used to securely select random characters from the character pool.
     secrets.SystemRandom().shuffle(): Used to shuffle the generated password characters to prevent predictable patterns.
     Fernet.encrypt() / Fernet.decrypt(): Methods from the cryptography library used to lock and unlock the password data.
     json.dump() / json.load(): Standard library methods used to serialize the dictionary data into a file and read it back.
     re.search() / re.match(): Regular expression methods used to find specific patterns (like digits or symbols) inside strings.
     sys.exit(): Used to safely terminate the program if authentication fails.

   **Custom Functions** <br>
     verify_master_password(): Handles the login logic. It checks if a .master file exists and validates the user's input against the stored hash.
     generate_password(): The core logic for creating passwords. It constructs a pool of characters based on user preferences and builds a secure string.
     check_password_strength(): Calculates a security score (0-100) based on password length and entropy, returning a rating (e.g., "Very Strong").
     handle_store() & handle_retrieve(): Functions that manage the user interface for saving and fetching credentials, handling the encryption/decryption process.
     load_passwords() & save_passwords(): specific file I/O functions that handle reading from and writing to the passwords.enc JSON file.
     get_encryption_key(): A utility that loads the existing encryption key or generates a new one if it doesn't exist.
## Core Functionality
    Master Authentication: Access to the application is secured via a master password. The password is never stored in plain text instead it is stored in and encrpyted format in the .master file.
    Password Generation: The system generates cryptographically strong passwords and  Users can customize the length and
    whether of uppercase letters, numbers, and symbols.
    Strength Analysis: The application evaluates password strength and character variety, assigning a score between 0 to 100 and a rating from Weak to Very Strong .
    Encrypted Storage: The program takes your login details, locks them using encryption so they cannot be read by others, and saves them into a file called passwords.enc.
    Data Retrieval: Users can list stored service names and retrieve specific passwords. The application decrypts the requested password on-the-fly for display.
