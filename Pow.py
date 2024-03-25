import tkinter as tk
import random
import hashlib
from threading import Thread, Lock
from time import time

class PoW_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Proof-of-Work (PoW) GUI")
        
        # Block data entry
        self.block_label = tk.Label(self.root, text="input:Block Data:")
        self.block_label.grid(row=0, column=0)
        self.block_entry = tk.Entry(self.root, width=40)
        self.block_entry.grid(row=0, column=1)

        # Difficulty level suggestion
        self.difficulty_suggestion_label = tk.Label(self.root, text="token Difficulty Suggestion:")
        self.difficulty_suggestion_label.grid(row=1, column=0)
        self.difficulty_suggestion_text = tk.Text(self.root, height=1, width=20)
        self.difficulty_suggestion_text.grid(row=1, column=1)

        # Difficulty level entry
        self.difficulty_label = tk.Label(self.root, text="Difficulty Level:")
        self.difficulty_label.grid(row=2, column=0)
        self.difficulty_entry = tk.Entry(self.root)
        self.difficulty_entry.grid(row=2, column=1)

        # Nonce display
        self.nonce_label = tk.Label(self.root, text="Nonce:")
        self.nonce_label.grid(row=3, column=0)
        self.nonce_text = tk.Text(self.root, height=1, width=20)
        self.nonce_text.grid(row=3, column=1)

        # Hash display
        self.hash_label = tk.Label(self.root, text="Hash:")
        self.hash_label.grid(row=4, column=0)
        self.hash_text = tk.Text(self.root, height=5, width=40)
        self.hash_text.grid(row=4, column=1, rowspan=5)

        # Start buttons
        self.simple_solve_button = tk.Button(self.root, text="Quick solve", command=self.simple_solve)
        self.simple_solve_button.grid(row=9, column=0)
        self.unlocked_solve_button = tk.Button(self.root, text="multi cell solve", command=self.unlocked_solve)
        self.unlocked_solve_button.grid(row=9, column=1)

        # Copy hash button
        self.copy_hash_button = tk.Button(self.root, text="Copy Final Hash", command=self.copy_hash)
        self.copy_hash_button.grid(row=10, columnspan=2)

        self.lock = Lock()  # Lock for synchronization
        self.start_time = None
        self.end_time = None

        self.root.mainloop()

    def start_timer(self):
        self.start_time = time()

    def stop_timer(self):
        self.end_time = time()

    def get_elapsed_time(self):
        if self.start_time is None or self.end_time is None:
            return None
        return self.end_time - self.start_time

    def calculate_difficulty_suggestion(self, block_data):
        # Heuristic approach to suggest difficulty based on block data complexity
        data_length = len(block_data)
        if data_length < 50:
            return "Medium", None
        elif data_length < 100:
            return "Hard", None
        else:
            return "Very Hard", None

    def generate_random_difficulty(self, difficulty):
        if difficulty == "Hard":
            return random.randint(100, 1000)
        elif difficulty == "Medium":
            return random.randint(50, 100)
        else:
            return None

    def proof_of_work_range(self, block, start_nonce, end_nonce, difficulty, result):
        nonce = start_nonce
        while nonce < end_nonce:
            # Concatenate the block data and nonce
            data = f"{block}{nonce}"
            # Calculate the hash of the data
            hash_result = hashlib.sha256(data.encode()).hexdigest()
            # Check if the hash meets the difficulty requirement
            if hash_result.startswith('0' * difficulty):
                with self.lock:
                    result['nonce'] = nonce
                    result['hash'] = hash_result
                    return
            nonce += 1

    def unlocked_solve(self):
        block_data = self.block_entry.get()
        user_difficulty = self.difficulty_entry.get()
        if user_difficulty:
            difficulty_level = int(user_difficulty)
        else:
            suggested_difficulty, _ = self.calculate_difficulty_suggestion(block_data)
            self.difficulty_suggestion_text.delete(1.0, tk.END)
            self.difficulty_suggestion_text.insert(tk.END, suggested_difficulty)
            difficulty_level = _

        # Start the timer
        self.start_timer()

        num_threads = 4  # Number of threads to use
        nonce_range = 2**32  # Range of nonce values to check
        step = nonce_range // num_threads

        results = [{'nonce': None, 'hash': None} for _ in range(num_threads)]

        threads = []
        for i in range(num_threads):
            start_nonce = i * step
            end_nonce = (i + 1) * step if i < num_threads - 1 else nonce_range
            thread = Thread(target=self.proof_of_work_range,
                            args=(block_data, start_nonce, end_nonce, difficulty_level, results[i]))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Stop the timer
        self.stop_timer()

        # Display elapsed time
        elapsed_time = self.get_elapsed_time()
        if elapsed_time:
            print(f"Elapsed Time: {elapsed_time} seconds")

        # Find the first result with a valid nonce
        for result in results:
            if result['nonce'] is not None:
                self.nonce_text.delete(1.0, tk.END)
                self.nonce_text.insert(tk.END, str(result['nonce']))
                self.hash_text.delete(1.0, tk.END)
                self.hash_text.insert(tk.END, f"Hash: {result['hash']}")
                break

    def proof_of_work(self, block, difficulty):
        nonce = 0
        while True:
            # Concatenate the block data and nonce
            data = f"{block}{nonce}"
            # Calculate the hash of the data
            hash_result = hashlib.sha256(data.encode()).hexdigest()
            # Display the hash for each attempted nonce
            self.hash_text.insert(tk.END, f"Nonce: {nonce}, Hash: {hash_result}\n")
            # Update the GUI to show the current nonce
            self.nonce_text.delete(1.0, tk.END)
            self.nonce_text.insert(tk.END, str(nonce))
            self.nonce_text.update()
            # Check if the hash meets the difficulty requirement
            if hash_result.startswith('0' * difficulty):
                return nonce
            nonce += 1

    def simple_solve(self):
        block_data = self.block_entry.get()
        user_difficulty = self.difficulty_entry.get()
        if user_difficulty:
            difficulty_level = int(user_difficulty)
        else:
            suggested_difficulty, suggested_difficulty_num = self.calculate_difficulty_suggestion(block_data)
            self.difficulty_suggestion_text.delete(1.0, tk.END)
            self.difficulty_suggestion_text.insert(tk.END, suggested_difficulty)
            difficulty_level = suggested_difficulty_num

        # Clear previous results
        self.nonce_text.delete(1.0, tk.END)
        self.hash_text.delete(1.0, tk.END)

        # Start the timer
        self.start_timer()

        nonce_value = self.proof_of_work(block_data, difficulty_level)

        # Stop the timer
        self.stop_timer()

        # Display elapsed time
        elapsed_time = self.get_elapsed_time()
        if elapsed_time:
            print(f"Elapsed Time: {elapsed_time} seconds")

        self.nonce_text.insert(tk.END, str(nonce_value))

    def copy_hash(self):
        final_hash = self.hash_text.get("end-2l", "end-1c")  # Get the final correct hash
        self.root.clipboard_clear()  # Clear the clipboard
        self.root.clipboard_append(final_hash)  # Append the final correct hash to the clipboard

        self.root.update()  # Update the clipboard

# Create an instance of the GUI
PoW_GUI()
