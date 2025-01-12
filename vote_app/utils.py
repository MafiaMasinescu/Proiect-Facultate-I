import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import os
from pymongo.mongo_client import MongoClient

username = "admin"
vote_dir = os.path.join(os.path.dirname(__file__))
def button_gen(canvas, text, command, x, y):
    button = ttk.Button(
        canvas,
        text=text,
        command=command
        )
    button.place(x=x, y=y, anchor="center")
    return button
def refresh_button(x , y , button1 , button2):
    load_votes(x , y)
    if can_vote(username):
        button1.config(state="enabled")
        button2.config(state="enabled")

def color_cycle(root , label, colors, color_index): 
    label.config(fg=colors[color_index[0]])
    color_index[0] = (color_index[0] + 1) % len(colors)
    root.after(500, color_cycle, root , label, colors, color_index)

uri = "mongodb+srv://VotantTEST:votant_test_parola@votecluster.bc2p3.mongodb.net/?retryWrites=true&w=majority&appName=VoteCluster"
client = MongoClient(uri)
db = client['ProiectVotare']
vot_col = db["Voturi"]
user_col = db["Users"]

def can_vote(username):
    result = user_col.find_one({"username": username})
    
    if result:
        if result.get("voted", False):
            return False  # a votat
        else:
            return True
    return False

def save_votes(username , votG, votL , but1 , but2):
    update_votes = vot_col.update_one(
        {},  # Specify a filter if needed to select the correct document
        {"$set": {
            "Votes.Calin Georgescu": votG.get(),
            "Votes.Elena Lasconi": votL.get()
        }}
    )
    user_col.update_one(
        {"username": username},
        {"$set": {"voted": True}}
    )
    but1.config(state="disabled")
    but2.config(state="disabled")

def load_votes(x, y):
    result = vot_col.find_one({}, {"Votes.Calin Georgescu"})
    calin_votes = result["Votes"].get("Calin Georgescu")
    result = vot_col.find_one({}, {"Votes.Elena Lasconi"})
    elena_votes = result["Votes"].get("Elena Lasconi")
    x.set(calin_votes)
    y.set(elena_votes)

def open_second_program(root , candidate , vot , x , y , button1 , button2):
    # Crează fereastra secundară
    second_window = tk.Toplevel(root)
    second_window.title("Confirmare Vot")
    second_window.geometry("300x200")
    label = tk.Label(second_window, text=f"Vrei să votezi cu {candidate}?")
    label.pack(pady=10)

    def confirm_vote(vote_dir , x , y , button1 , button2):
        subprocess.Popen(["python", "simion_animation.py"] , cwd=vote_dir ,  creationflags=subprocess.CREATE_NO_WINDOW)
        second_window.destroy()
        vot.set(vot.get() + 1)      
        save_votes(username , x , y , button1 , button2)                         
    button_yes = tk.Button(second_window, text="Da", command=lambda: confirm_vote(vote_dir , x , y , button1 , button2))
    button_yes.pack(pady=5)
    button_no = tk.Button(second_window, text="Nu", command=second_window.destroy)
    button_no.pack(pady=5)
