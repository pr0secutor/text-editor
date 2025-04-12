from tkinter import Button
from tkinter import font
from PIL import Image, ImageTk
from tkinter import colorchooser

def bold(my_text):
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    my_text.tag_configure("bold", font=bold_font)
    current_tags = my_text.tag_names("sel.first")
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")

def italic(my_text):
    italic_font = font.Font(my_text, my_text.cget("font"))
    italic_font.configure(slant="italic")
    my_text.tag_configure("italic", font=italic_font)
    current_tags = my_text.tag_names("sel.first")
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

def text_color(my_text, status_bar):
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)
        color_font = font.Font(my_text, my_text.cget("font"))
        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        current_tags = my_text.tag_names("sel.first")
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last")

def underline(my_text):
    underline_font = font.Font(my_text, my_text.cget("font"))
    underline_font.configure(underline=True)
    my_text.tag_configure("underline", font=underline_font)
    current_tags = my_text.tag_names("sel.first")
    if "underline" in current_tags:
        my_text.tag_remove("underline", "sel.first", "sel.last")
    else:
        my_text.tag_add("underline", "sel.first", "sel.last")

def strike(my_text):
    strike_font = font.Font(my_text, my_text.cget("font"))
    strike_font.configure(overstrike=True)
    my_text.tag_configure("overstrike", font=strike_font)
    current_tags = my_text.tag_names("sel.first")
    if "overstrike" in current_tags:
        my_text.tag_remove("overstrike", "sel.first", "sel.last")
    else:
        my_text.tag_add("overstrike", "sel.first", "sel.last")

def remove_align_tags(my_text):
    current_tags = my_text.tag_names("sel.first")
    for tag in ["left", "right", "center"]:
        if tag in current_tags:
            my_text.tag_remove(tag, "sel.first", "sel.last")

def align_left(my_text):
    remove_align_tags(my_text)
    my_text.tag_configure("left", justify='left')
    my_text.tag_add("left", "sel.first", "sel.last")

def align_right(my_text):
    remove_align_tags(my_text)
    my_text.tag_configure("right", justify='right')
    my_text.tag_add("right", "sel.first", "sel.last")

def align_middle(my_text):
    remove_align_tags(my_text)
    my_text.tag_configure("center", justify='center')
    my_text.tag_add("center", "sel.first", "sel.last")

def align_justify(my_text):
    remove_align_tags(my_text)

def setup_toolbar(toolbar_frame, my_text, status_bar):
    # Undo & Redo buttons
    undo_icon = ImageTk.PhotoImage(Image.open("icons/undo.png").resize((15, 15), Image.LANCZOS))
    undo_button = Button(toolbar_frame, borderwidth=0, image=undo_icon, command=my_text.edit_undo)
    undo_button.image = undo_icon  # Keep reference
    undo_button.grid(row=0, column=0, sticky="w", padx=8, pady=2)

    redo_icon = ImageTk.PhotoImage(Image.open("icons/redo.png").resize((15, 15), Image.LANCZOS))
    redo_button = Button(toolbar_frame, borderwidth=0, image=redo_icon, command=my_text.edit_redo)
    redo_button.image = redo_icon
    redo_button.grid(row=0, column=1, sticky="w", padx=8, pady=2)

    # Bold button
    bold_icon = ImageTk.PhotoImage(Image.open("icons/bold.png").resize((15, 15), Image.LANCZOS))
    bold_button = Button(toolbar_frame, borderwidth=0, image=bold_icon, command=lambda: bold(my_text))
    bold_button.image = bold_icon
    bold_button.grid(row=0, column=3, sticky="w", padx=8, pady=2)

    # Italic button
    italic_icon = ImageTk.PhotoImage(Image.open("icons/italics.png").resize((15, 15), Image.LANCZOS))
    italic_button = Button(toolbar_frame, borderwidth=0, image=italic_icon, command=lambda: italic(my_text))
    italic_button.image = italic_icon
    italic_button.grid(row=0, column=4, sticky="w", padx=8, pady=2)

    # Underline button
    underline_icon = ImageTk.PhotoImage(Image.open("icons/underline.png").resize((15, 15), Image.LANCZOS))
    underline_button = Button(toolbar_frame, borderwidth=0, image=underline_icon, command=lambda: underline(my_text))
    underline_button.image = underline_icon
    underline_button.grid(row=0, column=5, sticky="w", padx=8, pady=2)

    # Overstrike button
    strike_icon = ImageTk.PhotoImage(Image.open("icons/strike.png").resize((15, 15), Image.LANCZOS))
    strike_button = Button(toolbar_frame, borderwidth=0, image=strike_icon, command=lambda: strike(my_text))
    strike_button.image = strike_icon
    strike_button.grid(row=0, column=6, sticky="w", padx=8, pady=2)

    # Text color button
    color_icon = ImageTk.PhotoImage(Image.open("icons/color.png").resize((18, 18), Image.LANCZOS))
    color_text_button = Button(toolbar_frame, borderwidth=0, image=color_icon, command=lambda: text_color(my_text, status_bar))
    color_text_button.image = color_icon
    color_text_button.grid(row=0, column=7, padx=8, pady=2)

    # Align left
    left_icon = ImageTk.PhotoImage(Image.open("icons/align_left.png").resize((18, 18), Image.LANCZOS))
    left_button = Button(toolbar_frame, borderwidth=0, image=left_icon, command=lambda: align_left(my_text))
    left_button.image = left_icon
    left_button.grid(row=0, column=8, padx=8, pady=2)

    # Align right
    right_icon = ImageTk.PhotoImage(Image.open("icons/align_right.png").resize((18, 18), Image.LANCZOS))
    right_button = Button(toolbar_frame, borderwidth=0, image=right_icon, command=lambda: align_right(my_text))
    right_button.image = right_icon
    right_button.grid(row=0, column=9, padx=8, pady=2)

    # Align center
    center_icon = ImageTk.PhotoImage(Image.open("icons/align_middle.png").resize((18, 18), Image.LANCZOS))
    center_button = Button(toolbar_frame, borderwidth=0, image=center_icon, command=lambda: align_middle(my_text))
    center_button.image = center_icon
    center_button.grid(row=0, column=10, padx=8, pady=2)

    # Align justify
    justify_icon = ImageTk.PhotoImage(Image.open("icons/align_justify.png").resize((18, 18), Image.LANCZOS))
    justify_button = Button(toolbar_frame, borderwidth=0, image=justify_icon, command=lambda: align_justify(my_text))
    justify_button.image = justify_icon
    justify_button.grid(row=0, column=11, padx=8, pady=2)