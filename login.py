import time
import importlib.util
import tkinter
import threading
import os
import sys
import hashlib
from base64 import b64encode, b64decode
start_time = time.time()
def check_library(library_name):
    if importlib.util.find_spec(library_name) is not None:
        return True
    import subprocess
    subprocess.run(["pip", "install", library_name], creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL)

check_library("PIL")
check_library("customtkinter")
import customtkinter
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()
app.geometry("800x600")
app.title('Login')
db_client = None

def connect_to_db():
    """Connect to the database in a background thread."""
    global db_client
    check_library("pymongo")
    try:
        from pymongo.mongo_client import MongoClient
        uri = "mongodb+srv://VotantTEST:votant_test_parola@votecluster.bc2p3.mongodb.net/?retryWrites=true&w=majority&appName=VoteCluster"
        db_client = MongoClient(uri , serverSelectionTimeoutMS=5000 , connectTimeoutMS=5000 ) #asteapta 5 secunde daca nu sa conectat nici atunci baga eroare
        db_client.server_info()
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Eroare", e)
threading.Thread(target=connect_to_db, daemon=True).start()

def hash_password(password: str, username: str) -> str:
    """Hash the password using PBKDF2 with a salt based on the username."""
    # Generate a salt from the username (you could add randomness here if needed)
    salt = username.encode()
    
    # Generate the hash using PBKDF2 (100000 iterations for security)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    # Return the hashed password as a base64 string for storage
    return b64encode(hashed_password).decode('utf-8')

def check_password(hashed_password: str, password: str, username: str) -> bool:
    """Check if the entered password matches the stored hash using the same salt."""
    salt = username.encode()
    stored_hash = b64decode(hashed_password.encode())
    
    # Recompute the hash using the same salt and compare
    hashed_attempt = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    
    return hashed_attempt == stored_hash

class LoginPage:
    def __init__(self):
        frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Log into your Account", font=('Century Gothic', 20))
        l2.place(x=50, y=45)

        self.entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=110)

        self.entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password' , show = "*")
        self.entry2.place(x=50, y=163)
        self.usr_empty = None
        self.pasw_empty = None
        self.invalid_login = None
        self.show_password = False
        self.show_password = False

        def toggle_password_visibility():
            if self.show_password:
                self.entry2.configure(show="*")
                toggle_button.configure(text="   🙈   ")

            else:
                self.entry2.configure(show="")
                toggle_button.configure(text="👁️")
            self.show_password = not self.show_password

        toggle_button = customtkinter.CTkButton(master=frame, text="   🙈   ", width=30, height = 25 ,  command=toggle_password_visibility , anchor="center")
        toggle_button.place(x=270, y=165)

        def login_attempt(event=None):
            if self.usr_empty:
                self.usr_empty.destroy()
            if self.pasw_empty:
                self.pasw_empty.destroy()
            if self.invalid_login:
                self.invalid_login.destroy()

            username = self.entry1.get()
            password = self.entry2.get()
            db = db_client['ProiectVotare']
            users_col = db["Users"]
            result = users_col.find_one({"username": username})
            errors = False
            if not username:
                self.usr_empty = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Username can not be empty.", text_color="red")
                self.usr_empty.configure(font=('Century Gothic', 10), fg_color="transparent")
                self.usr_empty.place(x=50, y=140)
                errors = True
            if not password:
                self.pasw_empty = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Password can not be empty.", text_color="red")
                self.pasw_empty.configure(font=('Century Gothic', 10), fg_color="transparent")
                self.pasw_empty.place(x=50, y=195)
                errors = True
            if username and password and result:
                hashed_password = result["password"]
                if not check_password(hashed_password, password, username):
                    self.invalid_login = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Invalid username or password.", text_color="red")
                    self.invalid_login.configure(font=('Century Gothic', 10), fg_color="transparent")
                    self.invalid_login.place(x=50, y=220)
                    errors = True
            if errors:
                return
            print("Login successful.")
            start_launcher(username)

        def on_enter():
            from tkinter import messagebox
            messagebox.showinfo("Teapa", "Nu crezi ca vrei cam multe ?")

        l3 = customtkinter.CTkButton(master=frame, width=5, height=10, text="I forgot my password", command=on_enter, font=('Century Gothic', 10))
        l3.place(x=160, y=210)
        l3.configure(fg_color="transparent")

        button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=login_attempt, corner_radius=6)
        button1.place(x=50, y=240)
        app.bind("<Return>", login_attempt)

        button2 = customtkinter.CTkButton(master=frame, width=220, text="Register", command=RegisterPage, corner_radius=6)
        button2.place(x=50, y=290)

