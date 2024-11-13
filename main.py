from pytubefix import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image,ImageTk
import threading
import random
import os

root = tk.Tk()
root.title("YT_CONVERTER")
root.resizable(width=False, height=False)
root.geometry("500x300")

#downloaded_file_path = None

def browse_dir():
    return filedialog.askdirectory(title="Where to save?")

def draw_widgets():
    sel_label.config(state=tk.NORMAL)
    dropdown.config(state=tk.NORMAL)
    url_label.config(state=tk.NORMAL)
    url_input.config(state=tk.NORMAL)
    button.config(state=tk.NORMAL)

def remove_widgets():
    sel_label.config(state=tk.DISABLED)
    dropdown.config(state=tk.DISABLED)
    url_label.config(state=tk.DISABLED)
    url_input.config(state=tk.DISABLED)
    button.config(state=tk.DISABLED)

def selected_choice():
    return selected_option.get()

def dl_progress(stream, chunks, bytes_remaining):
    total_size = stream.filesize
    bytes_dld = total_size - bytes_remaining
    dl_percentage = (bytes_dld / total_size) * 100
    progress_bar['value'] = dl_percentage

def dl_window(url, dir, func):
    global progress_bar, new_window, dl_label
    new_window = tk.Toplevel()
    new_window.title("Downloading")
    new_window.geometry("400x100")
    new_window.resizable(width=False, height=False)
    new_window.attributes("-toolwindow", True)

    def x_button():
        funny = ["WAIT!!!", "Slow download? Check your connection",
                 "PLDT sucks right?", "Peenoise are supposed to be patient!",
                 "Sorry can't close this", "Python sucks because\nof it's threading",
                 "I can't fix the partial file problem so here's\nfunny things instead!",
                 "Sick of my humor?\nJust trying to appeal to white kids","Oy magbayad ka ng net mo!",
                 "Lemme guess your using mobile data?\nSheesh I deserved an award!"]
        rand_funny = random.choice(funny)
        dl_label.config(text=rand_funny)

    new_window.protocol("WM_DELETE_WINDOW", x_button)

    new_window.focus()
    new_window.grab_set()
    new_window.transient()

    orig_dl_label = f"Downloading..."
    dl_label = tk.Label(new_window, text=orig_dl_label, font=("Courier", 10))
    dl_label.pack()

    progress_bar = ttk.Progressbar(new_window, length=200, orient="horizontal", mode="determinate")
    progress_bar.pack()

    thread = threading.Thread(target=func, args=(url, dir))
    thread.start()

def yt_to_mp3(url, dir):
    try:
        remove_widgets()
        yt = YouTube(url, on_progress_callback=dl_progress)
        stream = yt.streams.get_audio_only()
        stream.download(output_path=dir, mp3=True)
        after_dl()
    except:
        prob_occurred()
        return

def yt_converter(url, dir):
    try:
        remove_widgets()
        yt = YouTube(url, on_progress_callback=dl_progress)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=dir)
        after_dl()
    except:
        prob_occurred()
        return

def after_dl():
    new_window.destroy()
    messagebox.showinfo("", "Download Successful! :>")
    draw_widgets()
    url_input.delete(0, tk.END)

def prob_occurred():
   def update_label():
       new_window.destroy()
       messagebox.showinfo("", "Problem occurred! Check network connection!")
       draw_widgets()

   if new_window.winfo_exists():
       update_label()

def on_click():
    url = url_input.get()
    if url.find("watch") == -1:
        return
    chosen_dir = browse_dir()
    if not chosen_dir:
        return

    if selected_choice() == options[0]:
        dl_window(url, chosen_dir, yt_to_mp3)
    else:
        dl_window(url, chosen_dir, yt_converter)

icon = Image.open("youtube_ico.ico").resize((80, 80))
icon_tk = ImageTk.PhotoImage(icon)

icon_label = tk.Label(root, image=icon_tk)
icon_label.pack()

sel_label = tk.Label(root, text="Select a converter:", font=("Courier", 12))
sel_label.pack()

options = ["Yt to Mp3", "Yt vid downloader"]
selected_option = tk.StringVar()
selected_option.set(options[0])
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.config(font=("Courier", 12))
dropdown.pack(pady=10)

url_label = tk.Label(root, text="Enter URL below:", font=("Courier", 12))
url_label.pack()

url_input = tk.Entry(root, width=30 ,font=("Courier", 12))
url_input.pack(pady=10)

button = tk.Button(root, text="Download!", font=("Courier", 15), command=on_click)
button.pack(pady=10)

root.mainloop()