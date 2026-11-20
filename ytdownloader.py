import tkinter
from tkinter import filedialog
import customtkinter
import yt_dlp
import threading
from pathlib import Path
import os
import sys


# default download path - the download folder
if sys.platform == 'win32':
    default_path = os.path.join(os.path.expanduser('~'), "Downloads")
elif sys.platform == 'linux':
    default_path = os.path.join(os.path.expanduser('~'), "downloads")


def Downloader(ytLink, path, is_video, ext):
    
    if not ytLink:
        finsih_label.configure(text="Please enter a valid URL", text_color="red")
        return
    

    finsih_label.configure(text="Fetching video info...", text_color="white")
    progressBar.set(0)
    pct.configure(text="0%")

    if video_switch.get():
        if ext == 'mp4':
            format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
        else:
            format = 'bestvideo+bestaudio/best'
    else:
        format = 'bestaudio/best'
            
    
    ydl_opts = {
        'format' : format,
        'outtmpl':f'{path}/%(title)s.{ext}',
        'progress_hooks': [on_progress],
        'js_runtimes': {'node': {}},
        'quiet':False,
        'verbose':True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(ytLink, download=False)
            video_title = info.get('title', 'Unkown Title')
            ui(title.configure, text=f"{video_title}", text_color="white")
            ui(finsih_label.configure, text="Downloading...", text_color="white")
            ydl.process_info(info)
        finsih_label.configure(text="Download Complete!", text_color="white")
    except Exception as e:
        finsih_label.configure(text='Download Failed', text_color="red")
        print(f"Error: {e}")


def startDownload():
    threading.Thread(
        target=Downloader,
        args=(link.get(), download_path.get(), video_switch.get(), ext.get()), 
        daemon=True
    ).start()


def ui(fn, *a, **kw):
    app.after(0, lambda: fn(*a, **kw))


def on_progress(d):
    if d['status'] == "downloading":
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded = d.get('downloaded_bytes', 0)

        if total > 0:
            percentage = downloaded / total
            ui(pct.configure, text=f"{int(percentage * 100)}%")
            ui(progressBar.set, percentage)

    elif d['status'] == 'finished':
        pct.configure(text="100%")
        progressBar.set(1.0)

    
    
def ask_path():
    path = filedialog.askdirectory()
    if path:
        download_path.set(path)
        path_label.configure(text=f"Path: {path}")
    return path


def extension_options():
    if video_switch.get():
        options = ['mp4','mkv','webm']
    else:
        options = ['mp3', 'webm']
    ui(ext.configure, values=options)
    ui(ext.set, options[0])
    return options


# System settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Icon
icon_path = os.path.join(os.getcwd(), "assets", "ytdownloader.ico")
if os.path.exists(icon_path):
    app.iconbitmap(icon_path)

# Adding UI elements
title = customtkinter.CTkLabel(app, text="Insert YouTube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40)
link.pack()

download_path = tkinter.StringVar()
download_path.set(default_path)

video_frame = customtkinter.CTkFrame(app, bg_color="transparent")
video_frame.pack(pady=10)

# audio or video choice
video_switch  = customtkinter.CTkSwitch(video_frame, command=extension_options, text='Download video', onvalue=True, offvalue=False, button_hover_color='orange', progress_color='orange')
video_switch.grid(row=0, column=1, padx=10, pady=20)


ext = customtkinter.CTkComboBox(video_frame, values=['mp3','webm'],
                                                button_hover_color="orange", 
                                               corner_radius=10, border_width=0, bg_color="transparent",
                                            #    button_color="blue",
                                               dropdown_hover_color="orange", dropdown_text_color="white")
ext.set('mp3')
ext.grid(row=0, column=2, padx=10, pady=10)


# path selection
path_label = customtkinter.CTkLabel(app, text="Path: not selected", text_color='white')
path_label.pack(pady=10)


# download status 
finsih_label = customtkinter.CTkLabel(app, text="", text_color="white")
finsih_label.pack()

# progress bar percentage
pct = customtkinter.CTkLabel(app, text="0%", text_color="white")
pct.pack()

progressBar = customtkinter.CTkProgressBar(app, width=200)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

my_frame = customtkinter.CTkFrame(app, bg_color='transparent')
my_frame.pack(pady=10)

# select folder button
path_button = customtkinter.CTkButton(my_frame, text='Select path', command=ask_path, text_color="white", hover_color='orange', corner_radius=5)
path_button.grid(row=0, column=1,padx=10, pady=10)


download_path.set(default_path)
path_label.configure(text=f"Path: {download_path.get()}")

# Download button
download_button = customtkinter.CTkButton(my_frame, text="Download", command=startDownload, bg_color="blue", text_color="white", hover_color='orange', corner_radius=5, border_color='black')
download_button.grid(row=0, column=0, padx=10, pady=10)

# Run the app
app.mainloop()
