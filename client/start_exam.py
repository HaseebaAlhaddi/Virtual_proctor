from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
import cv2
import easygui
import socket,pickle,struct
import pyshine as ps # pip install pyshine
import imutils
import threading
import numpy as np
import struct

window2=Tk()
window2.title("رررررر")
window2.geometry('400x490+0+110')
window2.configure(bg='#97f8e4')
window2.geometry('985x620+150+0')
window2.state('zoomed')
window2.iconbitmap("images/m_icon.ico")
pic=ImageTk.PhotoImage(Image.open("images/m33.jpg"))
Label(window2,image=pic,bg='#97f8e4').place(x=100,y=0)
    
def on_enter(e):
    s_nam.delete(0,'end')
def on_leave(e):
    name=s_nam.get()
    if name=='':
        s_nam.insert(0,'أسم الطالب')
s_nam=Entry(window2,width=14,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
s_nam.place(x=200,y=28)
s_nam.insert(0,'أسم الطالب')
s_nam.bind('<FocusIn>',on_enter)
s_nam.bind('<FocusOut>',on_leave) 
    
tch_ip =Entry(window2,width=14,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
tch_ip.place(x=200,y=100)
#tch_ip.insert(0,'عنوان جهاز الاستاذ')
    
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'أسم المـادة')
user=Entry(window2,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
user.place(x=219,y=140)
user.insert(0,'أسم المـادة')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave) 
    #=======================================================
    #def show_entry():
       # seleccted_value=Combobox.get()
        #if seleccted_value=="مباشرة":
            #entry.place(x=0,y=0)
        #else:
            #entry.place()
    #entry=Entry(window2)
    #Comb.bind("<<ComboboxSelected>>",lambda event:show_entry())
    #============================================================
canvas=Canvas(window2,width=250,height=200,bg='white')
canvas.place(x=195,y=320)
Button(window2,text='صـورة التقط',width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=570)
window2.mainloop()