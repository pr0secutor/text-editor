from tkinter import Button, Text, Frame, Tk, Label
from tkinter import font
from tkinter import colorchooser
from PIL import Image, ImageTk
import re

class DoublyLinkedList:
    class Node:
        def __init__(self, word="", index=-1, action=""):
            self.word = word  # The word or token (e.g., space, punctuation)
            self.index = index  # Position in the word list
            self.action = action  # "insert" or "delete"
            self.next = None
            self.prev = None

    def __init__(self, max_history=100):
        self.head = None
        self.curr = None
        self.tail = None
        self.max_history = max_history
        self.size = 0

    def insert(self, word, index, action):
        new_node = self.Node(word, index, action)
        if self.curr is None:
            self.head = new_node
            self.curr = new_node
            self.tail = new_node
            self.size = 1
        else:
            new_node.prev = self.curr
            self.curr.next = new_node
            self.curr = new_node
            self.tail = new_node
            self.size += 1
            # Truncate forward history
            self.tail.next = None
            # Limit history size
            if self.size > self.max_history:
                self.head = self.head.next
                self.head.prev = None
                self.size -= 1

    def undo(self):
        if self.curr and self.curr.prev:
            self.curr = self.curr.prev
            return self.curr.word, self.curr.index, self.curr.action
        return None, -1, ""

    def redo(self):
        if self.curr and self.curr.next:
            self.curr = self.curr.next
            return self.curr.word, self.curr.index, self.curr.action
        return None, -1, ""

class TextEditor:
    def __init__(self, text_widget):
        self.text = text_widget
        self.history = DoublyLinkedList(max_history=100)
        self.words = []  # Current list of words/tokens
        self.last_content = ""
        # Bind text changes
        self.text.bind("<<Modified>>", self.on_text_change)
        self.text.bind("<KeyRelease>", self.on_key_release)
        # Initialize history with empty state
        self.history.insert("", -1, "init")
        self.pending_change = False  # Debounce flag

    def get_words(self, content):
        # Split on whitespace and punctuation, preserving them as tokens
        return [w for w in re.split(r'(\s+|[^\w\s])', content) if w]

    def on_key_release(self, event):
        # Trigger change detection on specific keys
        if event.keysym in ("space", "Return", "BackSpace", "Delete") or event.char in (".", ",", "!", "?", ";", ":"):
            self.pending_change = True
            self.on_text_change(event)

    def on_text_change(self, event):
        if not (self.text.edit_modified() or self.pending_change):
            return
        current_content = self.text.get("1.0", "end-1c")
        if current_content == self.last_content:
            self.text.edit_modified(False)
            self.pending_change = False
            return

        current_words = self.get_words(current_content)
        last_words = self.get_words(self.last_content)

        # Find the first difference
        i = 0
        while i < len(current_words) and i < len(last_words) and current_words[i] == last_words[i]:
            i += 1

        if i < len(current_words) and i < len(last_words):
            # Word changed at position i
            if len(current_words) > len(last_words):
                # Insertion
                self.history.insert(current_words[i], i, "insert")
            elif len(current_words) < len(last_words):
                # Deletion
                self.history.insert(last_words[i], i, "delete")
        elif len(current_words) > len(last_words) and current_words:
            # Word inserted at the end
            self.history.insert(current_words[-1], len(current_words)-1, "insert")
        elif len(current_words) < len(last_words) and last_words:
            # Word deleted from the end
            self.history.insert(last_words[-1], len(last_words)-1, "delete")

        self.words = current_words
        self.last_content = current_content
        self.text.edit_modified(False)
        self.pending_change = False

    def undo(self):
        word, index, action = self.history.undo()
        if word is not None:
            if action == "insert":
                # Remove the inserted word
                self.words.pop(index)
            elif action == "delete":
                # Reinsert the deleted word
                self.words.insert(index, word)
            # Rebuild text from words
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "".join(self.words))
            self.last_content = "".join(self.words)

    def redo(self):
        word, index, action = self.history.redo()
        if word is not None:
            if action == "insert":
                # Reinsert the word
                self.words.insert(index, word)
            elif action == "delete":
                # Remove the word again
                self.words.pop(index)
            # Rebuild text from words
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "".join(self.words))
            self.last_content = "".join(self.words)

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

def setup_toolbar(toolbar_frame, my_text, status_bar, editor):
    # Undo & Redo buttons
    undo_icon = ImageTk.PhotoImage(Image.open("icons/undo.png").resize((15, 15), Image.LANCZOS))
    undo_button = Button(toolbar_frame, borderwidth=0, image=undo_icon, command=editor.undo)
    undo_button.image = undo_icon  # Keep reference
    undo_button.grid(row=0, column=0, sticky="w", padx=8, pady=2)

    redo_icon = ImageTk.PhotoImage(Image.open("icons/redo.png").resize((15, 15), Image.LANCZOS))
    redo_button = Button(toolbar_frame, borderwidth=0, image=redo_icon, command=editor.redo)
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