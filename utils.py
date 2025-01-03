import tkinter as tk
import subprocess
import os
import json
import zipfile
import io

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
    check_folder("vote_app")
    subfolder_path1 = os.path.join(os.path.dirname(__file__), "vote_app")
    app.right_frame.title = tk.Label(app.right_frame, text="Vote App", font=("Arial", 24, "bold"))
    app.right_frame.title.pack()
    app.right_frame.description = tk.Label(app.right_frame, text="\n\n\n\n\nVotati patrupedul uleiat MEDELEANUL", font=("Arial", 16))
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

def check_library(library_name):
    result = subprocess.run(["pip", "show", library_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print(f"The library '{library_name}' is installed.")
    else:
        os.system(f"pip install {library_name}")

def check_folder(folder):
    if os.path.exists(os.path.join(os.path.dirname(__file__), folder)):
        print(f"The folder '{folder}' exists.")
        return True
    else:
        print(f"The folder '{folder}' does not exist.")
        download_folder_from_github(f"Proiect-Facultate-I-main/{folder}" , folder)
    
def download_folder_from_github(folder_path , local_folder):
    # Construct the API URL for the specific folder
    api_url = "https://github.com/MafiaMasinescu/Proiect-Facultate-I/archive/refs/heads/main.zip"
    check_library("requests")
    import requests
    import shutil
    response = requests.get(api_url)
    current_folder = os.path.dirname(__file__)
    if response.status_code == 200:
    # Save the content to a local file
        zip_filename = "Proiect-Facultate-I-main.zip"
        with open("Proiect-Facultate-I-main.zip", "wb") as file:
            file.write(response.content)
        print("Download completed successfully.")
        extract_folder = "Proiect-Facultate-I-main"
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(__file__))
        print(f"Extraction completed. Files are extracted to '{extract_folder}'.")

    # Optionally, delete the ZIP file after extraction
        os.remove(zip_filename)
        print(f"Removed the ZIP file: {zip_filename}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

    move_process = subprocess.Popen(["cmd" , "/c" , "move", os.path.join(os.path.dirname(__file__) , "Proiect-Facultate-I-main" , "vote_app"), current_folder], cwd=current_folder, creationflags=subprocess.CREATE_NO_WINDOW)
    move_process.wait()
    if move_process.returncode == 0:
        shutil.rmtree(os.path.join(os.path.dirname(__file__) , "Proiect-Facultate-I-main"))



