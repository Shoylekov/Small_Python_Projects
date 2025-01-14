import os
import tkinter as tk
from tkinter import messagebox
import bcrypt
import cryptography
from cryptography.fernet import Fernet
import sqlite3

def initialize_database():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY,
                        username TEXT,
                        password BLOB,
                        description TEXT)''')
    conn.commit()
    conn.close()

initialize_database()

def set_master_password():
    set_window = tk.Toplevel(window)
    set_window.title("Set Master Password")
    set_window.geometry("400x300")
    
    tk.Label(set_window, text="Set your Master Password:", font=("Arial", 12)).pack(pady=20)
    master_password_entry = tk.Entry(set_window, show="*", font=("Arial", 12))
    master_password_entry.pack(pady=10, padx=20, fill="x")
    
    def save_master_password():
        password = master_password_entry.get()
        hashed_password = hash_master_password(password)
        # Store hashed password in a file or database securely (in this case, we're just using a file for simplicity)
        with open("master_password.hash", "wb") as file:
            file.write(hashed_password)
        set_window.destroy()
        messagebox.showinfo("Success", "Master password set successfully!")
    
    tk.Button(set_window, text="Save Master Password", command=save_master_password, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)


#  generate an encryption key
def generate_key():
    return Fernet.generate_key()

# load or generate the encryption key
def load_or_generate_key():
    key_file = "encryption_key.key"
    
    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            return f.read()
    else:
        key = generate_key()
        with open(key_file, "wb") as f:
            f.write(key)
        return key

# Load encryption key
encryption_key = load_or_generate_key()
cipher_suite = Fernet(encryption_key)

# Hash the master password for secure storage
def hash_master_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password():
    password = master_password_entry.get()
    try:
        with open("master_password.hash", "rb") as file:
            stored_hash = file.read()
        if bcrypt.checkpw(password.encode(), stored_hash):
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()
            show_main_window()
        else:
            messagebox.showerror("Error", "Incorrect password!")
    except FileNotFoundError:
        messagebox.showerror("Error", "No master password found. Please set one first.")
        set_master_password()

def show_main_window():
    main_window = tk.Toplevel(window)
    main_window.title("Password Manager - Main")
    main_window.geometry("400x300")

    main_window.config(bg="#f0f0f0")
    
    tk.Label(main_window, text="Welcome to your Password Manager!", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
    
    tk.Button(main_window, text="Add Password", command=add_password, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
    
    tk.Button(main_window, text="View Stored Passwords", command=view_passwords, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10)

def add_password():
    add_window = tk.Toplevel(window)
    add_window.title("Add Password")
    add_window.geometry("400x400")
    
    add_window.config(bg="#f0f0f0")
    
    tk.Label(add_window, text="Email/Username:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    username_entry = tk.Entry(add_window, font=("Arial", 12))
    username_entry.pack(pady=5, padx=20, fill="x")
    
    tk.Label(add_window, text="Password:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(add_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5, padx=20, fill="x")
    
    tk.Label(add_window, text="Description:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
    description_entry = tk.Entry(add_window, font=("Arial", 12))
    description_entry.pack(pady=5, padx=20, fill="x")
    
    def save_password():
        username = username_entry.get()
        password = password_entry.get()
        description = description_entry.get()
        
        save_password_to_db(username, password, description)
        add_window.destroy()
        messagebox.showinfo("Success", "Password saved successfully!")
    
    tk.Button(add_window, text="Save Password", command=save_password, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

def save_password_to_db(username, password, description):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    encrypted_password = cipher_suite.encrypt(password.encode())
    cursor.execute("INSERT INTO passwords (username, password, description) VALUES (?, ?, ?)", 
                   (username, encrypted_password, description))
    conn.commit()
    conn.close()

def view_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, description FROM passwords")
    rows = cursor.fetchall()
    
    view_window = tk.Toplevel(window)
    view_window.title("View Passwords")
    view_window.geometry("400x400")
    
    view_window.config(bg="#f0f0f0")
    
    tk.Label(view_window, text="Stored Passwords", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
    
    canvas = tk.Canvas(view_window)
    canvas.pack(side="left", fill="both", expand=True)
    
    scrollbar = tk.Scrollbar(view_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    password_frame = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=password_frame, anchor="nw")

    # Add password entries, labels, and buttons to the scrollable frame
    for row in rows:
        password_id = row[0]
        username = row[1]
        encrypted_password = row[2]  # This should be stored as BLOB
        description = row[3]
        
        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            
            password_label = tk.Label(password_frame, text=f"Username: {username}\nPassword: {decrypted_password}\nDescription: {description}", 
                                      font=("Arial", 12), bg="#f0f0f0", anchor="w")
            password_label.pack(pady=10, padx=20, fill="x")
            
            tk.Button(password_frame, text="Edit", command=lambda id=password_id: edit_password(id), font=("Arial", 10), bg="#FFC107", fg="black").pack(pady=5)
            tk.Button(password_frame, text="Delete", command=lambda id=password_id: delete_password(id), font=("Arial", 10), bg="#F44336", fg="white").pack(pady=5)
        
        except cryptography.fernet.InvalidToken:
            # Handle decryption failure
            error_label = tk.Label(password_frame, text=f"Username: {username}\nPassword: [ERROR] Decryption failed\nDescription: {description}", 
                                   font=("Arial", 12), bg="#f0f0f0", anchor="w")
            error_label.pack(pady=10, padx=20, fill="x")
    
    # Update the scrollable region of the canvas
    password_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    conn.close()


def delete_password(password_id):
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this password?")
    if confirm:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM passwords WHERE id=?", (password_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password deleted successfully!")

def edit_password(password_id):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, description FROM passwords WHERE id=?", (password_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Password")
        edit_window.geometry("400x400")
        
        # Styling
        edit_window.config(bg="#f0f0f0")
        
        username_entry = tk.Entry(edit_window, font=("Arial", 12))
        username_entry.insert(0, row[0])  # Set current username
        username_entry.pack(pady=10, padx=20, fill="x")
        
        password_entry = tk.Entry(edit_window, show="*", font=("Arial", 12))
        password_entry.insert(0, cipher_suite.decrypt(row[1]).decode())  # Set current password
        password_entry.pack(pady=10, padx=20, fill="x")
        
        description_entry = tk.Entry(edit_window, font=("Arial", 12))
        description_entry.insert(0, row[2])  # Set current description
        description_entry.pack(pady=10, padx=20, fill="x")
        
        def save_edit():
            new_username = username_entry.get()
            new_password = password_entry.get()
            new_description = description_entry.get()
            
            update_password_in_db(password_id, new_username, new_password, new_description)
            edit_window.destroy()
            messagebox.showinfo("Success", "Password updated successfully!")
        
        tk.Button(edit_window, text="Save Changes", command=save_edit, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

def update_password_in_db(password_id, new_username, new_password, new_description):
    encrypted_password = cipher_suite.encrypt(new_password.encode())
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE passwords SET username=?, password=?, description=? WHERE id=?", 
                   (new_username, encrypted_password, new_description, password_id))
    conn.commit()
    conn.close()

# When initializing the program:
encryption_key = load_or_generate_key()
cipher_suite = Fernet(encryption_key)


window = tk.Tk()
window.title("Password Manager")
window.geometry("400x300")

def show_login_window():
    global login_window, master_password_entry
    login_window = tk.Toplevel(window)
    login_window.title("Login")
    login_window.geometry("400x300")
    
    # Styling
    login_window.config(bg="#f0f0f0")
    
    tk.Label(login_window, text="Master Password:", font=("Arial", 12), bg="#f0f0f0").pack(pady=20)
    
    master_password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    master_password_entry.pack(pady=10, padx=20, fill="x")
    
    tk.Button(login_window, text="Login", command=verify_password, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)


show_login_window()


window.mainloop()