class RegisterPage:
    def __init__(self):
        frame = customtkinter.CTkFrame(master=l1, width=320, height=380, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        l2 = customtkinter.CTkLabel(master=frame, text="Register your Account", font=('Century Gothic', 20))
        l2.place(x=50, y=25)

        self.entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
        self.entry1.place(x=50, y=90)

        self.entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password')
        self.entry2.place(x=50, y=145)

        combo = customtkinter.CTkComboBox(master=frame , values=["Grupa 1" , "Grupa 2" , "Profesor" , "Altcineva"])
        combo.place(x=50, y=200)
        self.usr_exists = None
        self.pasw_exists = None
        self.usr_empty = None
        def register_attempt(event=None):
            if self.usr_exists:
                self.usr_exists.destroy()
            if self.pasw_exists:
                self.pasw_exists.destroy()
            if self.usr_empty:
                self.usr_empty.destroy()
            username = self.entry1.get()
            password = self.entry2.get()
            role = combo.get()
            db = db_client['ProiectVotare']
            users_col = db["Users"]
            result = users_col.find_one({"username": username})
            errors = False
            if not username:
                self.usr_empty = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Username can not be empty.", text_color="red")
                self.usr_empty.configure(font=('Century Gothic', 10), fg_color="transparent")
                self.usr_empty.place(x=50, y=120)
                errors = True
            if not password:
                self.pasw_exists = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Password can not be empty.", text_color="red")
                self.pasw_exists.configure(font=('Century Gothic', 10), fg_color="transparent")
                self.pasw_exists.place(x=50, y=175)
                errors = True
            if result:
                self.usr_exists = customtkinter.CTkLabel(master=frame, width=0, height=0, text="Username already exists.", text_color="red")
                self.usr_exists.configure(font=('Century Gothic', 10), fg_color="transparent")
                self.usr_exists.place(x=50, y=120)
                errors = True
            if errors:
                return
            hashed_password = hash_password(password, username)
            users_col.insert_one({"username": username, "password": hashed_password, "role": role , "voted" : False})
            print("Registered successfully.")
            start_launcher(username)

        button1 = customtkinter.CTkButton(master=frame, width=220, text="Register", command=register_attempt, corner_radius=6)
        button1.place(x=50, y=240)
        app.bind("<Return>", register_attempt)
        button2 = customtkinter.CTkButton(master=frame, width=220, text="Login", corner_radius=6)
        button2.place(x=50, y=290)
        button2.bind("<Button-1>", lambda e: LoginPage())

def start_launcher(username):
    app.destroy()
    import subprocess
    if getattr(sys, 'frozen', False):  # If running as a PyInstaller executable
        launcher_path = os.path.join(sys._MEIPASS, 'launcher.py')
    else:
        launcher_path = os.path.join(os.path.dirname(__file__), 'launcher.py')
    subprocess.Popen(("python", launcher_path , username ), cwd=os.path.dirname(__file__), creationflags=subprocess.CREATE_NO_WINDOW)
    
if getattr(sys, 'frozen', False):  # Check if running as a bundled app
    image_path = os.path.join(sys._MEIPASS, 'pattern.png')
else:
    image_path = os.path.join(os.path.dirname(__file__), 'pattern.png')
img1 = ImageTk.PhotoImage(Image.open(image_path))
l1 = customtkinter.CTkLabel(master=app, image=img1)
l1.pack()
LoginPage()
app.mainloop()
