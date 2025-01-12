import tkinter as tk
from PIL import Image, ImageTk
import os
import utils
import sys
username = "admin"

cul_G = ["red", "yellow", "blue", "white", "blue", "red"]
cul_L = ["red", "orange", "yellow", "green", "blue", "turquoise"]

root = tk.Tk()
root.geometry("800x600")
if len(sys.argv) > 1:
    username = sys.argv[1]
    root.title(f"Voteaza pentru viitorul romaniei {sys.argv[1]}")
    utils.username = username
else:
    root.title("Votati pentru viitorul Romaniei")
root["bg"] = "black"
root.resizable(False , False)
vote_dir = os.path.join(os.path.dirname(__file__))
image_path = os.path.join(vote_dir, "shadowfightvs.png")
center_img = Image.open(image_path).resize((160, 120))
left_img = Image.open(os.path.join(vote_dir , "giga_georgescu.jfif")).resize((440, 450))
right_img = Image.open(os.path.join(vote_dir , "helicopter.jfif")).resize((440, 450))
refresh_img = Image.open(os.path.join(vote_dir , "refresh.png")).resize((75, 75))
# tkinter are arfe
center_photo = ImageTk.PhotoImage(center_img)
left_photo = ImageTk.PhotoImage(left_img)
right_photo = ImageTk.PhotoImage(right_img)
refresh_img = ImageTk.PhotoImage(refresh_img)
main_canvas = tk.Canvas(root, width=800, height=600, bg="black", highlightthickness=0)
main_canvas.pack(fill="both", expand=True)

center_id = main_canvas.create_image(400, 300, image=center_photo, anchor="center")
refresh_button = tk.Button(main_canvas , command=lambda: utils.refresh_button(x , y , button1 , button2) , image=refresh_img)
refresh_button.place(x=400 , y=500 , anchor="center")
main_canvas.create_image(170, 200, image=left_photo, anchor="center")
main_canvas.create_image(650, 200, image=right_photo, anchor="center")
main_canvas.tag_raise(center_id)

main_canvas.create_rectangle(320, 0, 479, 240, fill="white", outline="white")
main_canvas.create_rectangle(320, 360, 479, 600, fill="white", outline="white")
x = tk.IntVar(value=0)
y = tk.IntVar(value=0)

#sect vot g
canvas1 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas1.place(relx=0.2, rely=0.85, anchor="center")
canvas1.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas1.create_line(10, 50, 190, 50, fill="white", width=2)
canvas1.create_text(100, 30, text="Calin Georgescu", fill="white", font=("Arial", 12, "bold"))
cnt_label1 = tk.Label(canvas1, textvariable=x, bg="black", fg="white", font=("Arial", 14))
cnt_label1.place(x=100, y=70, anchor="center")
button1 = utils.button_gen(canvas1, "Vote", lambda: utils.open_second_program(root , "Calin Georgescu" , x , x , y , button1 , button2), x=100, y=110)

#sect vot e
canvas2 = tk.Canvas(main_canvas, width=200, height=150, bg="black", highlightthickness=2, highlightbackground="white")
canvas2.place(relx=0.8, rely=0.85, anchor="center")
canvas2.create_rectangle(10, 10, 190, 140, outline="white", width=2)
canvas2.create_line(10, 50, 190, 50, fill="white", width=2)
canvas2.create_text(100, 30, text="Elena Lasconi", fill="white", font=("Arial", 12, "bold"))
cnt_label2 = tk.Label(canvas2, textvariable=y, bg="black", fg="white", font=("Arial", 14))
cnt_label2.place(x=100, y=70, anchor="center")
button2 = utils.button_gen(canvas2, "Vote", lambda: utils.open_second_program(root , "Elena Lasconi" , y , x , y , button1 , button2), x=100, y=110)
utils.load_votes(x , y)
if not utils.can_vote(username):
    button1.config(state="disabled")
    button2.config(state="disabled")
# ciclu de culor(nu de femei !)
utils.color_cycle(root , cnt_label1, cul_G, [0])
utils.color_cycle(root , cnt_label2, cul_L, [0])

root.mainloop()
