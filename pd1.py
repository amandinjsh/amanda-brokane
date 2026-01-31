#bibloteku imp.
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox
import os

#šifrešamas loģika
class CryptoManager:
    def __init__(self, key_path="secret.key"):
        self.key_path = key_path
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):#atslegas generesana
        if not os.path.exists(self.key_path):#ja nestrada
            key = Fernet.generate_key()
            with open(self.key_path, "wb") as file:
                file.write(key)
            return key

        with open(self.key_path, "rb") as file:#ja jau ir
            return file.read()

    def encrypt_file(self, path):#datnes sif.
        FileHandler.validate_file(path, require_encrypted=False)#parbauda vaii vis ir

        with open(path, "rb") as file:#nolasa datus
            data = file.read()

        encrypted_data = self.fernet.encrypt(data)#datus sifre

        encrypted_path = path + ".encrypted"#izveido jaunu sifretu failu
        with open(encrypted_path, "wb") as file:
            file.write(encrypted_data)

        return encrypted_path

    def decrypt_file(self, path):#atsifre
        FileHandler.validate_file(path, require_encrypted=True)#ļauj atsifret

        with open(path, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = self.fernet.decrypt(encrypted_data)

        original_path = path.replace(".encrypted", "")# oorģiin. faila atjaunosana
        with open(original_path, "wb") as file:
            file.write(decrypted_data)

        return original_path


class FileHandler:# parbauda drosibu
    @staticmethod#parbauda vai vis ir
    def validate_file(path, require_encrypted=False):
        if not os.path.exists(path):
            raise FileNotFoundError("Izvēlētā datne neeksistē.")

        if require_encrypted and not path.endswith(".encrypted"):
            raise ValueError("Datne nav šifrēta (.encrypted).")

        if not require_encrypted and path.endswith(".encrypted"):
            raise ValueError("Datne jau ir šifrēta.")


class AppGUI:#parada logu
    def __init__(self):
        self.crypto = CryptoManager()

        self.root = tk.Tk()#izveido galveno logu
        self.root.title("Konfidenciālu dokumentu pārvaldība")
        self.root.geometry("420x230")

        self.build_gui()
        self.root.mainloop()

    def build_gui(self):#zskats
        title = tk.Label(
            self.root,
            text="Droša datņu šifrēšana",
            font=("Arial", 14, "bold")
        )
        title.pack(pady=10)

        encrypt_btn = tk.Button(#siifre datn.
            self.root,
            text="Šifrēt datni",
            width=30,
            command=self.encrypt_action
        )
        encrypt_btn.pack(pady=10)

        decrypt_btn = tk.Button(#atsiifre datn.
            self.root,
            text="Atšifrēt datni",
            width=30,
            command=self.decrypt_action
        )
        decrypt_btn.pack(pady=10)

        exit_btn = tk.Button(#iziet poga
            self.root,
            text="Iziet",
            width=30,
            command=self.root.destroy
        )
        exit_btn.pack(pady=10)

    def encrypt_action(self):#kas notiek kad sifre
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            encrypted = self.crypto.encrypt_file(path)#veiiksmes pazin.
            messagebox.showinfo(
                "Veiksmīgi",
                f"Datne šifrēta:\n{encrypted}"
            )
        except Exception as error:#kludu apstrade
            messagebox.showerror("Kļūda", str(error))

    def decrypt_action(self):#poga atsifre
        path = filedialog.askopenfilename()
        if not path:
            return

        try:
            decrypted = self.crypto.decrypt_file(path)
            messagebox.showinfo(
                "Veiksmīgi",
                f"Datne atšifrēta:\n{decrypted}"
            )
        except Exception as error:
            messagebox.showerror("Kļūda", str(error))


if __name__ == "__main__":#prog palaisana
    AppGUI()

