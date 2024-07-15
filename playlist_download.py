import os
import tkinter as tk
from tkinter import filedialog, ttk
from pytube import Playlist, YouTube

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Playlist URL label and entry
        self.playlist_url_label = tk.Label(self, text="Playlist URL:")
        self.playlist_url_label.pack(side="top")
        self.playlist_url_entry = tk.Entry(self, width=50)
        self.playlist_url_entry.pack(side="top")

        # Destination folder label and button
        self.destination_folder_label = tk.Label(self, text="Destination Folder:")
        self.destination_folder_label.pack(side="top")
        self.destination_folder_button = tk.Button(self, text="Browse", command=self.browse_destination_folder)
        self.destination_folder_button.pack(side="top")
        self.destination_folder_path = tk.StringVar()
        self.destination_folder_path.set("")
        self.destination_folder_label_path = tk.Label(self, textvariable=self.destination_folder_path)
        self.destination_folder_label_path.pack(side="top")

        # Quality selection label and option menu
        self.quality_label = tk.Label(self, text="Quality:")
        self.quality_label.pack(side="top")
        self.quality_variable = tk.StringVar()
        self.quality_variable.set("360p")  # default quality
        self.quality_option_menu = tk.OptionMenu(self, self.quality_variable, "144p", "240p", "360p", "480p", "720p", "1080p")
        self.quality_option_menu.pack(side="top")

        # Download all button
        self.download_all_button = tk.Button(self, text="Download All", command=self.download_all_videos)
        self.download_all_button.pack(side="top")

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(side="top")

    def browse_destination_folder(self):
        folder_path = filedialog.askdirectory()
        self.destination_folder_path.set(folder_path)

    def download_all_videos(self):
        playlist_url = self.playlist_url_entry.get()
        destination_folder = self.destination_folder_path.get()
        quality = self.quality_variable.get()

        if not playlist_url or not destination_folder:
            print("Please enter both playlist URL and destination folder.")
            return

        playlist = Playlist(playlist_url)
        total_videos = len(playlist.videos)

        for i, video in enumerate(playlist.videos):
            yt = YouTube(video.watch_url)
            stream = yt.streams.filter(resolution=quality).first()
            stream.download(output_path=destination_folder)

            # Update progress bar
            progress = (i + 1) / total_videos * 100
            self.progress_bar["value"] = progress
            self.master.update_idletasks()

root = tk.Tk()
app = Application(master=root)
app.mainloop()