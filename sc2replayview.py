import tkinter as tk
import os
from datetime import datetime as dt
import pkg_resources

from PIL import Image, ImageDraw, ImageTk
import sc2reader

CACHE_FILE = "_sc2replayviewcache"

cache = {}

img = Image.open(pkg_resources.resource_filename(__name__, "rplayicon.ico"))

# Create the main window
window = tk.Tk()
window.title("SC2ReplayView")
icon = ImageTk.PhotoImage(img)
window.iconphoto(True, icon)

# Set the size of the window
window.geometry('1024x768')
dirname = ""
scrollbar = details = items = dir_entry = dir_label = None


def main():
    global dir_label, dir_entry, items, details, scrollbar
    # Create the directory selection widget
    dir_label = tk.Label(window, text='Directory:')
    dir_label.pack(side='top', fill='x')
    dir_entry = tk.Entry(window)
    dir_entry.pack(side='top', fill='x')
    dir_button = tk.Button(window, text='Open', command=select_dir)
    dir_button.pack(side='top', fill='x')

    # Create the listbox to hold the items
    items = tk.Listbox(window, selectmode='single', font=("Helvetica", 16), width=50, activestyle='none')
    items.pack(side='left', fill='both', expand=True)
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    items.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=items.yview)

    details = tk.Text(window, fg="#000000", bg="#ffffff", padx=10, pady=5, font=("Helvetica", 16))
    details.pack(side='right', fill='both', expand=True)
    details.tag_config("green", foreground="#006400")
    # Bind the show_details function to the <<ListboxSelect>> event
    items.bind('<<ListboxSelect>>', show_details)

    # Bind the move_selection function to the <Up> and <Down> keys
    window.bind('<Up>', move_selection)
    window.bind('<Down>', move_selection)

    try:
        with open(os.path.expanduser(os.path.join("~", CACHE_FILE))) as fp:
            value = fp.read().strip()
            if value:
                refresh_list_box(value)
                dir_entry.delete(0, "end")
                dir_entry.insert(0, value)
    except FileNotFoundError:
        pass

    # Run the main loop
    window.mainloop()


# Define a function to select a directory
def select_dir():
    refresh_list_box(dir_entry.get())


def refresh_list_box(name):
    global dirname
    dirname = name
    if dirname:
        # Clear the listbox
        items.delete(0, 'end')
        # Add the file names in the directory to the listbox
        filenames = os.listdir(dirname)
        # Sort the file names by their creation time
        filenames = sorted(filenames, key=lambda x: os.stat(os.path.join(dirname, x)).st_mtime, reverse=True)
        # Add the sorted file names to the listbox
        for filename in filenames:
            items.insert('end', f"{filename} {dt.fromtimestamp(os.stat(os.path.join(dirname, filename)).st_mtime).strftime('%Y-%m-%d')}")
        if filenames:
            items.selection_set(0)
            show_details(None)

        with open(os.path.expanduser(os.path.join("~", CACHE_FILE)), "w") as fp:
            fp.write(dirname)


def insert_player(tktext, replay, player_id):
    s = replay.player[player_id].name
    if replay.player[player_id].pick_race != replay.player[player_id].play_race:
        s += f" ({replay.player[player_id].pick_race}/{replay.player[player_id].play_race})"
    else:
        s += f" ({replay.player[player_id].pick_race})"
    s += "\n"
    tktext.insert(tk.END, s)
    if replay.winner.number == player_id:
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
        item = items.get(index).rsplit(maxsplit=1)[0]
        path = os.path.join(dirname, item)
        replay = cache.get(path)
        if replay is None:
            replay = sc2reader.load_replay(os.path.join(dirname, item), load_level=2)
            cache[path] = replay
        if replay.winner is None:
            details.insert(tk.END, "<unsupported>\n\nThis is likely an archon match")
        elif len(replay.players) > 2:
            details.insert(tk.END, "<unsupported>\n\nMore than 2 players")
        else:
            # Update the details label with the text of the selected item
            insert_player(details, replay, 1)
            insert_player(details, replay, 2)
            details.insert(tk.END, f"Map: {replay.map_name}\n")
            details.insert(tk.END, f"Length: {replay.length}\n")
            details.insert(tk.END, f"Date: {replay.date}\n")
            if replay.messages:
                details.insert(tk.END, "Chat:\n")
                for msg in replay.messages:
                    details.insert(tk.END, f"<{msg.player.name}> {msg.text}\n")


# Define a function to move the selection up and down
def move_selection(event):
    # Get the currently selected item
    index = items.curselection()
    # If the list is not empty and there is a selected item
    if items.size() > 0 and index:
        # Move the selection up or down
        if event.keysym == 'Up':
            if index[0] > 0:
                items.selection_clear(index)
                items.selection_set(index[0] - 1)
        elif event.keysym == 'Down':
            # items.selection_clear(index)
            if index[0] < items.size() - 1:
                items.selection_clear(index)
                items.selection_set(index[0] + 1)
        # Update the details label
        show_details(event)


if __name__ == "__main__":
    main()