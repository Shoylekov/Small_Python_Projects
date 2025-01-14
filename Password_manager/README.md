Password Manager

Overview

This is a Password Manager application built with Python and Tkinter. It securely stores user credentials using AES encryption (Fernet) and bcrypt hashing for master password security. The application supports adding, viewing, editing, and deleting stored passwords.

Features

- Master Password Protection

Secure access using a master password.

- AES Encryption

Encrypts stored passwords using the cryptography library.

- Secure Storage

Stores credentials in a local SQLite database.

- User Interface

Built using Tkinter for an easy-to-use graphical interface.

- Password Management

Add new credentials.

View stored credentials.

Edit or delete saved credentials.

- Automatic Encryption Key Handling

Generates and stores an encryption key securely.

Installation

Prerequisites

Ensure you have Python installed (version 3.6 or newer recommended).

Install required dependencies:

pip install bcrypt cryptography

Usage

1. Run the script

python password_manager.py

2. Set a master password (first-time users)

3. Log in using the master password

4. Manage your passwords

Add new credentials.

View saved credentials.

Edit or delete existing passwords.

Security Considerations

- Master Password Hashing

Uses bcrypt to securely hash and store the master password.

- AES Encryption

Uses cryptography.fernet for encrypting stored passwords.

- Local Storage

All data is stored in passwords.db (SQLite database).

- Encryption Key

Stored in encryption_key.key for secure password decryption.

File Structure

password_manager/
│── password_manager.py   # Main application file
│── passwords.db          # SQLite database (auto-generated)
│── encryption_key.key    # Encryption key file (auto-generated)
│── master_password.hash  # Hashed master password file (auto-generated)

Future Enhancements

- Implement a password generator

- Add cloud storage options for syncing passwords

- Enhance UI/UX with modern frameworks like PyQt or Tkinter improvements

License

This project is open-source and free to use.

Author

[Your Name]

