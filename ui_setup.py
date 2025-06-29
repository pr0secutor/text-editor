from tkinter import Frame, Scrollbar, Text, Label, Menu, BooleanVar
from file_operations import new_file, open_file, save_file, save_as_file
from edit_functions import cut_text, copy_text, paste_text, select_all
from format_functions import bg_color, all_text_color, find_text, wrap
from toolbar import setup_toolbar, TextEditor

def setup_ui(root):
    # Initialize global status for file operations
    open_status = {"name": None}

    # Create word_wrap BooleanVar
    word_wrap = BooleanVar()

    # Create toolbar frame
    toolbar_frame = Frame(root)
    toolbar_frame.pack(fill="x", pady=5)

    # Create main frame
    my_frame = Frame(root)
    my_frame.pack(pady=5)

    # Create scrollbars
    text_scroll = Scrollbar(my_frame)
    text_scroll.pack(side="right", fill="y")
    hor_scroll = Scrollbar(my_frame, orient="horizontal")
    hor_scroll.pack(side="bottom", fill="x")

    # Create text box
    my_text = Text(
        my_frame,
        width=80,
        height=20,
        font=("Helvetica", 16),
        selectbackground="lightgrey",
        selectforeground="black",
        undo=True,
        yscrollcommand=text_scroll.set,
        xscrollcommand=hor_scroll.set,
        wrap="none"
    )
    my_text.pack()

    # Configure scrollbars
    text_scroll.config(command=my_text.yview)
    hor_scroll.config(command=my_text.xview)

    # Create status bar
    status_bar = Label(root, text="Ready        ", anchor="e")
    status_bar.pack(fill="x", side="bottom", ipady=15)

    # Create menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # File menu
    file_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(
        label="New",
        command=lambda: new_file(my_text, status_bar, root),
        accelerator="(Ctrl+N)"
    )
    file_menu.add_command(
        label="Open",
        command=lambda: open_file(my_text, status_bar, root, open_status),
        accelerator="(Ctrl+O)"
    )
    file_menu.add_command(
        label="Save",
        command=lambda: open_status.update({
            "name": save_file(my_text, status_bar, save_as_file, root, open_status["name"])
        }),
        accelerator="(Ctrl+S)"
    )
    file_menu.add_command(
        label="Save As",
        command=lambda: open_status.update({
            "name": save_as_file(my_text, status_bar, root)
        })
    )
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Edit menu
    edit_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=lambda: cut_text(False, my_text, root), accelerator="(Ctrl+x)")
    edit_menu.add_command(label="Copy", command=lambda: copy_text(False, my_text, root), accelerator="(Ctrl+c)")
    edit_menu.add_command(label="Paste", command=lambda: paste_text(False, my_text, root, None), accelerator="(Ctrl+v)")
    edit_menu.add_separator()
    edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+z)")
    edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+y)")
    edit_menu.add_separator()
    edit_menu.add_command(label="Select All", command=lambda: select_all(True, my_text), accelerator="(Ctrl+a)")

    # Format menu
    format_menu = Menu(my_menu, tearoff=False)
    my_menu.add_cascade(label="Format", menu=format_menu)
    format_menu.add_command(label="All Text Color", command=lambda: all_text_color(my_text))
    format_menu.add_command(label="Background Color", command=lambda: bg_color(my_text))
    format_menu.add_command(label="Search", command=lambda: find_text(None, my_text), accelerator="(Ctrl+f)")
    format_menu.add_separator()
    format_menu.add_checkbutton(
        label="Word Wrap",
        onvalue=True,
        offvalue=False,
        variable=word_wrap,
        command=lambda: wrap(my_text, word_wrap)
    )

    # Setup TextEditor for undo/redo history
    editor = TextEditor(my_text)

    # Setup toolbar (pass editor)
    setup_toolbar(toolbar_frame, my_text, status_bar, editor)

    # Bindings
    root.bind('<Control-Key-n>', lambda e: new_file(my_text, status_bar, root))
    root.bind('<Control-Key-o>', lambda e: open_file(my_text, status_bar, root, open_status))
    root.bind('<Control-Key-s>', lambda e: save_file(my_text, status_bar, save_as_file, root, open_status["name"]))
    root.bind('<Control-Key-x>', lambda e: cut_text(True, my_text, root))
    root.bind('<Control-Key-c>', lambda e: copy_text(True, my_text, root))
    root.bind('<Control-Key-v>', lambda e: paste_text(True, my_text, root, None))
    root.bind('<Control-Key-f>', lambda e: find_text(True, my_text))
    root.bind('<Control-a>', lambda e: select_all(True, my_text))
    root.bind('<Control-A>', lambda e: select_all(True, my_text))

    return my_text, status_bar, toolbar_frame, open_status