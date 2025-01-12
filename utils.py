import tkinter as tk
import subprocess
import os
import zipfile
import threading
import queue
import sys

class DownloadProgress(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Downloading...")        
        window_width = 350
        window_height = 175
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")        
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()        
        self.status_text = tk.Text(self, height=6, width=45, wrap=tk.WORD)
        self.status_text.pack(pady=10)
        self.status_text.config(state=tk.DISABLED)
        import tkinter.ttk as ttk
        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)        
        self.progress_bar.start(5)
        
        # Queue for thread-safe communication
        self.message_queue = queue.Queue()
        self.check_queue()
    
    def update_status(self, message):
        self.message_queue.put(message)
    
    def check_queue(self):
        try:
            while True:
                message = self.message_queue.get_nowait()
                self.status_text.config(state='normal')
                self.status_text.insert(tk.END, message + "\n")
                self.status_text.see(tk.END)
                self.status_text.config(state='disabled')
        except queue.Empty:
            pass
        finally:
            self.after(100, self.check_queue)
    
    def finish(self):
        self.progress_bar.stop()
        self.destroy()


def select_button_gen(frame, text, command, x, y):
    button = tk.Button(
        frame,
        text=text,
        command=command,
        font=("Arial", 16, "bold"),
        fg="blue",
        bg="#FF6496"
        )
    button.place(x=x, y=y, anchor="center" , width=200 , height=60)
    return button

def update_frame(app , content_function):
    for widget in app.right_frame.winfo_children():
        widget.destroy()
    content_function(app)

class AppSection:
    def __init__(self, app, folder_name, title, description):
        self.app = app
        self.folder_name = folder_name
        self.title = title
        self.description = description
        self.subfolder_path = self.get_subfolder_path()
    
    def get_subfolder_path(self):
        if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
            base_path = os.path.dirname(sys.executable)
        else:  # If running as a Python script
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, self.folder_name)
    
    def create_section(self):
        self.app.right_frame.title = tk.Label(self.app.right_frame, text=self.title, font=("Arial", 24, "bold"))
        self.app.right_frame.title.pack()
        self.app.right_frame.description = tk.Label(
            self.app.right_frame, text=self.description, font=("Arial", 16), wraplength=380
        )
        self.app.right_frame.description.pack()

        if self.check_folder():
            self.add_launch_button()
        else:
            self.add_download_button()
    
    def check_folder(self):
        return os.path.exists(self.subfolder_path)

    def add_launch_button(self):
        window_title = self.app.winfo_toplevel().title()
        username = window_title.replace("Launcher de Proiecte - ", "") if " - " in window_title else ""
        #e ca sa trimiti usernameu mai departe unde va fi nevoie de conturi
        launch_button = tk.Button(
            self.app.right_frame,
            text="Launch",
            font=("Arial", 16, "bold"),
            command=lambda: subprocess.Popen(
                ["python", f"{self.folder_name}.py" , username],
                cwd=self.subfolder_path,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        )
        launch_button.pack(pady=50)

    def add_download_button(self):
        download_button = tk.Button(
            self.app.right_frame,
            text="Download",
            font=("Arial", 16, "bold"),
            command=self.handle_download
        )
        download_button.pack(pady=50)
        self.app.right_frame.download_button = download_button

    def handle_download(self):
        self.app.right_frame.download_button.config(state="disabled", text="Downloading...")

        def download_and_switch():
            download_folder_from_github(self.folder_name, self.app)
            # Update UI after download
            self.app.after(0, lambda: self.app.right_frame.download_button.pack_forget())
            self.add_launch_button()

        download_thread = threading.Thread(target=download_and_switch)
        download_thread.start()

def vote_app_content(app):
    vote_app = AppSection(app , folder_name="vote_app", title="Vote App", description="\n\n\n\n\nMami vreau sa merg sa votez in turu 2 !\nAvem turul 2 acasa\n Turul 2 acasa:")
    vote_app.create_section()

def pacanea_radu_content(app):
    pacanea_radu = AppSection(app , folder_name="pacanea_radu", title="Pacanea Radu", description="\n\n\n\n\n Joc de noroc realizat in python (pacanea)")
    pacanea_radu.create_section()

def stocks_app_content(app):
    stocks_app_content = AppSection(app , folder_name="stocks_app" , title="Stocks Graphs", description="\n\n\n\n\nAplicatie pentru vizualizarea stockurilor sub forma de grafic")
    stocks_app_content.create_section()

def check_library(library_name):
    result = subprocess.run(["pip", "show", library_name], creationflags=subprocess.CREATE_NO_WINDOW , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return True
    else:
        subprocess.run(
            ["pip", "install", library_name], creationflags=subprocess.CREATE_NO_WINDOW , stdout=subprocess.DEVNULL)
        return False

def check_folder(folder):
    if os.path.exists(os.path.join(os.path.dirname(__file__), folder)):
        return True
    else:
        return False
    
def check_libraries_from_file(file_path):
    with open(file_path, 'r') as file:
        libraries = file.readlines()
    libraries = [lib.strip() for lib in libraries if lib.strip()]    
    for library in libraries:
        check_library(library)
    
def download_folder_from_github(local_folder, parent_window):
    progress_window = DownloadProgress(parent_window)
    if check_library("requests"):
        progress_window.update_status("Library requests is installed")
    else:
        progress_window.update_status("Library requests is not installed")
        progress_window.update_status("Downloading library requests")
    import requests

    def perform_download():
        api_url = "https://github.com/MafiaMasinescu/Proiect-Facultate-I/archive/refs/heads/main.zip"

        if getattr(sys, 'frozen', False):  # If running as a PyInstaller bundle
            base_folder = os.path.dirname(sys.argv[0])
        else:  # If running as a Python script
            base_folder = os.path.dirname(os.path.abspath(__file__))

        progress_window.update_status(f"Base folder resolved to: {base_folder}")
        progress_window.update_status("Starting download...")
        response = requests.get(api_url)
        if response.status_code == 200:
            # Save the content to a local file
            zip_filename = os.path.join(base_folder, "Proiect-Facultate-I-main.zip")
            with open(zip_filename, "wb") as file:
                file.write(response.content)
            progress_window.update_status("Download completed successfully.")
            extract_folder = os.path.join(base_folder, "Proiect-Facultate-I-main")
            progress_window.update_status("Extracting files...")
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(base_folder)
            progress_window.update_status(f"Extraction completed. Files extracted to '{extract_folder}'.")
            os.remove(zip_filename)
            progress_window.update_status(f"Removed the ZIP file: {zip_filename}")
            progress_window.update_status("Moving files to final location...")
            move_process = subprocess.Popen(
                ["cmd", "/c", "move",
                 os.path.join(extract_folder, local_folder),
                 base_folder],
                cwd=base_folder,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            move_process.wait()
            check_libraries_from_file(os.path.join(base_folder, f"Proiect-Facultate-I-main/libraries.txt")) 
            import shutil
            if move_process.returncode == 0:
                shutil.rmtree(extract_folder)
            progress_window.update_status("Files moved successfully. Cleanup complete.")
            parent_window.after(1500, progress_window.finish)
        else:
            progress_window.update_status(f"Failed to download. Status code: {response.status_code}")
            parent_window.after(1500, progress_window.finish)

    download_thread = threading.Thread(target=perform_download)
    download_thread.start()
