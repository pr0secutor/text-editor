from tkinter import filedialog
from tkinter import END

def new_file(my_text, status_bar, root):
    my_text.delete("1.0", END)
    root.title("Untitled")
    status_bar.config(text="New File        ")

def open_file(my_text, status_bar, root, open_status):
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfilename(
        initialdir="E:/",
        title="Open File",
        filetypes=(
            ("Text Files", "*.txt"),
            ("HTML Files", "*.html"),
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        )
    )
    if text_file:
        open_status["name"] = text_file
        name = text_file.replace("E:/", "")
        status_bar.config(text=f'{text_file}        ')
        root.title(f'{name}')
        with open(text_file, 'r') as file:
            stuff = file.read()
            my_text.insert(END, stuff)

def save_as_file(my_text, status_bar, root):
    text_file = filedialog.asksaveasfilename(
        defaultextension=".*",
        initialdir="E:/",
        title="Save File",
        filetypes=(
            ("Text Files", "*.txt"),
            ("HTML Files", "*.html"),
            ("Python Files", "*.py"),
            ("All Files", "*.*")
        )
    )
    if text_file:
        with open(text_file, 'w') as f:
            f.write(my_text.get(1.0, END))
        status_bar.config(text=f'Saved: {text_file}        ')
        root.title(text_file.replace("E:/", ""))
        return text_file
    return None

def save_file(my_text, status_bar, save_as_file_fn, root, open_status_name):
    if open_status_name:
        with open(open_status_name, 'w') as text_file:
            text_file.write(my_text.get(1.0, END))
        status_bar.config(text=f'Saved: {open_status_name}        ')
        return open_status_name
    else:
        return save_as_file_fn(my_text, status_bar, root)