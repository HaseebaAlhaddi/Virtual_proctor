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
import create_account as ca

window=Tk()
window.resizable(False,False)
window.geometry('985x620+150+0')
window.state('zoomed')
window.title("المراقب الافتراضي")
window.configure(bg="#6ca8a3")

def view_window():
    #ca.view_window_create_account()
    print(";;;;")

video = cv2.VideoCapture(0)


def show_frame_log_in():
    success, frame = video.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (300, 300))
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.image = photo
    canvas.after(10, show_frame_log_in)
       

def Stop_camera_log_in():
    success, frame = video.read()
    frame = cv2.flip(frame, 1)
    user_name=coode.get()
    cv2.imwrite(user_name+"1.jpg", frame)
    video.release()
   
def log_in():
    global user,coode
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    user_name=coode.get()
    password=user.get()
    if user_name=='' or password=='':
         easygui.msgbox("تأكد من ادخال جميع البيانات",title="تنبيه")
    else:
         if client_socket:
              procrss_type="log_in"
              client_socket.sendall(procrss_type.encode())
              data = f"{user_name},{password}"
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاج")
              image=cv2.imread(user_name+"1.jpg")
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



def open_new_window():
    root=Toplevel(window)
    root.title("تغير كلمــة المــرور")
    root.geometry('400x490+0+110')
    root.configure(bg="#6ca8a3")
    root.resizable(False,False)
    root.iconbitmap("C:/Users/SAJA/Desktop/program_final/images/m_icon.ico")
    Label(root,width=20,text='تغيير كلمــة المــرور',font=('Micrsoft YaHei UI Light ',20,'bold'),fg='black',bg='#6ca8a3',border=0).place(x=40,y=9)
    Label(root,width=30,text='يرجى إدخال أسم المستخـدم مع كلمة المرورجديد',font=('Micrsoft YaHei UI Light ',15,'bold'),fg='white',bg='#6ca8a3',border=0).place(x=35,y=65)
    user1=Entry(root,width=20,fg='black',border=0,bg='white',font=('Micrsoft YaHei UI Light ',20,'bold'))
    user1.place(x=40,y=130)
    coode1=Entry(root,width=20,fg='#ff686b',border=0,bg="white",font=('Micrsoft YaHei UI Light ',20,'bold'))
    coode1.place(x=40,y=190)
    Button(root,text="التـــالــي",font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='tan2',width=30,cursor='hand2',activebackground='#ee1111').place(x=40,y=260)
#=======================================================#

window.iconbitmap("C:/Users/SAJA/Desktop/program_final/images/m_icon.ico")
logo_image = Image.open("C:/Users/SAJA/Desktop/program_final/images/m.jpg")
logo_image2 = ImageTk.PhotoImage(logo_image) 
lab=Label(window,image=logo_image2,bg='#6ca8a3')
lab.place(x=100,y=7)
btn=Button(window,width=10,text='تسجيــل الـدخــول',font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=793,y=248)
btn_up=Button(window,width=10,text='انشاء حسـاب جديد',command=view_window,font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='white',bg="#098d72",border=0)
btn_up.place(x=650,y=248)
def on_enter(e):
    user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'كـلمــــة المــــرور')
user=Entry(window,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',16,'bold'))
user.place(x=680,y=365)
user.insert(0,'كـلمــــة المــــرور')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave) 
def on_enter(e):
    coode.delete(0,'end')
def on_leave(e):
    name=coode.get()
    if name=='':
        coode.insert(0,'إســم الـمستخـدم') 
        
coode=Entry(window,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',16,'bold'))
coode.place(x=681,y=319)
coode.insert(0,'إســم الـمستخـدم')
coode.bind('<FocusIn>',on_enter)
coode.bind('<FocusOut>',on_leave)

Button(window,text="افتـح الكاميـرا ",width=9,font=('Arial',12,'bold'),command=show_frame_log_in,activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=757,y=470)
canvas = Canvas(window, width=300, height=300, bg='snow2')
canvas.place(x=334, y=331) 
btn=Button(window,width=15,command=open_new_window,text='لا اتذكر كلمـة المرور',font=('Arial',14,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=735,y=413)
Button(window,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),command=Stop_camera_log_in,activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=760,y=524)
Button(window,text=" تسجــل الـدخــول ",width=16,font=('Arial',11,'bold'),command=log_in,activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea').place(x=735,y=585)
window.mainloop()
