import tkinter as tk
import random
import time

SIMBOLURI = ["🍎", "🍒", "🍉", "🍌", "7"] 

class Pacanea:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine")

        self.balanta = 0
        self.pariu = 1

        # Top panel for balanta and add money
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10)

        # balanta display
        self.balanta_label = tk.Label(self.top_frame, text=f"Balanta: $0", font=("Arial", 14))
        self.balanta_label.pack(side=tk.LEFT, padx=20)

        # Add money section
        self.bani_frame = tk.Frame(self.top_frame)
        self.bani_frame.pack(side=tk.RIGHT)

        self.bani_entry = tk.Entry(self.bani_frame, width=10)
        self.bani_entry.pack(side=tk.LEFT, padx=5)

        self.bani_button = tk.Button(self.bani_frame, text="Adauga bani", command=self.bani)
        self.bani_button.pack(side=tk.LEFT)

        # pariu amount section
        self.pariu_frame = tk.Frame(self.root)
        self.pariu_frame.pack(pady=10)

        self.pariu_label = tk.Label(self.pariu_frame, text="Valoare pariu:", font=("Arial", 12))
        self.pariu_label.pack(side=tk.LEFT, padx=5)

        self.pariu_entry = tk.Entry(self.pariu_frame, width=10)
        self.pariu_entry.insert(0, "1")
        self.pariu_entry.pack(side=tk.LEFT, padx=5)

        # Slots display
        self.slots_frame = tk.Frame(self.root)
        self.slots_frame.pack(pady=20)

        self.slots = []
        for _ in range(3):
            label = tk.Label(self.slots_frame, text="-", font=("Arial", 36), width=4)
            label.pack(side=tk.LEFT, padx=10)
            self.slots.append(label)

        # Spin button
        self.spin_button = tk.Button(self.root, text="Invarte!", font=("Arial", 14), command=self.spin)
        self.spin_button.pack(pady=20)

        # Instructions panel
        self.instructions_frame = tk.Frame(self.root, bg="lightgrey", bd=2, relief=tk.SUNKEN)
        self.instructions_frame.pack(padx=10, pady=10, fill=tk.Y)

        instructions = (
            "   - 3 de acelasi fruct => x3 pariul.\n"
            "   - 2 de acelasi fruct => x2 pariul.\n"
            "   - 3 x 7 => x10 pariul.\n"
            "   - 2 x 7 => x5 pariul.\n"
        )

        instructions_label = tk.Label(self.instructions_frame, text=instructions, font=("Arial", 10), justify=tk.LEFT, bg="lightgrey")
        instructions_label.pack(padx=10, pady=10)

    def bani(self):
        try:
            amount = float(self.bani_entry.get())
            if amount <= 0:
                raise ValueError()
            self.balanta += amount
            self.update_balanta_display()
            self.bani_entry.delete(0, tk.END)
        except ValueError:
            self.bani_entry.delete(0, tk.END)
            self.bani_entry.insert(0, "Invalid")

    def update_balanta_display(self):
        self.balanta_label.config(text=f"Balanta: ${self.balanta:.2f}")

    def spin(self):
        try:
            self.pariu = float(self.pariu_entry.get())
            if self.pariu <= 0 or self.pariu > self.balanta:
                raise ValueError()
        except ValueError:
            self.pariu_entry.delete(0, tk.END)
            self.pariu_entry.insert(0, "Invalid")
            return

        self.balanta -= self.pariu  # Deduct pariu amount
        self.update_balanta_display()

        outcomes = []
        for i, slot in enumerate(self.slots):
            for _ in range(10):  # Simulate spinning
                symbol = random.choice(SIMBOLURI)
                slot.config(text=symbol)
                self.root.update()  # Refresh the GUI
                time.sleep(0.1)  # Delay for spinning effect
            outcomes.append(slot.cget("text"))

        self.castiguri(outcomes)

    def castiguri(self, outcomes):
        counts = {symbol: outcomes.count(symbol) for symbol in SIMBOLURI}
        multiplier = 0

        for symbol, count in counts.items():
            if count == 3:
                multiplier = 10 if symbol == "7" else 3
                break
            elif count == 2:
                multiplier = 5 if symbol == "7" else 2

        valoare_castiguri = self.pariu * multiplier
        self.balanta += valoare_castiguri
        self.update_balanta_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = Pacanea(root)
    root.mainloop()
