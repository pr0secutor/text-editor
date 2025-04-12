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

def check(value, my_text):
    my_text.tag_remove('found', "1.0", "end")
    my_text.tag_config('found', foreground='red')
    list_of_words = value.split(' ')
    for word in list_of_words:
        index = "1.0"
        while index:
            index = my_text.search(word, index, nocase=1, stopindex=END)
            if index:
                lastIndex = '%s+%dc' % (index, len(word))
                my_text.tag_add('found', index, lastIndex)
                index = lastIndex

def cancel_search(search):
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
           command=lambda: cancel_search(search)).grid(row=0, column=4, sticky='e'+'w', padx=2, pady=5)