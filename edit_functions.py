def cut_text(keyboard, my_text, root):
    selected = ""
    if keyboard:
        try:
            selected = root.clipboard_get()
        except:
            pass
    else:
        if my_text.tag_ranges("sel"):
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)
    return selected

def copy_text(keyboard, my_text, root):
    selected = ""
    if keyboard:
        try:
            selected = root.clipboard_get()
        except:
            pass
    else:
        if my_text.tag_ranges("sel"):
            selected = my_text.selection_get()
            root.clipboard_clear()
            root.clipboard_append(selected)
    return selected

def paste_text(keyboard, my_text, root, selected):
    if keyboard or selected is None:
        try:
            selected = root.clipboard_get()
        except:
            selected = ""
    if selected:
        position = my_text.index("insert")
        my_text.insert(position, selected)

def select_all(keyboard, my_text):
    my_text.tag_add('sel', '1.0', 'end')