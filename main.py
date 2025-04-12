from tkinter import Tk
from ui_setup import setup_ui

def main():
    root = Tk()
    root.title("Simple Text Editor")
    root.geometry("1000x600")
    root.resizable(True, True)

    # Setup UI components
    my_text, status_bar, toolbar_frame, open_status = setup_ui(root)

    root.mainloop()

if __name__ == "__main__":
    main()