import tkinter as tk
from PIL import Image, ImageTk  # For working with images
import os
import utils

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
refresh_button = tk.Button(main_canvas , command=lambda: utils.refresh_button(x , y , button1 , button2) , image=refresh_img)
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

# Create the first rectangle with text and a button
canvas1 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas1.place(relx=0.2, rely=0.85, anchor="center")
canvas1.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas1.create_line(10, 50, 190, 50, fill="white", width=2)
canvas1.create_text(100, 30, text="Calin Georgescu", fill="white", font=("Arial", 12, "bold"))
cnt_label1 = tk.Label(canvas1, textvariable=x, bg="black", fg="white", font=("Arial", 14))
cnt_label1.place(x=100, y=70, anchor="center")
button1 = utils.button_gen(canvas1, "Vote", lambda: utils.open_second_program(root , "Calin Georgescu" , x , x , y , button1 , button2), x=100, y=110)

# Create the second rectangle with text and a button
canvas2 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas2.place(relx=0.8, rely=0.85, anchor="center")
canvas2.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas2.create_line(10, 50, 190, 50, fill="white", width=2)
canvas2.create_text(100, 30, text="Elena Lasconi", fill="white", font=("Arial", 12, "bold"))
cnt_label2 = tk.Label(canvas2, textvariable=y, bg="black", fg="white", font=("Arial", 14))
cnt_label2.place(x=100, y=70, anchor="center")
button2 = utils.button_gen(canvas2, "Vote", lambda: utils.open_second_program(root , "Elena Lasconi" , y , x , y , button1 , button2), x=100, y=110)
utils.load_votes(x , y)
if not utils.can_vote(utils.hwid_code):
    button1.config(state="disabled")
    button2.config(state="disabled")
# Start color cycling
utils.color_cycle(root , cnt_label1, cul_G, [0])
utils.color_cycle(root , cnt_label2, cul_L, [0])

root.mainloop()
