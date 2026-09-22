import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("620x720")
        self.root.resizable(False, False)

        self.history = []
        self.current_password = ""

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.exclude_var = tk.BooleanVar(value=False)

        self.build_interface()

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="Advanced Password Generator",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Generate strong cryptographically secure passwords",
            font=("Arial", 10)
        )
        subtitle.pack(pady=(0, 20))

        settings = ttk.LabelFrame(
            self.root,
            text="Password Settings",
            padding=15
        )
        settings.pack(fill="x", padx=30, pady=10)

        tk.Label(
            settings,
            text="Password Length:"
        ).grid(row=0, column=0, sticky="w")

        self.length_spinbox = tk.Spinbox(
            settings,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=8
        )
        self.length_spinbox.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.length_scale = ttk.Scale(
            settings,
            from_=8,
            to=64,
            variable=self.length_var,
            command=self.update_length
        )
        self.length_scale.grid(
            row=0,
            column=2,
            padx=10,
            pady=5,
            sticky="ew"
        )

        settings.columnconfigure(2, weight=1)

        types = ttk.LabelFrame(
            self.root,
            text="Character Types",
            padding=15
        )
        types.pack(fill="x", padx=30, pady=10)

        ttk.Checkbutton(
            types,
            text="Uppercase Letters (A-Z)",
            variable=self.upper_var
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types,
            text="Lowercase Letters (a-z)",
            variable=self.lower_var
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types,
            text="Numbers (0-9)",
            variable=self.number_var
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types,
            text="Symbols (!@#$...)",
            variable=self.symbol_var
        ).pack(anchor="w", pady=3)

        ttk.Checkbutton(
            types,
            text="Exclude ambiguous characters (0, O, l, 1)",
            variable=self.exclude_var
        ).pack(anchor="w", pady=8)

        password_frame = ttk.LabelFrame(
            self.root,
            text="Generated Password",
            padding=15
        )
        password_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        self.password_entry = tk.Entry(
            password_frame,
            font=("Consolas", 16),
            justify="center",
            state="readonly"
        )
        self.password_entry.pack(
            fill="x",
            pady=5
        )

        self.strength_label = tk.Label(
            password_frame,
            text="Strength: —",
            font=("Arial", 11, "bold")
        )
        self.strength_label.pack(pady=5)

        self.strength_bar = ttk.Progressbar(
            password_frame,
            orient="horizontal",
            length=450,
            mode="determinate",
            maximum=100
        )
        self.strength_bar.pack(
            fill="x",
            pady=5
        )

        buttons = tk.Frame(self.root)
        buttons.pack(pady=15)

        ttk.Button(
            buttons,
            text="Generate Password",
            command=self.generate_password
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons,
            text="Copy Password",
            command=self.copy_password
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            buttons,
            text="Clear",
            command=self.clear_password
        ).grid(row=0, column=2, padx=5)

        history_frame = ttk.LabelFrame(
            self.root,
            text="Generation History — Last 5",
            padding=10
        )
        history_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.history_list = tk.Listbox(
            history_frame,
            font=("Consolas", 11),
            height=6
        )
        self.history_list.pack(
            fill="both",
            expand=True,
            side="left"
        )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_list.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.history_list.config(
            yscrollcommand=scrollbar.set
        )

    def update_length(self, value):
        self.length_var.set(int(float(value)))

    def get_character_sets(self):
        selected = []

        if self.upper_var.get():
            selected.append(string.ascii_uppercase)

        if self.lower_var.get():
            selected.append(string.ascii_lowercase)

        if self.number_var.get():
            selected.append(string.digits)

        if self.symbol_var.get():
            selected.append(string.punctuation)

        if self.exclude_var.get():
            selected = [
                chars.replace("0", "")
                .replace("O", "")
                .replace("l", "")
                .replace("1", "")
                for chars in selected
            ]

        return [chars for chars in selected if chars]

    def generate_password(self):
        try:
            length = int(self.length_var.get())
        except (ValueError, TypeError):
            messagebox.showerror(
                "Invalid Length",
                "Password length must be a number."
            )
            return

        if length < 8:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 8 characters."
            )
            return

        if length > 64:
            messagebox.showerror(
                "Invalid Length",
                "Password length cannot exceed 64 characters."
            )
            return

        character_sets = self.get_character_sets()

        if not character_sets:
            messagebox.showerror(
                "No Character Types",
                "Select at least one character type."
            )
            return

        if length < len(character_sets):
            messagebox.showerror(
                "Invalid Length",
                "Password length is too short for the selected character types."
            )
            return

        password_characters = []

        for character_set in character_sets:
            password_characters.append(
                secrets.choice(character_set)
            )

        all_characters = "".join(character_sets)

        for _ in range(length - len(password_characters)):
            password_characters.append(
                secrets.choice(all_characters)
            )

        secrets.SystemRandom().shuffle(password_characters)

        password = "".join(password_characters)

        self.current_password = password

        self.password_entry.config(state="normal")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")

        self.update_strength(
            password,
            len(character_sets)
        )

        self.copy_to_clipboard(password, show_message=False)

        self.add_to_history(password)

    def update_strength(self, password, diversity):
        length = len(password)

        score = 0

        if length >= 12:
            score += 30
        elif length >= 8:
            score += 15

        if length >= 16:
            score += 20

        if diversity >= 2:
            score += 20

        if diversity >= 3:
            score += 15

        if diversity >= 4:
            score += 15

        if score < 40:
            strength = "Weak"
        elif score < 75:
            strength = "Medium"
        else:
            strength = "Strong"

        self.strength_label.config(
            text=f"Strength: {strength}"
        )

        self.strength_bar["value"] = score

    def copy_password(self):
        if not self.current_password:
            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )
            return

        self.copy_to_clipboard(self.current_password, show_message=True)

    def copy_to_clipboard(self, password, show_message):
        try:
            pyperclip.copy(password)
        except pyperclip.PyperclipException:
            messagebox.showwarning(
                "Clipboard Unavailable",
                "The password was generated, but it could not be copied "
                "to the clipboard."
            )
            return False

        if show_message:
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard."
            )

        return True

    def add_to_history(self, password):
        self.history.insert(0, password)

        if len(self.history) > 5:
            self.history.pop()

        self.history_list.delete(0, tk.END)

        for item in self.history:
            self.history_list.insert(
                tk.END,
                item
            )

    def clear_password(self):
        self.current_password = ""

        self.password_entry.config(
            state="normal"
        )
        self.password_entry.delete(
            0,
            tk.END
        )
        self.password_entry.config(
            state="readonly"
        )

        self.strength_label.config(
            text="Strength: —"
        )

        self.strength_bar["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()