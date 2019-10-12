#!/usr/bin/env python3
"""
    Name: ASEfile
    Type: Encryption file App
    Credits: "EncryptionScript" class from "github.com/mak23" for file encryption
"""

import os
import sys
import hashlib
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Cryptodome.Cipher import AES


class EncryptionScript:
    """ "EncryptionScript" class from "github.com/mak23" for file encryption.
    (Has been modified a bit.) """
    def __init__(self, user_file, user_key, user_salt):
        # get the path to input file
        self.user_file = user_file
        
        # convert the key and salt to bytes
        self.user_key = bytes(user_key, "utf-8")
        self.user_salt = bytes(user_key[::-1], "utf-8")

        # get the file extension
        self.file_extension = self.user_file.split(".")[-1]
        
        # hash type for hashing key and salt
        self.hash_type = "SHA256"

        # encrypted file name
        self.encrypt_output_file = ".".join(self.user_file.split(".")[:-1]) + "." + self.file_extension + ".ASE"

        # decrypted file name
        self.decrypt_output_file = self.user_file[:-5]

        # dictionary to store hashed key and salt
        self.hashed_key_salt = dict()

        # hash key and salt into 16 bit hashes
        self.hash_key_salt()

    def encrypt(self):
        # create a cipher object
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )

        # read content of file
        with open(self.user_file, "rb") as f:
            content = f.read()

        # encrypt the file contents
        encrypted_content = cipher_object.encrypt(content)

        #  write the encrypted content to output file
        with open(self.encrypt_output_file, "wb") as g:
            g.write(encrypted_content)

        # clean up the cipher object
        del cipher_object

    def decrypt(self):
        #  exact same as above function except in reverse
        cipher_object = AES.new(
            self.hashed_key_salt["key"],
            AES.MODE_CFB,
            self.hashed_key_salt["salt"]
        )

        # read content of file
        with open(self.user_file, "rb") as f:
            content = f.read()

        # decrypt the file contents
        decrypted_content = cipher_object.decrypt(content)

        #  write the decrypted content to output file
        with open(self.decrypt_output_file, "wb") as g:
            g.write(decrypted_content)

        # clean up the cipher object
        del cipher_object

    def hash_key_salt(self):
        # --- convert key to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_key)

        # turn the output key hash into 32 bytes (256 bits)
        self.hashed_key_salt["key"] = bytes(hasher.hexdigest()[:32], "utf-8")

        # clean up hash object
        del hasher

        # --- convert salt to hash
        #  create a new hash object
        hasher = hashlib.new(self.hash_type)
        hasher.update(self.user_salt)

        # turn the output salt hash into 16 bytes (128 bits)
        self.hashed_key_salt["salt"] = bytes(hasher.hexdigest()[:16], "utf-8")
        
        # clean up hash object
        del hasher


