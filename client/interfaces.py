from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import cv2
import easygui
import socket,pickle,struct
import pyshine as ps # pip install pyshine
import imutils
import threading
import numpy as np
import struct
import virtual_proctor as vp
import re
window=Tk()
window.resizable(False,False)
window.geometry('985x620+150+0')
window.state('zoomed')
window.title("المراقب الافتراضي")
window.configure(bg="#6ca8a3")
global new_password,last_password
video_log_in = cv2.VideoCapture(0)
#---------------------------------------------

def show_frame_log_in():
    success, frame = video_log_in.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (300, 300))
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas_log_in.create_image(0, 0, anchor=NW, image=photo)
    canvas_log_in.image = photo
    canvas_log_in.after(10, show_frame_log_in)
#---------------------------------------------------------------
def Stop_camera_log_in():
    success, frame = video_log_in.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (300, 300))
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas_log_in.create_image(0, 0, anchor=NW, image=photo)
    canvas_log_in.image = photo
    user_name=user_name_log_in.get()
    cv2.imwrite(user_name+"1"+".jpg", frame)
    video_log_in.release()
#----------------------------------------------------------
video_crate_account = cv2.VideoCapture(0)
def show_frame():
    
    success, frame = video_crate_account.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (300, 300))
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.image = photo
    canvas.after(10, show_frame)
#----------------------------------------------------------------
def Stop_camera():
    
    success, frame = video_crate_account.read()
    frame = cv2.flip(frame, 1)
    user_name_string=user_name.get()
    cv2.imwrite(user_name_string+".jpg", frame)
    video_crate_account.release()
#----------------------------------------------------------------------
def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # تعبير  للتحقق من الصيغة للبريد الالكتروني

    if re.match(pattern, email):
        return True
    else:
        return False
def create_account():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    user_name_string=user_name.get()
    password_string=password.get()
    user_email=email.get()
    print(user_name_string)
    print(password_string)
    print(user_email)
    image=cv2.imread(user_name_string+".jpg")
    if user_name_string=='' or user_name_string=='إســم الـمستخـدم' or password_string=='' or password_string=='كـلمــــة المــــرور' or user_email==''or user_email=='بريدك الالكتروني' :
         messagebox.showinfo("MessageBox","تأكد من ادخال جميع البيانات ")
    if not validate_email(user_email):
        messagebox.showinfo("MessageBox","صيغة البريد غير صحيحة ")
    else:
         if client_socket:
              procrss_type="create_account"
              client_socket.sendall(procrss_type.encode())
              data = f"{user_name_string},{password_string},{user_email}"
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاح")
              #.....
              frame = imutils.resize(image,width=500)
              a = pickle.dumps(frame)
              message = struct.pack("Q",len(a))+a
              client_socket.sendall(message)
              print("تم ارسال الصورة بنجاح")
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
                   messagebox.showinfo("MessageBox","تم انشاء حساب بنجاح ")
              else:
                   print("فشل")
          
    client_socket.close()

#---------------------------------------------------------------------
def log_in():
    global user_name_main,my_id
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    user_name_string=user_name_log_in.get()
    user_name_main=user_name_string
    password_staing=password_log_in.get()
    image=cv2.imread(user_name_string+"1"+".jpg")
    if user_name_string=='' or user_name_string=='إســم الـمستخـدم' or password_staing==''or password_staing=='كـلمــــة المــــرور':
         messagebox.showinfo("MessageBox","تأكد من ادخال جميع البيانات ")
    else:
         if client_socket:
              procrss_type="log_in"
              client_socket.sendall(procrss_type.encode())
              data = f"{user_name_string},{password_staing}"
              print(data)
              data_size=struct.pack('!I',len(data))
              print(data_size)
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاح")
              
              frame = imutils.resize(image,width=500)
              a = pickle.dumps(frame)
              message = struct.pack("Q",len(a))+a
              client_socket.sendall(message)
              print("تم ارسال الصورة بنجاح")
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
                   my_id=client_socket.recv(4*1024).decode('latin-1')
                   print(my_id)
                   messagebox.showinfo("MessageBox","تم تسجيل الدخول بنجاح ")
                   user_name_main=user_name_string
                   print(user_name_main)
                   view_main_interface_window()

              else:
                   print("فشل")
                   messagebox.showinfo("MessageBox","فشل في تسجيل الدخول ")
    client_socket.close() 
         
