import sys
from pytubefix import YouTube
from pytubefix import Stream
from pytubefix import Playlist
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askdirectory, askopenfilename
import urllib.request
import threading

import os
import customtkinter
import subprocess
import shutil
import requests
import zipfile

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

colors = {
    'white': '#ffffff',
    'black': '#000000',
    'grey': '#333',
    'hover_red': '#ea3d3d'
}
background = colors['grey']


class Converter(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.folder_path = None
        self.folder_destination_path = None
        self.file_path = None
        self.ffmpeg_path = None

        self.title("Evil YouTube - Conversor")
        self.geometry("300x400")
        self.resizable(False, False)

        self.frame_buttons = customtkinter.CTkFrame(
            self
        )
        self.frame_buttons.pack(side='top', expand=True, fill='both')

        self.open_folder_button = customtkinter.CTkButton(
            self.frame_buttons, text="Select path", width=100, command=self.define_path)  # set command parameter
        self.open_folder_button.pack(side='left', expand=True)

        self.open_file = customtkinter.CTkButton(
            self.frame_buttons, text="Select file", width=100, command=self.select_file)
        self.open_file.pack(side='left', expand=True)


        self.info_frame = customtkinter.CTkFrame(
            self
        )
        self.info_frame.pack(side='top', expand=True, fill='both')

    
        self.instructions = customtkinter.CTkLabel(self.info_frame, text="1.- Select a option, convert multiple files or one file\n 2.- Select folder or file\n 3.- Select folder destination")
        self.instructions.pack(side='top', expand=True)

        # INSTALL MANAGER

        self.install_manager_frame = customtkinter.CTkFrame(
            self
        )
        self.install_manager_frame.pack_forget()

        self.status_label = customtkinter.CTkLabel(
            self.install_manager_frame, text=""
        )

        self.status_label.pack_forget()

        self.progressbar = customtkinter.CTkProgressBar(
            self.install_manager_frame, orientation="horizontal", progress_color='red', corner_radius=10, mode='indeterminate')
        self.progressbar.pack_forget()
        self.progressbar.set(0)


        # FFMPEG

        self.status_ffmpeg = customtkinter.CTkLabel(
            self.info_frame, text=""
        )
        self.status_ffmpeg.pack_forget()

        self.progressbar_ffmpeg = customtkinter.CTkProgressBar(
            self.info_frame, orientation="horizontal", progress_color='red', corner_radius=10, mode='indeterminate'
        )

        self.progressbar.pack_forget()

    def define_path(self):
        self.folder_path = askdirectory(intialdir=None)
        if not self.folder_path:
            messagebox.showinfo('Evil YouYube - Conversor', "Operation canceled by user")
            return
        selection = messagebox.askokcancel(
            "Evil YouTube - Conversor", "You want convert all mp4 files to mp3 files for this folder?")
        if selection:
            self.convert_all_mp4_to_mp3()
        else:
            return

    def execute_ffmpeg(self, single_file=False):
        self.progressbar_ffmpeg.pack()
        self.progressbar_ffmpeg.start()
        self.status_ffmpeg.configure(text="Converting")
        self.status_ffmpeg.pack()
        if single_file:
            proc = subprocess.run(
                ['powershell.exe',
                '.\convertmp4tomp3.ps1',
                '-FfmpegPath',
                self.ffmpeg_path,
                '-File',
                f'\'{self.file_path}\'',
                '-DestinationFolderPath',
                f'\'{self.folder_destination_path}\'']
            )

            if proc.returncode != 0:
                messagebox.showerror('Error during conversion', 'Error code: 4 script error')
            else:
                messagebox.showinfo('Files converted successfully', f'files converted sucessfully on {self.folder_destination_path}')

            self.progressbar_ffmpeg.stop()
        else:
            try:
                proc = subprocess.run(
                    ['powershell.exe',
                    '.\convertmp4tomp3.ps1',
                    '-FfmpegPath', 
                    self.ffmpeg_path, 
                    '-FolderPath', 
                    f'\'{self.folder_path}\'', 
                    '-DestinationFolderPath', 
                    f'\'{self.folder_destination_path}\''])
                    
                if proc.returncode != 0:
                    messagebox.showerror('Error during conversion', 'Error code: 3, Script error')
                else:
                    messagebox.showinfo('Files converted successfully', f'Files converted successfully on {self.folder_destination_path}')
            except OSError as e:
                messagebox.showerror('Error during conversion', e)
            finally:
                self.progressbar_ffmpeg.stop()

    def select_file(self):
        self.file_path = askopenfilename()
        if not self.file_path:
            messagebox.showinfo('Evil YouTube - Conversor', "Operation canceled by user")
            return
        selection = messagebox.askokcancel("Evil YouTube - Conversor", f"You want convert {self.file_path} to mp3?")
        if selection:
            self.convert_file_mp4_to_mp3()
        else:
            return


    def convert_all_mp4_to_mp3(self):
        if self.folder_path is None:
            return

        self.folder_destination_path = askdirectory(initialdir=None)

        # Use ffmpeg
        # Check if ffmpeg exists on the system

        relative_ffmpeg_bin = 'ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

        if shutil.which(relative_ffmpeg_bin) is not None:
            self.ffmpeg_path = f'\'{os.path.abspath(relative_ffmpeg_bin)}\''

            # if shutil.which('ffmpeg.exe') is not None:
            #     self.ffmpeg_path = shutil.which('ffmpeg.exe')
            # Execute powershell script

            t5 = threading.Thread(target=self.execute_ffmpeg)
            t5.start()

        else:
            install_ffmpeg = messagebox.askokcancel(
                "Evil YouTube - Conversor", "Not ffmpeg exist in your system do you want install ffmpeg?")
            if install_ffmpeg:
                t4 = threading.Thread(target=self.install_ffmpeg)
                t4.start()
            else:
                return

    def install_ffmpeg(self):

        self.install_manager_frame.pack(side='top', fill="both", expand=True)
        self.progressbar.pack()
        self.status_label.pack()

        default_filename = "ffmpeg.zip"
        git = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

        response = requests.get(git, stream=True)

        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', None))
            chunk_size = 100000
            bytes_downloaded = 0
            if total_size is not None:
                self.progressbar.configure(mode='determinate')
            else:
                self.progressbar.start()

            self.status_label.configure(
                text="Downloading ffmpeg please wait...")
            with open(default_filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file.write(chunk)
                    if total_size is not None:
                        bytes_downloaded += chunk_size
                        percentage = (bytes_downloaded / total_size)
                        self.progressbar.set(percentage)

            # Once installed unzip ffmpeg on the same directory
            self.status_label.configure(
                text="Unziping ffmpeg on current directory")
            with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname('ffmpeg.zip'))

            messagebox.showinfo("ffmpeg installed",
                                "ffmpeg has been installed successfully")
            self.progressbar.stop()
        else:
            messagebox.showerror("Failed ffmpeg download",
                                 "ffmpeg can not be installed")
            self.progressbar.stop()

    def convert_file_mp4_to_mp3(self):
        if self.file_path is None:
            return

        self.folder_destination_path = askdirectory(initaldir=None)
        relative_ffmpeg_bin = 'ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe'

        if shutil.which(relative_ffmpeg_bin) is not None:
            self.ffmpeg_path = f'\'{os.path.abspath(relative_ffmpeg_bin)}\''
            t6 = threading.Thread(target=self.execute_ffmpeg, kwargs={'single_file': True})
            t6.start()
        else:
            install_ffmpeg = messagebox.askokcancel(
                "Evil YouTube - Conversor", "Not ffmpeg exist in your system do you want install ffmpeg?")
            if install_ffmpeg:
                t4 = threading.Thread(target=self.install_ffmpeg)
                t4.start()
            else:
                return
        



# ROOT
root = Tk()
root.title("Evil YouTube")
root.geometry("600x450")
root.resizable(False, False)
root.config(background=background)
root.iconbitmap("./youtube.ico")

label_link = customtkinter.CTkLabel(
    root, text="YouTube URL", font=("Tahoma", 12))
label_link.grid(row=1, column=0, pady=0, padx="50")

entry_link = customtkinter.CTkEntry(
    root, placeholder_text="Set url", width=200, corner_radius=10)
entry_link.grid(row=1, column=1, pady=0)

# progressbar
progressbar = customtkinter.CTkProgressBar(
    root, width=200, orientation="horizontal", mode="determinate", corner_radius=10, progress_color="red")
progressbar.grid(row=2, column=1)
progressbar.set(0)
# output_filepath

selectionplaylist = IntVar()
selectionplaylist.set(0)

radiobutton_1 = customtkinter.CTkRadioButton(
    root, text="Video", variable=selectionplaylist, value=0, hover_color=colors['hover_red'], fg_color='red')
radiobutton_1.grid(row=4, column=0, pady=5, padx=5)

radiobutton_2 = customtkinter.CTkRadioButton(
    root, text="Playlist", variable=selectionplaylist, value=1, hover_color=colors['hover_red'], fg_color='red')
radiobutton_2.grid(row=5, column=0, pady=5, padx=5)

selection = IntVar()
selection.set(1)

radiobutton_3 = customtkinter.CTkRadioButton(
    root, text="High Quality", variable=selection, value=1, hover_color=colors['hover_red'], fg_color='red')
radiobutton_3.grid(row=3, column=0, pady=5, padx=5)

radiobutton_4 = customtkinter.CTkRadioButton(
    root, text="Low Quality", variable=selection, value=2, hover_color=colors['hover_red'], fg_color='red')
radiobutton_4.grid(row=2, column=0, pady=5, padx=5)

frame2 = customtkinter.CTkFrame(root, fg_color="transparent", width=400)

label_thumbnail = customtkinter.CTkLabel(frame2, fg_color="transparent")
label_title = customtkinter.CTkLabel(frame2, wraplength=250)
label_author = customtkinter.CTkLabel(frame2)


def open_conversor():
    app = Converter()
    app.mainloop()


def update_progress(percentage):
    if percentage < 1:
        progressbar.set(percentage)
    else:
        progressbar.set(1)


def new_path():
    global filepath
    path = askdirectory(initialdir="./")
    filepath = path
    # statusbar["text"] = f"Route established in {filepath}"

# on complete function


def on_complete_function(stream, file_path):
    messagebox.showinfo("YouTube Downloader", "Download Completed")

# on progress function


def progress_function(s, chunk, bytes_remaining):
    percentage_complete = int(
        (s.filesize - bytes_remaining) / s.filesize * 100) * .01
    progressbar.set(percentage_complete)


def get_thumbnail(video_obj):
    global photo
    thumbnail = Image.open(urllib.request.urlopen(video_obj.thumbnail_url))
    photo = ImageTk.PhotoImage(thumbnail.resize((220, 120)))
    frame2.grid(row=6, column=1)
    label_thumbnail.configure(image=photo)
    label_thumbnail.grid(row=6, column=1)


def set_label(title, author):
    label_title.configure(text=str(title))
    label_title.grid(row=1, column=1)
    label_author.configure(text=str(author))
    label_author.grid(row=2, column=1, columnspan=3)


def get_video_object(url="", playlist=False):
    try:
        if not playlist:
            video = YouTube(url, on_progress_callback=progress_function)
            video.register_on_complete_callback(on_complete_function)
        else:
            video = YouTube(url)
    except:
        messagebox.showerror(
            "Find error", f"Url: {url} not is a valid youtube url, please set a valid url or check a new app update")
        return None
    get_thumbnail(video)
    title = video.title # WARNING 4/11/2024 THIS METHOD GET A EXCEPTION pytube.exceptions.PytubeError
    author = video.author
    set_label(title, author)
    filtracion = video.streams.filter(progressive=True,
                                      file_extension="mp4").order_by("resolution").desc()
    return filtracion


def download(filtracion, filepath=""):
    if filtracion == None:
        return
    if selection.get() == 1:
        video = filtracion.last()  # last // low quality
    if selection.get() == 2:
        video = filtracion.first()  # first // high quality
    try:
        video.download(output_path=filepath)
    except ConnectionError:
        messagebox.showerror("Network Error", "Internet connection lost")


def download_playlist():
    video_list = entry_link.get()
    playlist = Playlist(video_list)
    filepath = askdirectory(initialdir=None)
    quantityes = 0

    try:
        if filepath != "":
            for url in playlist.video_urls:

                video = get_video_object(url, playlist=True)
                download(video, filepath=filepath)
                quantityes += 1
                # Use percentage if use a different progressbar
                # total_percentage = ((quantityes / len(playlist.video_urls)) * 100)

                step = quantityes / len(playlist.video_urls)
                progressbar.set(step)
        else:
            messagebox.showerror("Error", "No path established")
    except:
        messagebox.showerror(
            "Playlist error", f"Playlist: {video_list} not is a valid YouTube playlist, please set a valid YouTube playlist or check a new app update")


def button_download_video():
    url = entry_link.get()
    filepath = askdirectory(initialdir=None)
    if filepath != "":
        video = get_video_object(url)
        download(video, filepath=filepath)
    else:
        messagebox.showerror("Error", "No path established")


def preview():
    url = entry_link.get()
    get_video_object(url)


def download_menu():
    if selectionplaylist.get() == 0:
        t2 = threading.Thread(target=button_download_video)
        t2.start()
    if selectionplaylist.get() == 1:
        t3 = threading.Thread(target=download_playlist)
        t3.start()


button_download = customtkinter.CTkButton(
    root, text="Download", command=download_menu, hover_color=colors['hover_red'], fg_color='red')
# boton_download = Button(root, text="Download",fg="red", bg="black", command=download_menu, font=("Segoe UI", 12), border=0)
button_download.grid(row=1, column=2, pady=20, padx=20)

button_preview = customtkinter.CTkButton(
    root, text="Preview", command=preview, hover_color=colors['hover_red'], fg_color='red')
button_preview.grid(row=2, column=2)

# boton_download = Button(root, text="Preview",fg="red", bg="black", command=preview, font=("Segoe UI", 12), border=0)
# boton_download.grid(row = 2, column = 2, pady= 20, padx=20)

# Window emergent


def error_downloading():
    messagebox.showerror("YouTube Downloader", "Downloading Error")


def close_app():
    message_close = messagebox.askokcancel(
        "YouTube Downloader", "Closing YouTube Downloader")
    if message_close == True:
        root.destroy()


def about_menu():
    message_about = messagebox.showinfo(
        "About", "Support on ChrisVergara7@outlook.com")


# barra menus
menu_bar = Menu(root)
root.config(menu=menu_bar, width=300, height=300)
# elements menu bar
FilesMenu = Menu(menu_bar, tearoff=0)
ToolsMenu = Menu(menu_bar, tearoff=0)
AboutMenu = Menu(menu_bar, tearoff=0)
# Add elements
menu_bar.add_cascade(label="Files", menu=FilesMenu)
menu_bar.add_cascade(label="Tools", menu=ToolsMenu)
menu_bar.add_cascade(label="About", menu=AboutMenu)
# add subelements Filemenu
FilesMenu.add_command(label="Path", command=new_path)
FilesMenu.add_separator()  # separator
FilesMenu.add_command(label="Close", command=close_app)
# add subelements Toolsmenu
# none
# add subelements Aboutmenu
AboutMenu.add_command(label="About", command=about_menu)
ToolsMenu.add_command(label="Mp4 to mp3 tool", command=open_conversor)
# Thumbnail label


if __name__ == "__main__":
    root.mainloop()
