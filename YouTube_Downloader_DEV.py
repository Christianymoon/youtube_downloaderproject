import sys
from pytube import YouTube
from pytube import Stream
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter.filedialog import askdirectory

#ROOT
root = Tk()
root.title("Youtube downloader")
root.geometry("600x400")
root.resizable(False,False)
root.config(background= "black")

#secondary frame
frame_1 = Frame(root)
frame_1.pack(side="top", anchor="n")
frame_1.config(width="500", height="500",)
frame_1.config(background='#181818')
frame_1.pack(fill="both", expand=True)

#Labels and entrys
titulo = "YouTube Downloader"
label_title = Label(frame_1, text=titulo, font= "Consolas",
                    bg='#181818',fg="white")
label_title.place()
entry_link = Entry(frame_1)
entry_link.place()
label_link = Label(frame_1, text="Ingrese link de youtube",
                   font= "Consolas", fg="white", bg="#181818")
label_link.place()
#grid title
label_title.grid(row=0, column = 1, pady= "70", padx="10", sticky = "n")
#entry link
entry_link.grid(row = 2, column = 1, pady= "20")
label_link.grid(row = 2, column = 0, pady= "20", padx="70")
#youtube logo grid
image = PhotoImage(file="YT_Log_2.png")
label_image = Label(frame_1, image= image, bg="#181818")
label_image.grid(row = 0, column = 0, pady= "50", padx= "25")
#Statusbar

statusbar = Label(root, text= "YouTube Downloader by Christian VR", bg="black", fg= "green",
                  relief= SUNKEN, font= ("Consolas",9) )
statusbar.pack(side= "bottom", anchor= "w", fill= "x")

#progressbar
progressbar = ttk.Progressbar(frame_1, orient= HORIZONTAL, mode="determinate")
progressbar.place(x=80, y=280, width=150)
#output_filepath
def new_path():
    global filedialog

    filedialog = askdirectory(initialdir="C:/")
    statusbar["text"] = f"Route established in {filedialog}"

#on complete function
def on_complete_function(stream, file_path):
    messagebox.showinfo("YouTube Downloader", "Download Completed")
    print("Descarga completada")
    statusbar["text"]= f"Download completed in {filedialog}"
#on progress function
def progress_function(s, chunk, bytes_remaining):
    percentage_complete = int((s.filesize - bytes_remaining) / s.filesize * 100)
    progressbar.step(99.9)

def downloading():
        link = entry_link.get()
        video = YouTube(link, on_complete_callback=on_complete_function)
        statusbar["text"]= "on progress callback"
        video.register_on_progress_callback(progress_function)
        statusbar["text"] = "filter query results"
        titulo = video.title
        autor = video.author
        duracion = video.length
        print(          f"Autor del video -- {autor}")
        print(          f"duracion del video {duracion}" )
        filtracion = video.streams.filter(progressive=True,
        file_extension="mp4",).order_by("resolution").desc()
        first_video = filtracion.last()# first // high quality || last // low quality
        try:
            descarga = first_video.download(output_path=filedialog)
            print(filedialog)
        except:
            messagebox.showerror("YouTube Downloader", "Error: Specify download path or your internet conection")
            statusbar["text"] = "Download error: Specify download path or verify your internet conection"

boton_download = Button(frame_1, text="Descargar",fg="white", bg="#181818", command=downloading,
                        font= "Consolas")
boton_download.grid(row = 3, column = 1, pady= 50)
#Window emergent
def error_downloading():
    messagebox.showerror("YouTube Downloader", "Downloading Error")
def close_app():
    message_close = messagebox.askokcancel("YouTube Downloader", "Closing YouTube Downloader")
    if message_close == True:
        root.destroy()
def about_menu():
    message_about = messagebox.showinfo("About", "Support on ChrisVergara7@outlook.com")

#barra menus
menu_bar = Menu(root)
root.config(menu= menu_bar, width= 300, height= 300)
#elements menu bar
FilesMenu = Menu(menu_bar, tearoff= 0)
ToolsMenu = Menu(menu_bar)
AboutMenu = Menu(menu_bar, tearoff= 0)
#Add elements
menu_bar.add_cascade(label="Files", menu= FilesMenu)
menu_bar.add_cascade(label="Tools", menu= ToolsMenu)
menu_bar.add_cascade(label="About", menu= AboutMenu)
#add subelements Filemenu
FilesMenu.add_command(label= "Abrir")
FilesMenu.add_command(label= "Path", command= new_path)
FilesMenu.add_separator() #separator
FilesMenu.add_command(label= "Close", command= close_app)
#add subelements Toolsmenu
#none
#add subelements Aboutmenu
AboutMenu.add_command(label= "About", command= about_menu)
#Thumbnail label

root.mainloop()