#----------------------------------------------------------------
def forget_password():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    f_user_name=user1.get()
    f_user_email=coode1.get()
    if f_user_name=='' or f_user_name=='اسم المستخدم' or f_user_email=='' or f_user_email=='بريدك الالكتروني':
        messagebox.showinfo("MessageBox","تأكد من ادخال جميع البيانات ")
    if not validate_email(f_user_email):
        messagebox.showinfo("MessageBox","صيغة البريد غير صحيحة ")
    else :
        if client_socket:
              procrss_type="forget_password"
              client_socket.sendall(procrss_type.encode())
              data=f"{f_user_name},{f_user_email}"
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاح")
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
                   messagebox.showinfo("MessageBox","تم ارسال كلمة المرور الخاصة بك الى بريدك الالكتروني ")

              else:
                   print("فشل")
                   messagebox.showinfo("MessageBox"," فشل : هناك خطاء تاكد من صحة البيانات ")
        
    client_socket.close()

#----------------------------------------------------------------
def change_password():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    new_password_string=new_password.get()
    last_password_string=last_password.get()
    print(user_name_main)
    if new_password_string=='' or last_password_string=='':
        messagebox.showinfo("MessageBox","تأكد من ادخال جميع البيانات ")
    else:
        if client_socket:
              procrss_type="change_password"
              client_socket.sendall(procrss_type.encode())
              data=f"{my_id},{new_password_string}"
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              print("تم ارسال البيانات بنجاح")
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
                   messagebox.showinfo("MessageBox","تم تغيير كلمة المرور بنجاح ")

              else:
                   print("فشل")
                   messagebox.showinfo("MessageBox","فشل في تغيير كلمة المرور ")
        
    client_socket.close()
   
    
#-------------------------------------------------------------
video_start_exam = cv2.VideoCapture(0)
def show_frame_start_exam():
    
    success, frame = video_start_exam .read()
    #print(success)
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (300, 300))
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas_start_exam.create_image(0, 0, anchor=NW, image=photo)
    canvas_start_exam.image = photo
    canvas_start_exam.after(10, show_frame_start_exam)
    video_start_exam .release()
#----------------------------------------------------------------
def Stop_camera_start_exam():
    
    success, frame = video_start_exam .read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite(user_name_main+"1"+".jpg", frame)
    video_start_exam .release()

def start_exam_button():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    #client_socket.connect((host_ip,port))
    subject_name_string=subject_name.get()
    image=cv2.imread(user_name_main+"1"+".jpg")
    if subject_name_string=="":
        messagebox.showinfo("MessageBox","تأكد من ادخال جميع البيانات ")
    else:
        if client_socket:
            procrss_type="start_exam"
            client_socket.sendall(procrss_type.encode())
            data = f"{my_id},{user_name_main},{subject_name_string}"
            print(data)
            data_size=struct.pack('!I',len(data))
            client_socket.send(data_size)
            client_socket.send(data.encode('latin-1'))
            print(data)
            print("تم ارسال البيانات بنجاح") 
      
            
            frame = imutils.resize(image,width=500)
            a = pickle.dumps(frame)
            message_image = struct.pack("Q",len(a))+a
            client_socket.sendall(message_image)
            print("تم ارسال الصورة بنجاح")
            message=client_socket.recv(4*1024).decode('latin-1')
            if message=="True":
                print("تم بنجاح")
                messagebox.showinfo("MessageBox","تم التحقق من الهوية بنجاح")
                client_socket.close()
                thread=threading.Thread(target=vp.start_exam) 
                thread.start()
            else:
                print("فشل")
                messagebox.showinfo("MessageBox","فشل في التحقق من الهوية ")
                client_socket.close()
    


