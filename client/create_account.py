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

video = cv2.VideoCapture(0)

stop_camera=False
def show_frame():
    success, frame = video.read()
    if stop_camera==False:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (300, 300))
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=NW, image=photo)
        canvas.image = photo
        canvas.after(10, show_frame)
       

def Stop_camera():
    global stop_camera
    stop_camera=True
    success, frame = video.read()
    frame = cv2.flip(frame, 1)
    user_name=coode.get()
    cv2.imwrite(user_name+".jpg", frame)
    video.release()

def create_account():
    global user,coode,email
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    user_name=coode.get()
    password=user.get()
    user_email=email.get()
    print(user_name)
    print(password)
    print(user_email)
    image=cv2.imread(user_name+".jpg")
    if user_name=='' or password=='' or user_email=='':
         easygui.msgbox("تأكد من ادخال جميع البيانات",title="تنبيه")
    else:
         if client_socket:
              procrss_type="create_account"
              client_socket.sendall(procrss_type.encode())
              data = f"{user_name},{password},{user_email}"
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاج")
              #.....
              frame = imutils.resize(image,width=380)
              a = pickle.dumps(frame)
              message = struct.pack("Q",len(a))+a
              client_socket.sendall(message)
              print("تم ارسال الصورة بنجاح")
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
              else:
                   print("فشل")
          
         client_socket.close()

window1=Tk()
window1.title("نشــاء حساب جديد")
window1.geometry('985x900+150+0')
window1.state('zoomed')
window1.configure(bg="#6ca8a3")
window1.iconbitmap("images/m_icon.ico")
logo_image2=ImageTk.PhotoImage(Image.open("images/m2.jpg"))  
Label(window1,image=logo_image2,bg='#6ca8a3').place(x=100,y=0)
btn_up=Button(window1,width=10,text='انشاء حسـاب جديد',font=('Open Sans ',18,'bold'),fg='white',cursor='hand2',activebackground='#098d72',activeforeground='white',bg="#12b28e",border=0)
btn_up.place(x=630,y=241)
btn=Button(window1,width=10,text='تسجيــل الـدخــول',font=('Open Sans ',18,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#098d72",border=0)
btn.place(x=783,y=240)
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'كـلمــــة المــــرور')
user=Entry(window1,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',17,'bold'))
user.place(x=687,y=355)
user.insert(0,'كـلمــــة المــــرور')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave) 
    #---------------------------------------------
def on_enter(e):
    coode.delete(0,'end')
def on_leave(e):
    name=coode.get()
    if name=='':
        coode.insert(0,'إســم الـمستخـدم')         
coode=Entry(window1,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',17,'bold'))
coode.place(x=687,y=309)
coode.insert(0,'إســم الـمستخـدم')
coode.bind('<FocusIn>',on_enter)
coode.bind('<FocusOut>',on_leave)
    #---------------------------------------------
def on_enter(e):
    email.delete(0,'end')
def on_leave(e):
    name=email.get()
    if name=='':
        email.insert(0,'البــريد الإلكتــروني')         
email=Entry(window1,width=14,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',17,'bold'))
email.place(x=687,y=410)
email.insert(0,'البــريد الإلكتــروني')
email.bind('<FocusIn>',on_enter)
email.bind('<FocusOut>',on_leave)
    #---------------------------------------
Button(window1,text="افتح الكـاميـرا",width=10,font=('yu gothic ui',12,'bold'),activeforeground='black',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f',command=show_frame).place(x=762,y=462)
canvas = Canvas(window1, width=300, height=300, bg='snow2')
canvas.place(x=334, y=331)
Button(window1,text=" جـديـد حســاب أنشــاء ",width=16,font=('yu gothic ui',11,'bold'),activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea',command=create_account).place(x=735,y=578)
Button(window1,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f',command=Stop_camera).place(x=760,y=510)
window1.mainloop()