# 📝 Tkinter Text Editor

A lightweight and modular text editor built using Python's `tkinter` library. The editor supports basic file operations such as creating new files, opening existing files, saving, and saving as new files. The app has been organized into reusable and importable components for better structure and maintainability.

---

## 📁 Project Structure

```
text-editor-python/
│
├── main.py                  # Entry point of the application
├── file_operations.py       # Handles file-related operations (open, save, save as)
├── edit_operations.py       # (Optional) For undo, redo, cut, copy, paste etc.
├── toolbar_operations.py    # (Optional) Toolbar-related logic
├── format_operations.py     # (Optional) Text formatting (bold, italic, etc.)
├── app_init.py              # Sets up and initializes the main application UI
└── README.md                # You're reading it 😉
```

---

## 🔧 Features

- **New File:** Clear the editor and start fresh.
- **Open File:** Load `.txt`, `.py`, `.html`, and other files.
- **Save File:** Save changes to the currently open file.
- **Save As:** Save the file under a new name or location.
- **Keyboard Shortcuts:**
  - `Ctrl + N` – New File
  - `Ctrl + O` – Open File
  - `Ctrl + S` – Save File

---

## 🏃 Getting Started

### Prerequisites

- Python 3.x installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/text-editor-python.git
   cd text-editor-python
   ```
2. Install the packages
   ```bash
   pip install -r requirements.txt 
   ```

3. Run the app:
   ```bash
   python main.py
   ```

---

## 🧠 Code Highlights

- Modularized file operations like `new_file`, `open_file`, `save_file`, and `save_as_file`.
- Uses a dictionary (`open_status`) to manage the current file's state.
- Makes use of `tkinter.filedialog` for file navigation and `lambda` functions for command bindings.