#----------------------------------------------------------------
def delete_acount():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.0.28' 
    port = 9999
    client_socket.connect((host_ip,port))
    result=messagebox.askquestion("MessageBox","هل تريد حذف الحساب بالفعل")
    if result=='yes':
        
        if client_socket:
              procrss_type="delete_account"
              client_socket.sendall(procrss_type.encode())
              data=my_id
              print(data)
              data_size=struct.pack('!I',len(data))
              client_socket.send(data_size)
              client_socket.send(data.encode('latin-1'))
              message=client_socket.recv(4*1024).decode('latin-1')
              if message=="True":
                   print("تم بنجاح")
                   messagebox.showinfo("MessageBox","تم  حذف الحساب بنجاح ")

              else:
                   print("فشل")
                   messagebox.showinfo("MessageBox","فشل في حذف الحساب  ")
         
    client_socket.close()
def open_new_window():
    global user1 ,coode1
    root=Toplevel(window)
    root.title("نسيان كلمة المرور")
    root.geometry('400x490+0+110')
    root.configure(bg="#6ca8a3")
    root.resizable(False,False)
    root.iconbitmap("C:/Users/SAJA/Desktop/program_final/images/m_icon.ico")
    #Label(root,width=20,text='تغيير كلمــة المــرور',font=('Micrsoft YaHei UI Light ',20,'bold'),fg='black',bg='#6ca8a3',border=0).place(x=40,y=9)
    #Label(root,width=30,text='يرجى إدخال أسم المستخـدم مع كلمة المرورجديد',font=('Micrsoft YaHei UI Light ',15,'bold'),fg='white',bg='#6ca8a3',border=0).place(x=35,y=65)
    def on_enter(e):
        username=user1.get()
        if username == 'اسم المستخدم':
            user1.delete(0,'end')
    def on_leave(e):
        us_name=user1.get()
        if us_name=='':
           user1.insert(0,'اسم المستخدم')
    user1=Entry(root,width=20,fg='black',border=0,bg='white',font=('Micrsoft YaHei UI Light ',20,'bold'))
    user1.place(x=40,y=130)
    user1.insert(0,'اسم المستخدم')
    user1.bind('<FocusIn>',on_enter)
    user1.bind('<FocusOut>',on_leave) 
    def on_enter(e):
        useremail=coode1.get()
        if useremail == 'بريدك الالكتروني':
            coode1.delete(0,'end')
    def on_leave(e):
        us_email=coode1.get()
        if us_email=='':
           coode1.insert(0,'بريدك الالكتروني')
    coode1=Entry(root,width=20,fg='#ff686b',border=0,bg="white",font=('Micrsoft YaHei UI Light ',20,'bold'))
    coode1.place(x=40,y=190)
    coode1.bind('<FocusIn>',on_enter)
    coode1.bind('<FocusOut>',on_leave)
    coode1.insert(0,'بريدك الالكتروني')
    Button(root,text="التـــالــي",font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='tan2',command=forget_password,width=30,cursor='hand2',activebackground='#ee1111').place(x=40,y=260)
