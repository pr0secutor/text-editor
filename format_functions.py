from tkinter import colorchooser, Toplevel, Label, Entry, Button
from tkinter import END

def bg_color(my_text):
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)

def all_text_color(my_text):
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)

def wrap(my_text, word_wrap):
    if word_wrap.get():
        my_text.config(wrap="word")
    else:
        my_text.config(wrap="none")

def kmp_preprocess(pattern):
    """Preprocess pattern to get the longest prefix-suffix (lps) array."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i].lower() == pattern[length].lower():
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """Yield all start indices of pattern in text using KMP algorithm."""
    lps = kmp_preprocess(pattern)
    i = j = 0
    while i < len(text):
        if text[i].lower() == pattern[j].lower():
            i += 1
            j += 1
        if j == len(pattern):
            yield i - j
            j = lps[j - 1]
        elif i < len(text) and text[i].lower() != pattern[j].lower():
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

def check(value, my_text):
    my_text.tag_remove('found', "1.0", "end")
    my_text.tag_config('found', foreground='red')
    list_of_words = value.split(' ')
    content = my_text.get("1.0", "end-1c")
    for word in list_of_words:
        if not word:
            continue
        word_len = len(word)
        for start in kmp_search(content, word):
            line = content.count('\n', 0, start) + 1
            if line == 1:
                col = start
            else:
                last_nl = content.rfind('\n', 0, start)
                col = start - last_nl - 1
            index_start = f"{line}.{col}"
            index_end = f"{line}.{col + word_len}"
            my_text.tag_add('found', index_start, index_end)

def cancel_search(search):
    # Remove highlight before closing
    # Find the parent text widget from the search window's children
    for widget in search.master.winfo_children():
        if hasattr(widget, 'tag_remove'):
            widget.tag_remove('found', "1.0", "end")
    search.destroy()
    return "break"

def find_text(e, my_text):
    search = Toplevel()
    search.title('Find Text')
    search.transient()
    search.resizable(False, False)
    Label(search, text='Find All:').grid(row=0, column=0, sticky='e')
    x = search.winfo_x()
    y = search.winfo_y()
    search.geometry("+%d+%d" % (x+500, y+300))
    entry_widget = Entry(search, width=25)
    entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    entry_widget.focus_set()
    Button(search, text='Search', underline=0,
           command=lambda: check(entry_widget.get(), my_text)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=5)
    Button(search, text='Cancel', underline=0,
           command=lambda: (my_text.tag_remove('found', "1.0", "end"), cancel_search(search))).grid(row=0, column=4, sticky='e'+'w', padx=2, pady=5)