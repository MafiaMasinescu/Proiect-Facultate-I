import tkinter as tk
from PIL import Image, ImageTk
import os


class AnimationApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Remove window borders and title bar
        
        # Make the window size to cover the whole screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')  # Full screen size

        # Set the window background to gray
        self.root.config(bg="gray")
        
        # Load and resize images using Pillow
        dir_path = os.path.join(os.path.dirname(__file__))
        # Load and resize main image
        original_main_image = Image.open(os.path.join(dir_path , "simion_sosoaca.png"))
        resized_main_image = original_main_image.resize((500, 500), Image.Resampling.LANCZOS)  # Resize to 300x300 pixels
        self.main_png = ImageTk.PhotoImage(resized_main_image)

        # Load and resize speech bubble image (ensure transparency is preserved)
        original_bubble_image = Image.open(os.path.join(dir_path , "speechbubble.png")).convert("RGBA")
        resized_bubble_image = original_bubble_image.resize((250, 150), Image.Resampling.LANCZOS)  # Resize to 200x100 pixels
        self.speech_bubble = ImageTk.PhotoImage(resized_bubble_image)

        # Create image elements on the canvas
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, highlightthickness=0)
        self.canvas.pack()

        self.main_image = self.canvas.create_image(-100, screen_height // 2, image=self.main_png)  # Start off-screen
        self.bubble_image = self.canvas.create_image(1220, screen_height // 2 - 150, image=self.speech_bubble, state="hidden")

        # Add text for the speech bubble
        self.bubble_text = self.canvas.create_text(
            1220, screen_height // 2 - 150,  # Initial position (matches speech bubble)
            text="Planul Simion!\nVoteaza Simion!",  # The text to display
            fill="black",  # Text color
            font=("Arial", 14, "bold"),  # Font style
            state="hidden"  # Initially hidden
        )

        self.animate_slide_in()

    def animate_slide_in(self):
        def move_left_to_center(x):
            if x < (self.root.winfo_screenwidth() // 2) - 100:  # Stop when reaching the center
                self.canvas.coords(self.main_image, x, self.root.winfo_screenheight() // 2)
                self.root.after(10, move_left_to_center, x + 7)  # Update position every 10ms

        def show_bubble():
            self.canvas.itemconfig(self.bubble_image, state="normal")  # Show speech bubble
            self.canvas.itemconfig(self.bubble_text, state="normal")  # Show text
            self.root.after(5000, hide_bubble)  # Wait 5 seconds before hiding the bubble

        def hide_bubble():
            self.canvas.itemconfig(self.bubble_image, state="hidden")  # Hide speech bubble
            self.canvas.itemconfig(self.bubble_text, state="hidden")  # Hide text
            move_right()

        def move_right():
            def slide_out(x):
                if x < self.root.winfo_screenwidth() + 500:  # Move until off-screen to the right
                    self.canvas.coords(self.main_image, x, self.root.winfo_screenheight() // 2)
                    self.root.after(10, slide_out, x + 7)
                else:
                    root.destroy()
            slide_out(self.root.winfo_screenwidth() // 2)  # Start the right movement from the center

        move_left_to_center(-200)  # Start the slide from left
        self.root.after(3500, show_bubble)  # Show speech bubble after 2.5 seconds


if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationApp(root)
    root.mainloop()