#--------------------------------------------------------------------------
def view_create_account_window():
    global user_name,password,email,canvas
    window1=Toplevel(window)
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
        mypassword=password.get()
        if mypassword == 'كـلمــــة المــــرور':
            password.delete(0,'end')
    def on_leave(e):
        code=password.get()
        if code=='':
           password.insert(0,'كـلمــــة المــــرور')
    password=Entry(window1,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',17,'bold'))
    password.place(x=687,y=355)
    password.insert(0,'كـلمــــة المــــرور')
    password.bind('<FocusIn>',on_enter)
    password.bind('<FocusOut>',on_leave) 
    def on_enter(e):
        name=user_name.get()
        if name =='إســم الـمستخـدم':
            user_name.delete(0,'end')
    def on_leave(e):
        name=user_name.get()
        if name=='':
            user_name.insert(0,'إســم الـمستخـدم')         
    user_name=Entry(window1,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',17,'bold'))
    user_name.place(x=687,y=309)
    user_name.insert(0,'إســم الـمستخـدم')
    user_name.bind('<FocusIn>',on_enter)
    user_name.bind('<FocusOut>',on_leave)
    def on_enter(e):
        myemail=email.get()
        if myemail =='البــريد الإلكتــروني':
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
    Button(window1,text="افتح الكـاميـرا",width=10,font=('yu gothic ui',12,'bold'),activeforeground='black',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f',command=show_frame).place(x=762,y=462)
    canvas = Canvas(window1, width=300, height=300, bg='snow2')
    canvas.place(x=334, y=331)
    Button(window1,text=" جـديـد حســاب أنشــاء ",width=16,font=('yu gothic ui',11,'bold'),activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea',command=create_account).place(x=735,y=578)
    Button(window1,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f',command=Stop_camera).place(x=760,y=510)
    window1.mainloop()
#...................................................................
def view_main_interface_window():
    window2=Toplevel(window)
    window2.geometry('985x620+150+0')
    window2.state('zoomed')
    window2.title('المراقب الافتراضي')
    window2.resizable(False,False)
    window2.iconbitmap("images/m_icon.ico")
    logo_image=ImageTk.PhotoImage(Image.open("images/m3 .jpg"))  
    Label(window2,image=logo_image,bg='white').place(x=0,y=0)
    Button(window2,text="الإختبــار بدا",width=10,command=view_instructions_window,font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=1128,y=28)
    Button(window2,text="السابق الإختبار عرض",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=900,y=29)
    Button(window2,text="الـحســـاب حـذف",command=delete_acount,width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=680,y=28)
    Button(window2,text="المـرور كلمـة تغيير",command=view_change_password_window,width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=450,y=28)
    window2.mainloop()
#--------------------------------------------------------------------
def view_instructions_window():
    window3=Toplevel(window)
    window3.title("التـعليمــــات")
    #window1.geometry('400x490+0+110')
   # window1.configure(bg='#031634')
    window3.state('zoomed')
    window3.iconbitmap("images/m_icon.ico")
    pic=ImageTk.PhotoImage(Image.open("images/m4.jpg"))
    Label(window3,image=pic,bg='white').place(x=0,y=0)
    Button(window3,text="فهمت لقد",width=10,command=view_start_exam_window,font=('yu gothic ui',17,'bold'),activeforeground='white',fg='white',bd=3, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=10,y=600)
    window3.mainloop()

#--------------------------------------------------------------------
def view_start_exam_window():
    global subject_name,canvas_start_exam
    window4=Toplevel(window)
    window4.title("بدأ الاختبار")
    window4.geometry('400x490+0+110')
    window4.configure(bg='#97f8e4')
    window4.geometry('985x620+150+0')
    window4.state('zoomed')
    window4.iconbitmap("images/m_icon.ico")
    pic=ImageTk.PhotoImage(Image.open("images/m7.jpg"))
    Label(window4,image=pic,bg='#97f8e4').place(x=100,y=0)
    def on_enter(e):
        mysubject=subject_name.get()
        if mysubject =='أسم المـادة':
            subject_name.delete(0,'end')
    def on_leave(e):
        name=subject_name.get()
        if name=='':
            subject_name.insert(0,'أسم المـادة')
    subject_name=Entry(window4,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
    subject_name.place(x=219,y=20)
    subject_name.insert(0,'أسم المـادة')
    subject_name.bind('<FocusIn>',on_enter)
    subject_name.bind('<FocusOut>',on_leave) 
    
    canvas_start_exam = Canvas(window4, width=260, height=300, bg='white')
    canvas_start_exam.place(x=187, y=100) 
    Button(window4,text='صـورة التقط',command=Stop_camera_start_exam,width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=510)
    Button(window4,text='فتح الكاميرا',command=show_frame_start_exam,width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=450)
    Button(window4,text='ارسال',command=start_exam_button,width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=567)
    window4.mainloop()

#--------------------------------------------------------------------
def view_change_password_window():
    global new_password,last_password
    window5=Toplevel(window)
    window5.title("تغير كلمة المـرور")
    window5.geometry('985x900+150+0')
    window5.state('zoomed')
    window5.configure(bg="#97f8e4")
    window5.iconbitmap("images/m_icon.ico")
    logo_image2=ImageTk.PhotoImage(Image.open("images/m6.jpg"))  
    Label(window5,image=logo_image2,bg='#97f8e4').place(x=100,y=0)
    def on_enter(e):
        n_password=new_password.get()
        if n_password =='كـلمــــة المــــرور الجديدة':
            new_password.delete(0,'end')
    def on_leave(e):
        name=new_password.get()
        if name=='':
            new_password.insert(0,'كـلمــــة المــــرور الجديدة')
    new_password=Entry(window5,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
    new_password.place(x=550,y=390)
    new_password.insert(0,'كـلمــــة المــــرور الجديدة')
    new_password.bind('<FocusIn>',on_enter)
    new_password.bind('<FocusOut>',on_leave) 
        #---------------------------------------------
    def on_enter(e):
        la_password=last_password.get()
        if la_password =='كلمة المرور القديمة':
            last_password.delete(0,'end')
    def on_leave(e):
        name=last_password.get()
        if name=='':
            last_password.insert(0,'كلمة المرور القديمة')        
    last_password=Entry(window5,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
    last_password.place(x=550,y=327)
    last_password.insert(0,'كلمة المرور القديمة')
    last_password.bind('<FocusIn>',on_enter)
    last_password.bind('<FocusOut>',on_leave)
        #---------------------------------------------
    Button(window5,text=" تغييـــر ",width=13,command=change_password,font=('yu gothic ui',16,'bold'),activeforeground='black',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=555,y=490)

    window5.mainloop()
#--------------------------------------------------------------------
window.iconbitmap("C:/Users/SAJA/Desktop/program_final/images/m_icon.ico")
logo_image = Image.open("C:/Users/SAJA/Desktop/program_final/images/m.jpg")
logo_image2 = ImageTk.PhotoImage(logo_image) 
lab=Label(window,image=logo_image2,bg='#6ca8a3')
lab.place(x=100,y=7)
btn=Button(window,width=10,text='تسجيــل الـدخــول',font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=793,y=248)
btn_up=Button(window,width=10,text='انشاء حسـاب جديد',command=view_create_account_window,font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='white',bg="#098d72",border=0)
btn_up.place(x=650,y=248)
def on_enter(e):
    lo_password=password_log_in.get()
    if lo_password =='كـلمــــة المــــرور':
        password_log_in.delete(0,'end')
def on_leave(e):
    name=password_log_in.get()
    if name=='':
       password_log_in.insert(0,'كـلمــــة المــــرور')
password_log_in=Entry(window,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',16,'bold'))
password_log_in.place(x=680,y=365)
password_log_in.insert(0,'كـلمــــة المــــرور')
password_log_in.bind('<FocusIn>',on_enter)
password_log_in.bind('<FocusOut>',on_leave) 
def on_enter(e):
    lo_name=user_name_log_in.get()
    if lo_name =='إســم الـمستخـدم':
        user_name_log_in.delete(0,'end')
def on_leave(e):
    name=user_name_log_in.get()
    if name=='':
        user_name_log_in.insert(0,'إســم الـمستخـدم') 
        
user_name_log_in=Entry(window,width=15,fg='gray63',border=0,justify= "right",bg="#eaeaea",font=('Arial',16,'bold'))
user_name_log_in.place(x=681,y=319)
user_name_log_in.insert(0,'إســم الـمستخـدم')
user_name_log_in.bind('<FocusIn>',on_enter)
user_name_log_in.bind('<FocusOut>',on_leave)

Button(window,text="افتـح الكاميـرا ",width=9,font=('Arial',12,'bold'),command=show_frame_log_in,activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=757,y=470)
canvas_log_in = Canvas(window, width=300, height=300, bg='snow2')
canvas_log_in.place(x=334, y=331) 
btn=Button(window,width=15,command=open_new_window,text='لا اتذكر كلمـة المرور',font=('Arial',14,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=735,y=413)
Button(window,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),command=Stop_camera_log_in,activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=760,y=524)
Button(window,text=" تسجــل الـدخــول ",width=16,font=('Arial',11,'bold'),command=log_in,activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea').place(x=735,y=585)
window.mainloop()