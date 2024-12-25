import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For working with images
import subprocess
import json
import os

def button_gen(canvas, text, command, x, y):
    # Create the ttk.Button
    button = ttk.Button(
        canvas,
        text=text,
        command=command
        )
    button.place(x=x, y=y, anchor="center")  # Use absolute positioning within the canvas
    return button

def color_cycle(label, colors, color_index): 
    label.config(fg=colors[color_index[0]])
    color_index[0] = (color_index[0] + 1) % len(colors)
    root.after(500, color_cycle, label, colors, color_index)

def save_votes(votG, votL , but1 , but2):
    with open(os.path.join(os.path.dirname(__file__), "votes.json"), "w") as file:
        votes = {"Calin Georgescu": votG.get(), "Elena Lasconi": votL.get() , "Voted": True}
        json.dump(votes, file)
        but1.config(state="disabled")
        but2.config(state="disabled")

def load_votes(x, y  , button1 , button2):
    try:
        with open(os.path.join(os.path.dirname(__file__), "votes.json"), "r") as file:
            votes = json.load(file)
            x.set(votes["Calin Georgescu"])
            y.set(votes["Elena Lasconi"])
            #daca sunt un pic al dracu , NU , TREBUIE SA le si encryptez cu base64 ca sa nu umble toti prosti la ele
            if votes.get("Voted" , False):
                button1.config(state="disabled")
                button2.config(state="disabled")
            else:
                button1.config(state="normal")
                button2.config(state="normal")
    except FileNotFoundError:
        x.set(0)
        y.set(0)
        print("File not found")
    except json.JSONDecodeError:
        x.set(0)
        y.set(0)
        print("JSON decode error")
print(os.path.join(__file__ , "votes.json"))
cul_G = ["red", "yellow", "blue", "white", "blue", "red"]
cul_L = ["red", "orange", "yellow", "green", "blue", "turquoise"]

# Create the main window
root = tk.Tk()
root.geometry("800x600")
root.title("Votati pentru viitorul Romaniei")
root["bg"] = "black"
root.resizable(False , False)
vote_dir = os.path.join(os.path.dirname(__file__))
# Load the images
image_path = os.path.join(vote_dir, "shadowfightvs.png")
center_img = Image.open(image_path).resize((160, 120))  # Resize for ~20% of screen
left_img = Image.open(os.path.join(vote_dir , "giga_georgescu.jfif")).resize((440, 450))    # Full height adjusted
right_img = Image.open(os.path.join(vote_dir , "helicopter.jfif")).resize((440, 450))    # Full height adjusted
refresh_img = Image.open(os.path.join(vote_dir , "refresh.png")).resize((75, 75))    # Full height adjusted
# Convert images for Tkinter
center_photo = ImageTk.PhotoImage(center_img)
left_photo = ImageTk.PhotoImage(left_img)
right_photo = ImageTk.PhotoImage(right_img)
refresh_img = ImageTk.PhotoImage(refresh_img)
# Create the canvas for the background and widgets
main_canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
main_canvas.pack(fill="both", expand=True)

# Add the images to the background
center_id = main_canvas.create_image(400, 300, image=center_photo, anchor="center")  # Center image # Center image
refresh_button = tk.Button(main_canvas , command=lambda: load_votes(x , y , button1 , button2) , image=refresh_img)
refresh_button.place(x=400 , y=500 , anchor="center")
main_canvas.create_image(170, 200, image=left_photo, anchor="center")    # Left image
main_canvas.create_image(650, 200, image=right_photo, anchor="center")   # Right image
main_canvas.tag_raise(center_id)

# Add white sections above and below the center image
main_canvas.create_rectangle(320, 0, 479, 240, fill="white", outline="white")  # Upper white section
main_canvas.create_rectangle(320, 360, 479, 600, fill="white", outline="white")  # Lower white section

# Define variables
x = tk.IntVar(value=0)
y = tk.IntVar(value=0)
def open_second_program(candidate , vot):
    # Crează fereastra secundară
    second_window = tk.Toplevel(root)
    second_window.title("Confirmare Vot")
    second_window.geometry("300x200")

    # Label care arată candidatul ales
    label = tk.Label(second_window, text=f"Vrei să votezi cu {candidate}?")
    label.pack(pady=10)

    def confirm_vote():
        subprocess.Popen(["python", "simion_animation.py"] , creationflags=subprocess.CREATE_NO_WINDOW)
        second_window.destroy()
        vot.set(vot.get() + 1)      
        save_votes(x , y , button1 , button2)
                         
    # Butoane pentru confirmarea votului
    button_yes = tk.Button(second_window, text="Da", command=lambda: confirm_vote())
    button_yes.pack(pady=5)

    button_no = tk.Button(second_window, text="Nu", command=second_window.destroy)
    button_no.pack(pady=5)

# Create the first rectangle with text and a button
canvas1 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas1.place(relx=0.2, rely=0.85, anchor="center")
canvas1.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas1.create_line(10, 50, 190, 50, fill="white", width=2)
canvas1.create_text(100, 30, text="Calin Georgescu", fill="white", font=("Arial", 12, "bold"))
cnt_label1 = tk.Label(canvas1, textvariable=x, bg="black", fg="white", font=("Arial", 14))
cnt_label1.place(x=100, y=70, anchor="center")
button1 = button_gen(canvas1, "Vote", lambda: open_second_program("Calin Georgescu" , x), x=100, y=110)

# Create the second rectangle with text and a button
canvas2 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas2.place(relx=0.8, rely=0.85, anchor="center")
canvas2.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas2.create_line(10, 50, 190, 50, fill="white", width=2)
canvas2.create_text(100, 30, text="Elena Lasconi", fill="white", font=("Arial", 12, "bold"))
cnt_label2 = tk.Label(canvas2, textvariable=y, bg="black", fg="white", font=("Arial", 14))
cnt_label2.place(x=100, y=70, anchor="center")
button2 = button_gen(canvas2, "Vote", lambda: open_second_program("Elena Lasconi" , y), x=100, y=110)
load_votes(x , y , button1 , button2)
# Start color cycling
color_cycle(cnt_label1, cul_G, [0])
color_cycle(cnt_label2, cul_L, [0])

# Start the main event loop
root.mainloop()
