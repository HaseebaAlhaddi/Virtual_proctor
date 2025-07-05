from tkinter import *
from PIL import ImageTk,Image
import cv2
import easygui
import socket,pickle,struct
import pyshine as ps # pip install pyshine
import imutils
import threading
import numpy as np
import struct

window=Tk()
window.geometry('985x620+150+0')
window.state('zoomed')
window.title('المراقب الافتراضي')
window.resizable(False,False)
window.iconbitmap("images/m_icon.ico")
logo_image=ImageTk.PhotoImage(Image.open("images/m3 .jpg"))  
Label(window,image=logo_image,bg='white').place(x=0,y=0)
Button(window,text="الإختبــار بدا",width=10,font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=1128,y=28)
Button(window,text="السابق الإختبار عرض",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=900,y=29)
Button(window,text="الـحســـاب حـذف",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=680,y=28)
Button(window,text="المـرور كلمـة تغيير",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=450,y=28)

window.mainloop()