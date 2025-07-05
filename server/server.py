import socket
import threading
import numpy as np
import cv2
import pickle
import struct
import pyshine as ps
import mysql.connector
import face_recognition
import os
import math
import sys
import keyboard
from datetime import datetime
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import re
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import pandas as pd



db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="virtual_proctor")
cursor=db.cursor()


global myid
folder_name = "faces"

# تأكد من وجود المجلد
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def send_to_email(email,message):
    host_email = 'smtp.gmail.com'  # استبدله بعنوان خادم البريد الإلكتروني المناسب
    port_email = 587  # استبدله بمنفذ الخادم المناسب
    username = 'virtualproctor2023@gmail.com'  # استبدله بعنوان بريدك الإلكتروني
    password = 'kjae gqzh tqvd jkue'  # استبدله بكلمة مرور بريدك الإلكتروني
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email # استبدله بعنوان بريد المستلم
    msg['Subject'] ='كلمة المرور'
    body = f'كلمة المرور الخاصة بك هو: {message}'
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP(host_email, port_email) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def show_client(addr,client_socket,name,subject):
    global video_file_name
    fourcc =0x7634706d 
    now = datetime.now()
    time_str = now.strftime("%d%m%Y%H%M%S")
    time_name = time_str+'.mp4'
    fps = 1.0
    frame_shape = False
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket: # if a client socket exists
            data = b""
            payload_size = struct.calcsize("Q")
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]
                
                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                text  =  f"CLIENT: {addr}"
                time_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                frame =  ps.putBText(frame,time_now,10,10,vspace=10,hspace=1,font_scale=0.7, background_RGB=(255,0,0),text_RGB=(255,250,250))
                
                if not frame_shape:
                    
                    video_file_name  = name+"-"+subject + time_name
                    out = cv2.VideoWriter(video_file_name, fourcc, fps, (frame.shape[1], frame.shape[0]), True)
                    frame_shape = True
                out.write(frame)
                cv2.imshow(f"FROM {addr}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
            client_socket.close()
    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        pass
		

def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range_val * 2.0)
    if face_distance > face_match_threshold:
        return (round(linear_val * 100, 2))
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return (round(value, 2))

class FaceRecognition:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_current_frame = True
        self.encode_faces()

    def encode_faces(self):

        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(os.path.join('faces', image))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self,frame):
        name = 'Unknown'
        confidence = 0
        if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    
                    if len(matches) > 0:
                        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index]:
                            name = self.known_face_names[best_match_index]
                            confidence = face_confidence(face_distances[best_match_index])
                    self.face_names.append(f'{name}({confidence})')
        self.process_current_frame = not self.process_current_frame
        return name,confidence 


