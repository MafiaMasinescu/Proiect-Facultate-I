import tkinter as tk
import os
import utils
app = tk.Tk()
app.title(f"Launcher de Proiecte")
app.geometry("600x400")
app.minsize(600, 400)
subfolder_path1 = os.path.join(os.path.dirname(__file__), "vote_app")
# poti folosi os.listdir() ca sa vezi toate fisierele si pot sa dai un for ca sa treci prin toate proiectele mai usor si dai un except la launcher.py dar pt git nu stiu inca cum sa faci
app.left_frame = tk.Frame(app, width=200, height= 200 , bg="gray")
app.right_frame = tk.Frame(app, width=200, height= 400)
app.left_frame.pack(side="left" , fill="y")
app.right_frame.pack(side="top" , fill="both")
b1 = utils.select_button_gen(app.left_frame, "Vote App", lambda: utils.update_frame(app , utils.vote_app_content), 100, 30)
b2 = utils.select_button_gen(app.left_frame, "Git", lambda: utils.update_frame(app , utils.git_content), 100, 90)
app.mainloop()
