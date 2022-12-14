import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()

frame_1 = tk.Frame()

title = tk.Label(
    text="YouTube Video Downloader",
    background="orange",
    width=100,
    height=5,
    master=frame_1)

description = tk.Label(
    text="Ingresa el link al video:",
    width=100,
    height=2,
    border=5)

button = tk.Button(
    text="Download!",
    width=20,height=3,
    foreground="white",
    background="#609CF8",
    activebackground="pink")

vid_link = tk.Entry(
    border=5,
    width=100)

frame_1.pack()
title.pack()
description.pack()
vid_link.pack()
button.pack()

window.mainloop()

#Retrieving text with .get()
#Deleting text with .delete()
#Inserting text with .insert()

#text_box.get("1.0", tk.END)
#'Hello\nWorld\n'