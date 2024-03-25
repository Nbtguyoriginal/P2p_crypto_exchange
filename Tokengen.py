import tkinter as tk
from tkinter import ttk, messagebox
import random
import datetime

def generate_token():
    date_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    date = date_entry.get()  # Get value from date entry field
    description = description_entry.get()  # Get value from description entry field
    type = type_entry.get()  # Get value from type entry field
    amount = amount_entry.get()
    company = company_entry.get()
    user_id = random.randint(1000, 9999)
    transaction_id = random.randint(10**(int(id_digits_entry.get())-1), 10**int(id_digits_entry.get()) - 1)
    
    token = f"Date-Time: {date_time}, Date: {date}, Description: {description}, Type: {type}, Amount: {amount}, Company: {company}, User ID: {user_id}, Transaction ID: {transaction_id:0{id_digits_entry.get()}d}"
    return token

def generate_single_token():
    token = generate_token()
    token_frame = ttk.Frame(tokens_text)
    token_frame.pack(fill='x')
    token_label = ttk.Label(token_frame, text=token)
    token_label.pack(fill='x')
    copy_button = ttk.Button(token_frame, text="Copy Token", command=lambda: copy_token(token))
    copy_button.pack(side="right")

def generate_block_tokens():
    num_tokens = int(num_tokens_entry.get())
    if num_tokens < 5:
        messagebox.showerror("Error", "Number of tokens should be 5 or more for a block.")
        return
    block_frame = ttk.Frame(tokens_text)
    block_frame.pack(fill='x')
    block_label = ttk.Label(block_frame, text="Block Tokens:")
    block_label.pack(fill='x')
    tokens = []
    for _ in range(num_tokens):
        token = generate_token()
        tokens.append(token)
        token_label = ttk.Label(block_frame, text=token)
        token_label.pack(fill='x')
    copy_button = ttk.Button(block_frame, text="Copy Block Tokens", command=lambda: copy_block_tokens(tokens))
    copy_button.pack(side="right")

def copy_token(token):
    root.clipboard_clear()
    root.clipboard_append(token)
    messagebox.showinfo("Copy Token", "Token copied to clipboard.")

def copy_block_tokens(tokens):
    tokens_text = "\n".join(tokens)
    root.clipboard_clear()
    root.clipboard_append(tokens_text)
    messagebox.showinfo("Copy Block Tokens", "Block tokens copied to clipboard.")

# GUI
root = tk.Tk()
root.title("Token Generator")

tk.Label(root, text="Date:").pack()  # New field
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Description:").pack()  # New field
description_entry = tk.Entry(root)
description_entry.pack()

tk.Label(root, text="Type:").pack()  # New field
type_entry = tk.Entry(root)
type_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Company:").pack()
company_entry = tk.Entry(root)
company_entry.pack()

tk.Label(root, text="Number of Digits in Transaction ID:").pack()  # New field
id_digits_entry = tk.Entry(root)
id_digits_entry.pack()

tk.Label(root, text="Number of Tokens (for block):").pack()
num_tokens_entry = tk.Entry(root)
num_tokens_entry.pack()

single_token_button = tk.Button(root, text="Generate Single Token", command=generate_single_token)
single_token_button.pack()

block_token_button = tk.Button(root, text="Generate Block Tokens", command=generate_block_tokens)
block_token_button.pack()

tk.Label(root, text="Generated Tokens:").pack()
tokens_text = ttk.Frame(root)
tokens_text.pack(fill='both', expand=True)

root.mainloop()