class MainWindow:
    """ GUI Wrapper """

    # configure root directory path relative to this file
    THIS_FOLDER_G = ""
    if getattr(sys, "frozen", False):
        # frozen
        THIS_FOLDER_G = os.path.dirname(sys.executable)
    else:
        # unfrozen
        THIS_FOLDER_G = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, root):
        self.root = root
        self._cipher = None
        self._file_url = tk.StringVar()
        self._secret_key = tk.StringVar()
        self._salt = tk.StringVar()
        self._status = tk.StringVar()
        self._status.set("ASE")

        root.title("ASEfile")
        root.configure(bg="#e7eaf6")

        try:
            icon_img = tk.Image(
                "photo",
                file=self.THIS_FOLDER_G + "/file/icon.png"
            )
            root.call(
                "wm",
                "iconphoto",
                root._w,
                icon_img
            )
        except Exception as e:
            # print(e)
            pass

        self.menu_bar = tk.Menu(
            root,
            bg="#e7eaf6",
            relief=tk.FLAT
        )
        self.menu_bar.add_command(
            label="معلومات",
            command=self.show_help_callback
        )
        self.menu_bar.add_command(
            label="خروج",
            command=root.quit
        )

        root.configure(
            menu=self.menu_bar
        )

        self.file_entry_label = tk.Label(
            root,
            text="ادخل مسار الملف او اختار المسار الملف",
            bg="#e7eaf6",
            anchor=tk.W
        )
        self.file_entry_label.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=0,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.file_entry = tk.Entry(
            root,
            textvariable=self._file_url,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT
        )
        self.file_entry.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=6,
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.select_btn = tk.Button(
            root,
            text="اختار الملف",
            command=self.selectfile_callback,
            width=42,
            bg="#A4A939",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.select_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=2,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.key_entry_label = tk.Label(
            root,
            text="-ادخل المفتاح الخاص -ارجو حفظ المفتاح لأستخدامه فى فك التشفير",
            bg="#e7eaf6",
            anchor=tk.W
        )
        self.key_entry_label.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=3,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.key_entry = tk.Entry(
            root,
            textvariable=self._secret_key,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT
        )
        self.key_entry.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=6,
            row=4,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        # self.salt_entry_label = tk.Label(
        #     root,
        #     text="Enter Salt",
        #     bg="#e7eaf6",
        #     anchor=tk.W
        # )
        # self.salt_entry_label.grid(
        #     padx=12,
        #     pady=(6, 0),
        #     ipadx=0,
        #     ipady=1,
        #     row=5,
        #     column=0,
        #     columnspan=4,
        #     sticky=tk.W+tk.E+tk.N+tk.S
        # )

        # self.salt_entry = tk.Entry(
        #     root,
        #     textvariable=self._salt,
        #     bg="#fff",
        #     exportselection=0,
        #     relief=tk.FLAT
        # )
        # self.salt_entry.grid(
        #     padx=15,
        #     pady=6,
        #     ipadx=8,
        #     ipady=6,
        #     row=6,
        #     column=0,
        #     columnspan=4,
        #     sticky=tk.W+tk.E+tk.N+tk.S
        # )
        
        self.encrypt_btn = tk.Button(
            root,
            text="تشفير",
            command=self.encrypt_callback,
            bg="#AA7239",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.encrypt_btn.grid(
            padx=(15, 6),
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=0,
            columnspan=2,
            sticky=tk.W+tk.E+tk.N+tk.S
        )
        
        self.decrypt_btn = tk.Button(
            root,
            text="فك التشفير",
            command=self.decrypt_callback,
            bg="#226666",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.decrypt_btn.grid(
            padx=(6, 15),
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=2,
            columnspan=2,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.clear_btn = tk.Button(
            root,
            text="مسح البيانات",
            command=self.clear_callback,
            bg="#AA3939",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT
        )
        self.clear_btn.grid(
            padx=15,
            pady=(4, 12),
            ipadx=24,
            ipady=6,
            row=8,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.status_label = tk.Label(
            root,
            textvariable=self._status,
            bg="#e7eaf6",
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.FLAT,
            wraplength=350
        )
        self.status_label.grid(
            padx=12,
            pady=(0, 12),
            ipadx=0,
            ipady=1,
            row=9,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 2, weight=1)
        tk.Grid.columnconfigure(root, 3, weight=1)

    def selectfile_callback(self):
        name = filedialog.askopenfile()
        try:
            self._file_url.set(name.name)
            # print(name.name)
        except Exception as e:
            # print(e)
            pass

    def encrypt_callback(self):
        try:
            self._cipher = EncryptionScript(
                self._file_url.get(),
                self._secret_key.get(),
                self._salt.get()
            )
            self._cipher.encrypt()
            self._cipher = None
            self._status.set("تم تشفير الملف")
        except Exception as e:
            # print(e)
            self._status.set(e)

    def decrypt_callback(self):
        try:
            self._cipher = EncryptionScript(
                self._file_url.get(),
                self._secret_key.get(),
                self._salt.get()
            )
            self._cipher.decrypt()
            self._cipher = None
            self._status.set("تم فك تشفير الملف")
        except Exception as e:
            # print(e)
            self._status.set(e)

    def clear_callback(self):
        self._cipher = None
        self._file_url.set("")
        self._secret_key.set("")
        self._salt.set("")
        self._status.set("---")

    def show_help_callback(self):
        messagebox.showinfo(
            "معلومات",
     """1. اضغط على اختار الملف واختار ملف نصي او صورة او ملف مضغوط
2. ادخل المفتاح الخاص لتشفير الملف ,تذكر هذا المفتاح لأستخدامه فى فك التشفير لأحقا 
3. اضغط على تشفير لتشفير الملف سيظهر ملف بصيغة (.ASE)
4. عند فك التشفير اختار الملف المراد فك تشفيرة وادخل المفتاح الخاص  ثم ستظهر الملف بالصيغة الحقيقة 
5.  اضغط على مسح لمسح المعلومات """
        )


if __name__ == "__main__":
    ROOT = tk.Tk()
    MAIN_WINDOW = MainWindow(ROOT)
    ROOT.mainloop()
