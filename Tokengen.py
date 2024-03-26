import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import requests

# AES Encryption
def aes_encrypt(key, data):
    key = key.encode()
    iv = b'\x00' * 16  # Initialization Vector
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data

def aes_decrypt(key, encrypted_data):
    key = key.encode()
    iv = b'\x00' * 16  # Initialization Vector
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(decrypted_data) + unpadder.finalize()
    return data.decode()

# Fernet Encryption
def generate_key():
    return Fernet.generate_key()

def get_fernet_cipher_suite(key):
    return Fernet(key)

def encrypt_data(data, cipher_suite):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data, cipher_suite):
    return cipher_suite.decrypt(encrypted_data).decode()

def generate_token():
    date_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    date = date_entry.get()
    description = description_entry.get()
    type = type_entry.get()
    amount = amount_entry.get()
    company = company_entry.get()
    user_id = random.randint(1000, 9999)
    transaction_id = random.randint(10**(int(id_digits_entry.get())-1), 10**int(id_digits_entry.get()) - 1)
    
    token = f"Date-Time: {date_time}, Date: {date}, Description: {description}, Type: {type}, Amount: {amount}, Company: {company}, User ID: {user_id}, Transaction ID: {transaction_id:0{id_digits_entry.get()}d}"
    return token

def display_token(token):
    token_text.config(state=tk.NORMAL)
    token_text.delete("1.0", tk.END)
    token_text.insert(tk.END, token)
    token_text.config(state=tk.DISABLED)

def generate_single_token():
    token = generate_token()
    if current_encryption == "Fernet":
        encrypted_token = encrypt_data(token, fernet_cipher_suite)
    elif current_encryption == "AES":
        encrypted_token = aes_encrypt(encryption_key_entry.get(), token)
    display_token(f"Unencrypted Token:\n{token}\n\nEncrypted Token:\n{encrypted_token}")
    send_webhook(encrypted_token)

def generate_block_tokens():
    num_tokens = int(num_tokens_entry.get())
    if num_tokens < 5:
        messagebox.showerror("Error", "Number of tokens should be 5 or more for a block.")
        return
    tokens = []
    for _ in range(num_tokens):
        token = generate_token()
        tokens.append(token)
    block_data = "\n".join(tokens)
    if current_encryption == "Fernet":
        encrypted_block = encrypt_data(block_data, fernet_cipher_suite)
    elif current_encryption == "AES":
        encrypted_block = aes_encrypt(encryption_key_entry.get(), block_data)
    display_token(f"Unencrypted Block:\n{block_data}\n\nEncrypted Block:\n{encrypted_block}")
    send_webhook(encrypted_block)

def copy_token():
    token_text_value = token_text.get("1.0", "end-1c").split("Encrypted Token:")[0].strip()  # Extract unencrypted token
    root.clipboard_clear()
    root.clipboard_append(token_text_value)

def copy_encrypted_token():
    token_text_value = token_text.get("1.0", "end-1c")  # Get the entire token text
    root.clipboard_clear()
    root.clipboard_append(token_text_value)

def send_webhook(data):
    webhook_url = "https://your-webhook-endpoint.com"
    response = requests.post(webhook_url, data={"encrypted_data": data})
    if response.status_code == 200:
        messagebox.showinfo("Webhook Sent", "Data sent via webhook successfully.")
    else:
        messagebox.showerror("Webhook Error", f"Failed to send data via webhook. Status code: {response.status_code}")

def send_selected_data():
    if selected_option.get() == "Single Token":
        generate_single_token()
    elif selected_option.get() == "Block Tokens":
        generate_block_tokens()

def update_encryption():
    global current_cipher_suite, current_encryption
    selected_encryption = encryption_combobox.get()
    if selected_encryption == "Fernet":
        current_cipher_suite = fernet_cipher_suite
    elif selected_encryption == "AES":
        current_encryption = "AES"
    else:
        messagebox.showerror("Error", "Invalid encryption selected.")

# GUI
root = tk.Tk()
root.title("Token Generator")

tk.Label(root, text="Date:").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Description:").pack()
description_entry = tk.Entry(root)
description_entry.pack()

tk.Label(root, text="Type:").pack()
type_entry = tk.Entry(root)
type_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Company:").pack()
company_entry = tk.Entry(root)
company_entry.pack()

tk.Label(root, text="Number of Digits in Transaction ID:").pack()
id_digits_entry = tk.Entry(root)
id_digits_entry.pack()

tk.Label(root, text="Number of Tokens (for block):").pack()
num_tokens_entry = tk.Entry(root)
num_tokens_entry.pack()

tk.Label(root, text="Encryption:").pack()
encryption_combobox = ttk.Combobox(root, values=["Fernet", "AES"], state="readonly")
encryption_combobox.pack()
encryption_combobox.current(0)
encryption_combobox.bind("<<ComboboxSelected>>", lambda event: update_encryption())

tk.Label(root, text="Encryption Key (AES only):").pack()
encryption_key_entry = tk.Entry(root, show="*")
encryption_key_entry.pack()

selected_option = tk.StringVar()
selected_option.set("Single Token")

single_token_radio = tk.Radiobutton(root, text="Single Token", variable=selected_option, value="Single Token")
single_token_radio.pack()

block_token_radio = tk.Radiobutton(root, text="Block Tokens", variable=selected_option, value="Block Tokens")
block_token_radio.pack()

send_button = tk.Button(root, text="Send Selected Data", command=send_selected_data)
send_button.pack()

copy_encrypted_button = tk.Button(root, text="Copy Encrypted Token", command=copy_encrypted_token)
copy_encrypted_button.pack()

tk.Label(root, text="Generated Token/Block:").pack()
token_text = tk.Text(root, height=10, width=50)
token_text.pack()

# Initialize Fernet cipher suite
fernet_key = generate_key()
fernet_cipher_suite = get_fernet_cipher_suite(fernet_key)

# Default encryption settings
current_cipher_suite = fernet_cipher_suite
current_encryption = "Fernet"

root.mainloop()
