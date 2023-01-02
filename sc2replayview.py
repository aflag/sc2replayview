import tkinter as tk
import os
import sc2reader

cache = {}

# Create the main window
window = tk.Tk()
window.title("Item List")

# Set the size of the window
window.geometry('1024x768')
dirname = ""

# Define a function to select a directory
def select_dir():
    global dirname
    # Get the directory from the entry widget
    dirname = dir_entry.get()
    # If the directory is not empty
    if dirname:
        # Clear the listbox
        items.delete(0, 'end')
        # Add the file names in the directory to the listbox
        filenames = os.listdir(dirname)
        # Sort the file names by their creation time
        filenames = sorted(filenames, key=lambda x: os.stat(os.path.join(dirname, x)).st_mtime, reverse=True)
        # Add the sorted file names to the listbox
        for filename in filenames:
            items.insert('end', filename)

# Create the directory selection widget
dir_label = tk.Label(window, text='Directory:')
dir_label.pack(side='top', fill='x')
dir_entry = tk.Entry(window)
dir_entry.pack(side='top', fill='x')
dir_button = tk.Button(window, text='Select', command=select_dir)
dir_button.pack(side='top', fill='x')

# Create the listbox to hold the items
items = tk.Listbox(window, selectmode='single', font=("Helvetica", 16), width=50)
items.pack(side='left', fill='both', expand=True)

# Create a label to display the details of the selected item
# details = tk.Label(window, text='')
# details.pack(side='right', fill='both', expand=True)

details = tk.Text(window, fg="#000000", bg="#ffffff", padx=10, pady=5, font=("Helvetica", 16))
details.pack(side='right', fill='both', expand=True)
details.tag_config("green", foreground="#006400")

def insert_player(tktext, replay, player_id):
    s = replay.player[player_id].name
    if replay.player[player_id].pick_race != replay.player[player_id].play_race:
        s += f" ({replay.player[player_id].pick_race}/{replay.player[player_id].play_race})"
    else:
        s += f" ({replay.player[player_id].pick_race})"
    s += "\n"
    tktext.insert(tk.END, s)
    if replay.winner and replay.winner.number == player_id:
        # Get the index of the last character in the widget
        last_index = tktext.index("end-1c")
        # Add a tag to the last line of the widget
        tktext.tag_add("green", "end-2l", last_index)

# Define a function to update the details label when an item is selected
def show_details(event):
    try:
        index = items.curselection()[0]
    except IndexError:
        pass
    else:
        # Get the index of the selected item
        details.delete("1.0", "end")
        # Get the text of the selected item
        item = items.get(index)
        path = os.path.join(dirname, item)
        replay = cache.get(path)
        if replay is None:
            replay = sc2reader.load_replay(os.path.join(dirname, item), load_level=2)
            cache[path] = replay
        # Update the details label with the text of the selected item
        insert_player(details, replay, 1)
        insert_player(details, replay, 2)
        details.insert(tk.END, f"Length: {replay.length}\n")
        details.insert(tk.END, f"Date: {replay.date}\n")

# Bind the show_details function to the <<ListboxSelect>> event
items.bind('<<ListboxSelect>>', show_details)

# Define a function to move the selection up and down
def move_selection(event):
    # Get the currently selected item
    index = items.curselection()
    # If the list is not empty and there is a selected item
    if items.size() > 0 and index:
        # Move the selection up or down
        if event.keysym == 'Up':
            items.selection_clear(index)
            if index[0] > 0:
                items.selection_set(index[0] - 1)
        elif event.keysym == 'Down':
            items.selection_clear(index)
            if index[0] < items.size() - 1:
                items.selection_set(index[0] + 1)
        # Update the details label
        show_details(event)

# Bind the move_selection function to the <Up> and <Down> keys
window.bind('<Up>', move_selection)
window.bind('<Down>', move_selection)

# Run the main loop
window.mainloop()