def process_client_request(addr, client_socket):

    print("تم اتقبال طلب جديد")
    process_type = client_socket.recv(1024).decode('latin-1')
    print(process_type)

    if process_type == "create_account":
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
        # استقبال البيانات
        data_create_account = client_socket.recv(data_size).decode('latin-1')
        name, password, email = data_create_account.split(',')
        print(name)
        print(password)
        print(email)
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
                packet = client_socket.recv(64*1024)  # 4K
                if not packet:
                    break
                data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(64*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        text = f"CLIENT: {addr}"
        cv2.imshow(f"FROM {addr}", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("تم استقبال الصورة")
        output_path = os.path.join(folder_name, name+".jpg")
        cv2.imwrite(output_path, frame)
        
        with open('faces/'+name+".jpg","rb") as file:
            image_byte=file.read()
        try:
            sql="INSERT INTO student(student_name,password,student_email,student_image) VALUES (%s,%s,%s,%s) "
            cursor.execute(sql,(name,password,email,image_byte))
            db.commit()
            print("تم إضافة البيانات بنجاح")
            response = "True"
        except Exception as e:
            db.rollback()  # إلغاء أي تغييرات في حالة حدوث خطأ
            print("حدث خطأ أثناء إضافة البيانات:", str(e))
            response = "Flase"
        data.flush()
        data_create_account.flush()
        frame_data.flush()
        client_socket.sendall(response.encode())
        client_socket.close()
        
    
    elif process_type == "log_in":
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
        print(data_size)
        # استقبال البيانات
        data_log_in = client_socket.recv(data_size).decode('latin-1')
        name, password = data_log_in.split(',')
        print(name)
        print(password)
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
                packet = client_socket.recv(64*1024)  # 4K
                if not packet:
                    break
                data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(64*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        text = f"CLIENT: {addr}"
        cv2.imshow(f"FROM {addr}", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("تم استقبال الصورة")
        query = "SELECT * FROM student WHERE student_name=%s AND password=%s"
        try:
            cursor.execute(query, (name, password))
            result = cursor.fetchone()
            db.commit()
            fr = FaceRecognition()
            n,c=fr.run_recognition(frame)
            print(n)
            if n!='Unknown':
                nn,path=n.split('.')
            else:
                nn='Unknown'
            print(result)
            print(c)
            if result and nn==name and c>85:
                response = "True"
                id=str(result[0])
                client_socket.sendall(response.encode())
                client_socket.sendall(id.encode())
                print("تم التحقق بنجاح")
            else:
                response = "False"
                client_socket.sendall(response.encode())
                print("فشل في التحقق")
        except Exception as e:
            db.rollback()  # إلغاء أي تغييرات في حالة حدوث خطأ
            print("حدث خطأ أثناء الاستعلام عن البيانات:", str(e))
            response = "Flase"
            client_socket.sendall(response.encode())
        client_socket.close() 
        data.flush()
        data_log_in.flush()
        frame_data.flush()
     
        
    elif process_type == "change_password":
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
            # استقبال البيانات
        data_change_password = client_socket.recv(data_size).decode('latin-1')
        student_id1,new_password=data_change_password.split(',')
        student_id_int=int(student_id1)
        sql="UPDATE student SET password=%s WHERE student_id=%s"
        cursor.execute(sql,(new_password,student_id_int))
        db.commit()
        print("تم تعيير كلمة المرور بنجاح")
        response = "True"
        client_socket.sendall(response.encode())
        client_socket.close()
        data_change_password.flush()
        
    elif process_type=="start_exam":
        global student_id,student_name,subject
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
        print(data_size)
        data_start_exam = client_socket.recv(data_size).decode('latin-1')
        print(data_start_exam)
        student_id,student_name,subject=data_start_exam.split(',')
        data = b""
        payload_size = struct.calcsize("Q")
        while len(data) < payload_size:
                packet = client_socket.recv(64*1024)  # 4K
                if not packet:
                    break
                data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(64*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        text = f"CLIENT: {addr}"
        cv2.imshow(f"FROM {addr}", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("تم استقبال الصورة")
        fr = FaceRecognition()
        n,c=fr.run_recognition(frame)
        print(n)
        nn=""
        if n!='Unknown':
            nn,path=n.split('.')
        else:
            nn='Unknown'
        print(c)
        if nn==student_name and c>85:
            response = "True"
            client_socket.sendall(response.encode())
            print("تم التحقق بنجاح")
            
        else:
            response = "False"
            client_socket.sendall(response.encode())
            print("فشل في التحقق")
        
        client_socket.close()
        data_start_exam.flush()
        data.flush()
        frame_data.flush()
    
    elif process_type=='view_client':
       show_client(addr, client_socket,student_name,subject)
    elif process_type=='send_notes':
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
        print(data_size)
        move_note=client_socket.recv(data_size).decode('utf-8')
        print("Move Note:", move_note)
        
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
        print(data_size)
        voice_note =client_socket.recv(data_size*2).decode('utf-16')
        print("تم استقبال البيانات")
        day_date=date.today()
        day_date=str(day_date)
        with open(video_file_name,"rb") as file:
            video_data=file.read()
        try:
            sql="INSERT INTO reports(student_id, teacher_id, subject, date, movement_notes, voice_note, video) VALUES  (%s,%s,%s,%s,%s,%s,%s) "
            cursor.execute(sql,(student_id,3,subject,day_date,move_note,voice_note,video_data))
            db.commit()
            print("تم إضافة البيانات بنجاح")
        except Exception as e:
            db.rollback()  # إلغاء أي تغييرات في حالة حدوث خطأ
            print("حدث خطأ أثناء إضافة البيانات:", str(e)) 
        client_socket.close()
    
    elif process_type=='forget_password':
        data_size = struct.unpack('!I', client_socket.recv(4))[0]
            # استقبال البيانات
        data_forget_password = client_socket.recv(data_size).decode('latin-1')
        user_name,user_email=data_forget_password.split(',')
        print(data_forget_password)
        query = "SELECT * FROM student WHERE student_name=%s AND student_email=%s"
        try:
            cursor.execute(query, (user_name, user_email))
            result = cursor.fetchone()
            db.commit()
            if result:
                response = "True"
                send_to_email(result[3],result[2])
                print("تم الارسال بنجاح")
                print(result[3])
                print(result[2])

            else:
                response="False"
        except Exception as e:
            db.rollback()  
            print("حدث خطأ أثناء الاستعلام عن البيانات:", str(e))
            response = "Flase"
        client_socket.sendall(response.encode())
        client_socket.close()
        del data_forget_password
    
    elif process_type=='delete_account':
        ata_size = struct.unpack('!I', client_socket.recv(4))[0]
        data_delete_account = client_socket.recv(data_size).decode('latin-1')
        student_id_int=int(data_delete_account)
        query = "DELETE FROM student WHERE student_id =%s"
        try:
            cursor.execute(query,(student_id_int,))
            db.commit()
            print("تم حذف الحساب بنجاخ")
            response="True"
        except Exception as e:
            db.rollback()
            print("حدث خطأ أثناء حذف الحساب:", str(e))
            response = "Flase"
        client_socket.sendall(response.encode())
        client_socket.close()

def open_connection():
    messagebox.showinfo(" MessageBox","تم فتح الاتصال بنجاح")
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:',host_ip)
    port = 9999
    socket_address = (host_ip,port)
    server_socket.bind(socket_address)
    server_socket.listen()
    print("Listening at",socket_address)   
    while True:
        client_socket,addr = server_socket.accept()
        thread = threading.Thread(target=process_client_request, args=(addr,client_socket))
        thread.start()
        print("TOTAL CLIENTS ",threading.activeCount() - 1)

def view_data():
    query = "SELECT student.student_name,teacher.teacher_name,reports.subject,reports.date,reports.movement_notes,voice_note FROM student,reports,teacher WHERE student.student_id=reports.student_id and teacher.teacher_id=reports.teacher_id "
    data_frame = pd.read_sql(query, db)

    # استبعاد العمود الذي لا ترغب في عرضه
    columns_to_display = [col for col in data_frame.columns if col != 'video' and col !='id']
    data_frame_filtered = data_frame[columns_to_display]

    # إنشاء واجهة المستخدم وعرض البيانات في DataGridView
    app = QApplication(sys.argv)

    window_data = QMainWindow()
    window_data .setWindowTitle("DataGridview Example")

    table_view = QTableView(window_data )

    # تحويل البيانات إلى QStandardItemModel
    model = QStandardItemModel(data_frame_filtered.shape[0], data_frame_filtered.shape[1])
    model.setHorizontalHeaderLabels(data_frame_filtered.columns)

    for row in range(data_frame_filtered.shape[0]):
        for column in range(data_frame_filtered.shape[1]):
            item = QStandardItem(str(data_frame_filtered.iloc[row, column]))
            model.setItem(row, column, item)

    table_view.setModel(model)

    table_view.resizeColumnsToContents()

    window_data.setCentralWidget(table_view)
    window_data.show()

    sys.exit(app.exec_())

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # تعبير عادي للتحقق من الصيغة

    if re.match(pattern, email):
        return True
    else:
        return False
#_________________________________________________
def delete():
    result=messagebox.askquestion("MessageBox","هل تريد حذف الحساب")
    if result=="yes":
        tid=myid
        insert_query = "DELETE FROM teacher WHERE teacher_id =%s"
        cursor.execute(insert_query,(tid,))
        db.commit()
        messagebox.showinfo(" MessageBox","تم حذف الحساب بنجاح")

#_________________________________________________
def open_connection_btn():
    thread = threading.Thread(target=open_connection)
    thread.start()
# واجهة بدء المراقبة
def start_exam():
    def close_window():
        window1.destroy()
    window1 = Toplevel(window)
    window1.config(bg="#66849c",padx=50,pady=70)
    window1.title("بدء المراقبه ")
    window1.geometry("500x400")
    window1.state('zoomed')
    window1.resizable(False,False)
    window1.iconbitmap("m_icon.ico")
    #window.attributes("-alpha",0.3)
    image=Image.open("i.jpg")
    image=image.resize((1300,590),Image.ANTIALIAS)
    background_image=ImageTk.PhotoImage(image)
    background_label=Label(window1,image=background_image)
    background_label.place(x=0,y=0,relwidth=1,relheight=1)
        #container=Frame(window1,border=0,relief=GROOVE,padx=100,pady=20,bg="#D0DEF6")
        #container.pack()
    button_login = Button(window1, width=13,text="فتح الاتصال ",command=open_connection_btn,font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2')
    button_login.place(x=860,y=90)
    button_login = Button(window1,width=13, text="عرض النتائج ",command=view_data,font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2')
    button_login.place(x=650,y=160)
    button_login = Button(window1,width=13, text="حذف الحساب  ",font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2',command=delete)
    button_login.place(x=470,y=236)
    button_login = Button(window1, text="خروج  ",font=('Arial',16,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='red',activebackground='#f8c701',border=0,cursor='hand2',command=close_window)
    button_login.place(x=340,y=460)
        #container.config(width="1000",height="850")
    window1.mainloop()

#_________________________________________________
def create_account():
    user_name=entry_username1.get()
    password=coode1.get()
    user_email=email.get()
    if (user_name !="اكتب الاسم هنا" or user_name!="") and (password !="كلمة المرور " or password!="" )and (user_email !="البــريد الإلكتــروني" or user_email ==""):
        if validate_email(user_email):
            insert_query = "INSERT INTO teacher (teacher_name,password,teacher_email) VALUES (%s,%s,%s)"
            cursor.execute(insert_query, (user_name,password,user_email))
            db.commit()
            messagebox.showinfo(" MessageBox","تمت اضافة المستخدم الى قاعدة البيانات بنجاح")
        else:
            messagebox.showinfo(" MessageBox"," البريد الالكتروني غير صحيح")

    else:
        messagebox.showinfo(" MessageBox"," تاكد من تعبئة جميع الحقول بشكل صحيح")

#_________________________________________________
# واجهة انشاء حساب 
def creat_windo():
    def close_window1():
        root.destroy()
    global entry_username1,coode1,email
    root = Toplevel(window)
    #root.config(bg="BLACK",padx=50,pady=70)
    root.title("انشاء حساب")
    root.geometry("500x400+200+500")
    root.state('zoomed')
    root.iconbitmap("m_icon.ico")
    root.resizable(False,False)
    image=Image.open("r4.jpg")
    image=image.resize((1400,700),Image.ANTIALIAS)
    background_image=ImageTk.PhotoImage(image)
    background_label=Label(root,image=background_image)
    background_label.place(x=0,y=0,relwidth=1,relheight=1)

    image=Image.open("s1.png") 
    image=image.resize((200,200))
    photo=ImageTk.PhotoImage(image)
    label=Label(root,image=photo,bg='#ffe0cc')
    label.place(x=670,y=118)
    # إنشاء عناصر واجهة المستخدم
    def on_enter(e):
        check=entry_username1.get()
        if check=='اكتب الاسم هنا':
            entry_username1.delete(0,'end')
    def on_leave(e):
        name=entry_username1.get()
        if name=='':
            entry_username1.insert(0,'اكتب الاسم هنا') 
    entry_username1 = Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),relief=SOLID,justify="center")
    entry_username1.place(x=665,y=400)
    entry_username1.insert(0,'اكتب الاسم هنا')
    entry_username1.bind('<FocusIn>',on_enter)
    entry_username1.bind('<FocusOut>',on_leave) 

    def on_enter(e):
        check=coode1.get()
        if check=='كلمة المرور ':
            coode1.delete(0,'end')
    def on_leave(e):
        name=coode1.get()
        if name=='':
            coode1.insert(0,'كلمة المرور ') 
    coode1=Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),justify="center",show="*")
    coode1.place(x=665,y=447)
    coode1.insert(0,'كلمة المرور ')
    coode1.bind('<FocusIn>',on_enter)
    coode1.bind('<FocusOut>',on_leave)
    def on_enter(e):
        check=email.get()
        if check=='البــريد الإلكتــروني':
            email.delete(0,'end')
    def on_leave(e):
        name=email.get()
        if name=='':
            email.insert(0,'البــريد الإلكتــروني')         
    email=Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',14,'bold'))
    email.place(x=675,y=490)
    email.insert(0,'البــريد الإلكتــروني')
    email.bind('<FocusIn>',on_enter)
    email.bind('<FocusOut>',on_leave)
    
    
    button_login = Button(root,width=15, text="انشــاء حســاب ",font=('Arial',12,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=create_account)
    button_login.place(x=700,y=545)
    button_login1 = Button(root,width=15, text="لدي حسـاب بالفعــل ",font=('Arial',12,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=close_window1)
    button_login1.place(x=700,y=615)
    button_login = Button(root,text="خروج ",activebackground='#ff7f2f',font=('Arial',13,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',border=0,cursor='hand2',command=close_window1)
    button_login.place(x=585,y=667)
    #container.config(width="1000",height="850")
 
    root.mainloop()
#_________________________________________________
def forget_password_btn():
    name_user=user1.get()
    email_user=email1.get()
    if (name_user!='' or name_user!='اسم المستخدم') and (email_user!='' or email_user!='بريدك الالكتروني'):
        if not validate_email(email_user):
            messagebox.showinfo(" MessageBox"," البريد الالكتروني غير صحيح")
        else:
            query = "SELECT * FROM teacher WHERE teacher_name=%s AND teacher_email=%s"
            try:
                cursor.execute(query, (name_user, email_user))
                result = cursor.fetchone()
                db.commit()
                if result:
                    send_to_email(email_user,result[2])
                    messagebox.showinfo("MessageBox","تم ارسال كلمة المرور الخاصة بك الى بريدك الالكتروني ")
                else:
                    messagebox.showinfo(" MessageBox"," لا يوجد حساب بالبيانات التي ادخلتها")
            except Exception as e:
                db.rollback()  
                print("حدث خطأ أثناء الاستعلام عن البيانات:", str(e))
                messagebox.showinfo(" MessageBox","حدث خطأ أثناء الاستعلام عن البيانات:")

            
                    
    else:
        messagebox.showinfo(" MessageBox"," تاكد من تعبئة جميع الحقول بشكل صحيح")
    
        


def forget_password_window():
    global user1 ,email1
    window4=Toplevel(window)
    window4.title("نسيان كلمة المرور")
    window4.geometry('400x490+0+110')
    window4.configure(bg="#6ca8a3")
    window4.resizable(False,False)
    #window4.iconbitmap("C:/Users/SAJA/Desktop/program_final/images/m_icon.ico")
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
    user1=Entry(window4,width=20,fg='gray63',border=0,bg='white',font=('Micrsoft YaHei UI Light ',20,'bold'))
    user1.place(x=40,y=130)
    user1.insert(0,'اسم المستخدم')
    user1.bind('<FocusIn>',on_enter)
    user1.bind('<FocusOut>',on_leave)
    def on_enter(e):
        useremail=email1.get()
        if useremail == 'بريدك الالكتروني':
            email1.delete(0,'end')
    def on_leave(e):
        us_email=email1.get()
        if us_email=='':
           email1.insert(0,'بريدك الالكتروني')
    email1=Entry(window4,width=20,fg='gray63',border=0,bg="white",font=('Micrsoft YaHei UI Light ',20,'bold'))
    email1.place(x=40,y=190)
    email1.insert(0,'بريدك الالكتروني')
    email1.bind('<FocusIn>',on_enter)
    email1.bind('<FocusOut>',on_leave)
    Button(window4,text="التـــالــي",font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='tan2',command=forget_password_btn,width=30,cursor='hand2',activebackground='#ee1119').place(x=40,y=260)
#--------------------------------------------------------------------------



#*************************************************
#*************************************************
# إنشاء نافذة التطبيق
window = Tk()
#window.config(bg="black",padx=50,pady=70)
window.title("تسجيل الدخول")
window.geometry("500x400")
window.state('zoomed')
window.resizable(False,False)
image=Image.open("r3.jpg")
image=image.resize((1400,700),Image.ANTIALIAS)
background_image=ImageTk.PhotoImage(image)
background_label=Label(window,image=background_image)
background_label.place(x=0,y=0,relwidth=1,relheight=1)
#container=Frame(window,border=0,relief=GROOVE,padx=100,pady=50,bg="#47948A")
#container.pack()
window.iconbitmap("m_icon.ico")
image=Image.open("s1.png") 
image=image.resize((200,200))
photo=ImageTk.PhotoImage(image)
label=Label(window,image=photo,bg='#e2f0fb')

    
label.place(x=665,y=120)
    # إنشاء عناصر واجهة المستخدم
def show_message():
    result=messagebox.askquestion("MessageBox","هل نسيت كلمة المرور بالفعل")
    if result=='yes':
        messagebox.showinfo("MessageBox",":قم بانشاء حساب جديد  ")
        
    else:
        messagebox.showinfo(" MessageBox","من فضلك،حاول مرة اخرى")


def log_in():
    user_name=entry_username.get()
    password=coode.get()
    if (user_name !="اكتب اسمك هنا من فضلك" or user_name!="") and (password !="اكتب كلمة المرور الخاصة بك" or password!=""):
        insert_query = "SELECT * FROM teacher WHERE teacher_name=%s AND password=%s "
        cursor.execute(insert_query, (user_name,password))
        result=cursor.fetchone()
        db.commit()
        if result:
            myid=result[0]
            print(myid)
            print(result)
            start_exam()
        else :
            messagebox.showinfo(" MessageBox","من فضلك،تاكد من صحة البيانات المدخلة")
    else:
        messagebox.showinfo(" MessageBox","تاكد من تعبئة جميع الحقول")
             
def on_enter(e):
    name=entry_username.get()
    if name=='اكتب اسمك هنا من فضلك':
        entry_username.delete(0,'end')
def on_leave(e):
    name=entry_username.get()
    if name=='':
        entry_username.insert(0,'اكتب اسمك هنا من فضلك') 
entry_username = Entry(window,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),relief=SOLID,justify="center")
entry_username.place(x=670,y=408)
entry_username.insert(0,'اكتب اسمك هنا من فضلك')
entry_username.bind('<FocusIn>',on_enter)
entry_username.bind('<FocusOut>',on_leave) 

def on_enter(e):
    name=coode.get()
    if name=='اكتب كلمة المرور الخاصة بك':
        coode.delete(0,'end')
def on_leave(e):
    name=coode.get()
    if name=='':
        coode.insert(0,'اكتب كلمة المرور الخاصة بك') 
coode=Entry(window,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),justify="center",show="*")
coode.place(x=670,y=455)
coode.insert(0,'اكتب كلمة المرور الخاصة بك')
coode.bind('<FocusIn>',on_enter)
coode.bind('<FocusOut>',on_leave)



button_login = Button(window, text="تسجيل الدخول",font=('Arial',15,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=log_in)
button_login.place(x=720,y=550)
label_forgot_password = Label(window, text="هل نسيت كلمة المرور؟",bg='white',font=('Arial ',14,'bold'),fg="red",cursor="hand2")
label_forgot_password.place(x=700,y=500)
label_forgot_password.bind("<Button-1>",lambda event:forget_password_window())
button_create_account = Button(window, text=" إنشاء حساب جديد  ",font=('Arial',15,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=creat_windo)
button_create_account.place(x=700,y=630)
#container.config(width="1000",height="850")
window.mainloop()
#*************************************************
#*************************************************

