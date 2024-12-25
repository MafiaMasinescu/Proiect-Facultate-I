import tkinter as tk
import subprocess
import os
import json

votes_json = os.path.join(os.path.dirname(__file__), "vote_app", "votes.json")
def select_button_gen(frame, text, command, x, y):
    button = tk.Button(
        frame,
        text=text,
        command=command,
        font=("Arial", 16, "bold"),
        fg="blue",
        bg="#FF6496"
        )
    button.place(x=x, y=y, anchor="center" , width=200 , height=60)  # Use absolute positioning within the canvas
    return button

def update_frame(app , content_function):
    for widget in app.right_frame.winfo_children():
        widget.destroy()
    content_function(app)

def vote_app_content(app):
    subfolder_path1 = os.path.join(os.path.dirname(__file__), "vote_app")
    app.right_frame.title = tk.Label(app.right_frame, text="Vote App", font=("Arial", 24, "bold"))
    app.right_frame.title.pack()
    app.right_frame.description = tk.Label(app.right_frame, text="\n\n\n\n\nA simple voting application", font=("Arial", 16))
    app.right_frame.description.pack()
    app.right_frame.launch_button = tk.Button(app.right_frame, text="Launch", font=("Arial", 16, "bold"), command=lambda: subprocess.Popen(["python", "vote_app.py"] , cwd = subfolder_path1 , creationflags=subprocess.CREATE_NO_WINDOW))
    app.right_frame.launch_button.pack(pady=50)

def git_content(app):
    subfolder_path2 = os.path.join(os.path.dirname(__file__), "git")
    app.right_frame.title = tk.Label(app.right_frame, text="Git", font=("Arial", 24, "bold"))
    app.right_frame.title.pack()
    app.right_frame.description = tk.Label(app.right_frame, text="\n\n\n\n\nA simple git application", font=("Arial", 16))
    app.right_frame.description.pack()
    app.right_frame.launch_button = tk.Button(app.right_frame, text="Launch", font=("Arial", 16, "bold"), command=lambda: subprocess.Popen(["python", "git.py"] , cwd = subfolder_path2 , creationflags=subprocess.CREATE_NO_WINDOW))
    app.right_frame.launch_button.pack(pady=50)

def load_votes(x, y):
    try:
        with open(os.path.join(os.path.dirname(__file__), "vote_app", "votes.json"), "r") as file:
            votes = json.load(file)
            x.set(votes["Calin Georgescu"])  # Use .set() to update the value
            y.set(votes["Elena Lasconi"])  # Use .set() to update the value
    except FileNotFoundError:
        x.set(0)
        y.set(0)
        print("File not found")
    except json.JSONDecodeError:
        x.set(0)
        y.set(0)
        print("JSON decode error")
