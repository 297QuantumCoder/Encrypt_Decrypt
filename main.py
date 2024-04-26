import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet
import pyperclip

class FileEncryptorDecryptor:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure File Encryption/Decryption Tool")

        self.label = tk.Label(master, text="Select a file:")
        self.label.pack()

        self.encrypt_button = tk.Button(master, text="Encrypt", command=self.encrypt_file)
        self.encrypt_button.pack()

        self.decrypt_button = tk.Button(master, text="Decrypt", command=self.decrypt_file)
        self.decrypt_button.pack()

    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            with open(file_path, 'rb') as file:
                original_data = file.read()
            encrypted_data = cipher_suite.encrypt(original_data)
            with open(file_path + '.encrypted', 'wb') as file:
                file.write(encrypted_data)
            key_str = key.decode()
            pyperclip.copy(key_str)
            messagebox.showinfo("Encryption", f"File encrypted successfully!\nKey: {key_str}\nKey copied to clipboard.")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename()
        if file_path.endswith('.encrypted'):
            key = simpledialog.askstring("Input Key", "Enter the key used for encryption:")
            if key:
                try:
                    cipher_suite = Fernet(key.encode())
                    with open(file_path, 'rb') as file:
                        encrypted_data = file.read()
                    decrypted_data = cipher_suite.decrypt(encrypted_data)
                    with open(file_path[:-10], 'wb') as file:
                        file.write(decrypted_data)
                    messagebox.showinfo("Decryption", "File decrypted successfully!")
                except Exception as e:
                    messagebox.showerror("Decryption Error", "Failed to decrypt file. Please check the key.")
        else:
            messagebox.showerror("Decryption Error", "Selected file is not encrypted!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileEncryptorDecryptor(root)
    root.mainloop()
