import tkinter as tk
import sys
if getattr(sys, 'frozen', False):  # Running in PyInstaller executable
    sys.path.append(sys._MEIPASS)
import utils
app = tk.Tk()
if len(sys.argv) > 1:
    app.title(f"Launcher de Proiecte - {sys.argv[1]}")
else:
    app.title("Launcher de Proiecte")
app.geometry("600x400")
app.resizable(False, False)
app.attributes("-topmost", True)
app.left_frame = tk.Frame(app, width=200, height= 200 , bg="gray")
app.right_frame = tk.Frame(app, width=200, height= 400)
app.left_frame.pack(side="left" , fill="y")
app.right_frame.pack(side="top" , fill="both")
b1 = utils.select_button_gen(app.left_frame, "Vote App", lambda: utils.update_frame(app , utils.vote_app_content), 100, 30)
b2 = utils.select_button_gen(app.left_frame, "Pacanea", lambda: utils.update_frame(app , utils.pacanea_radu_content), 100, 90)
b3 = utils.select_button_gen(app.left_frame, "Stocks Graphs", lambda: utils.update_frame(app , utils.stocks_app_content), 100, 150)
app.attributes("-topmost", False)
app.mainloop()
