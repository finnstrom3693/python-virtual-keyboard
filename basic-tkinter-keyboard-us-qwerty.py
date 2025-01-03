import tkinter as tk
from tkinter import ttk

# Define the US QWERTY layout
KEYS = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
    ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['CapsLock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'],
    ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
    ['Space']
]

class OnScreenKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("On-Screen Keyboard")

        # State variables for Shift and CapsLock
        self.shift_active = False
        self.caps_lock_active = False
        self.buttons = {}

        # Create the text box with larger dimensions
        self.text_box = tk.Text(root, height=20, width=80, wrap=tk.WORD, font=("Courier New", 12))
        self.text_box.pack(pady=10, padx=10)

        # Copy to Clipboard button
        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)

        # Create the keyboard frame
        self.keyboard_frame = ttk.Frame(root)
        self.keyboard_frame.pack()

        self.create_keyboard()

    def create_keyboard(self):
        for row_index, row in enumerate(KEYS):
            frame = ttk.Frame(self.keyboard_frame)
            frame.pack()

            for key in row:
                if key == 'Space':
                    button = ttk.Button(frame, text=key, command=lambda k=key: self.key_press(k), width=40)
                else:
                    button = ttk.Button(frame, text=key, command=lambda k=key: self.key_press(k), width=5)
                button.pack(side=tk.LEFT, padx=2, pady=2)
                self.buttons[key] = button

    def key_press(self, key):
        if key == 'Backspace':
            content = self.text_box.get("1.0", tk.END)
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert("1.0", content[:-2])  # Remove the last character
        elif key == 'Enter':
            self.text_box.insert(tk.END, '\n')
        elif key == 'Tab':
            self.text_box.insert(tk.END, '\t')
        elif key == 'CapsLock':
            self.caps_lock_active = not self.caps_lock_active
            self.update_displayed_keys()
        elif key == 'Shift':
            self.shift_active = not self.shift_active
            self.update_displayed_keys()
        elif key == 'Space':
            self.text_box.insert(tk.END, ' ')
        else:
            if self.shift_active:
                shift_map = {
                    '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
                    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+',
                    '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<',
                    '.': '>', '/': '?'
                }
                key = shift_map.get(key, key.upper())
                self.shift_active = False  # Reset shift after use
                self.update_displayed_keys()
            elif self.caps_lock_active:
                key = key.upper()
            else:
                key = key.lower()

            self.text_box.insert(tk.END, key)

    def update_displayed_keys(self):
        shift_map = {
            '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+',
            '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<',
            '.': '>', '/': '?'
        }
        for key, button in self.buttons.items():
            if key in shift_map:
                if self.shift_active:
                    button.config(text=shift_map[key])
                elif self.caps_lock_active and key.isalpha():
                    button.config(text=key.upper())
                else:
                    button.config(text=key)
            elif key.isalpha():
                if self.caps_lock_active:
                    button.config(text=key.upper())
                else:
                    button.config(text=key.lower())
            else:
                button.config(text=key)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.text_box.get("1.0", tk.END).strip())
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    keyboard = OnScreenKeyboard(root)
    root.mainloop()
