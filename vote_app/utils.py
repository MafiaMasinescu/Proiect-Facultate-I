import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import os
from pymongo.mongo_client import MongoClient

vote_dir = os.path.join(os.path.dirname(__file__))
def button_gen(canvas, text, command, x, y):
    # Create the ttk.Button
    button = ttk.Button(
        canvas,
        text=text,
        command=command
        )
    button.place(x=x, y=y, anchor="center")  # Use absolute positioning within the canvas
    return button
def refresh_button(x , y , button1 , button2):
    load_votes(x , y)
    if can_vote(hwid_code):
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
hwid_col = db["HWID"]
hwid_raw = subprocess.check_output(["wmic", "csproduct", "get", "uuid"], text=True).strip()
hwid_lines = hwid_raw.splitlines()
hwid_code = None
for line in hwid_lines:
    if "UUID" not in line and line.strip():  # Ignore the header and empty lines
        hwid_code = line.strip()
        break
def can_vote(hwid):
    # Query to check if the HWID is in the collection and if it has voted or not
    result = hwid_col.find_one({"HWID": hwid})
    if result:
        # If the HWID is found, check if the user has voted
        if result["Voted"]:
            return False  #a votat deja
        else:
            return True  #nu a votat inca
    else:
        # If the HWID does not exist, allow voting
        return True
def save_votes(votG, votL , but1 , but2):
    update_votes = vot_col.update_one(
        {},  # Specify a filter if needed to select the correct document
        {"$set": {
            "Votes.Calin Georgescu": votG.get(),
            "Votes.Elena Lasconi": votL.get()
        }}  # Use the $set operator to directly set the values
    )
    hwid_col.insert_one({"HWID": hwid_code, "Voted": True})
    print(f"HWID {hwid_code} added to the collection.")
    but1.config(state="disabled")
    but2.config(state="disabled")

def load_votes(x, y):
    result = vot_col.find_one({}, {"Votes.Calin Georgescu"})  # Fetch only Calin Georgescu's votes
    calin_votes = result["Votes"].get("Calin Georgescu")
    result = vot_col.find_one({}, {"Votes.Elena Lasconi"})  # Fetch only Calin Georgescu's votes
    elena_votes = result["Votes"].get("Elena Lasconi")
    x.set(calin_votes)
    y.set(elena_votes)

def open_second_program(root , candidate , vot , x , y , button1 , button2):
    # Crează fereastra secundară
    second_window = tk.Toplevel(root)
    second_window.title("Confirmare Vot")
    second_window.geometry("300x200")

    # Label care arată candidatul ales
    label = tk.Label(second_window, text=f"Vrei să votezi cu {candidate}?")
    label.pack(pady=10)

    def confirm_vote(vote_dir , x , y , button1 , button2):
        subprocess.Popen(["python", "simion_animation.py"] , cwd=vote_dir ,  creationflags=subprocess.CREATE_NO_WINDOW)
        second_window.destroy()
        vot.set(vot.get() + 1)      
        save_votes(x , y , button1 , button2)
                         
    # Butoane pentru confirmarea votului
    button_yes = tk.Button(second_window, text="Da", command=lambda: confirm_vote(vote_dir , x , y , button1 , button2))
    button_yes.pack(pady=5)

    button_no = tk.Button(second_window, text="Nu", command=second_window.destroy)
    button_no.pack(pady=5)
