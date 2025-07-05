from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox

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
window.iconbitmap("C:/Users/PC/Desktop/server/m_icon.ico")
image=Image.open("s1.png") 
image=image.resize((200,200))
photo=ImageTk.PhotoImage(image)
label=Label(window,image=photo,bg='#e2f0fb')
label.place(x=548,y=47)
# إنشاء عناصر واجهة المستخدم
def show_message():
    result=messagebox.askquestion("MessageBox","هل نسيت كلمة المرور بالفعل")
    if result=='yes':
         messagebox.showinfo("MessageBox",":قم بانشاء حساب جديد  ")
        
    else:
       messagebox.showinfo(" MessageBox","من فضلك،حاول مرة اخرى")



def on_enter(e):
    entry_username.delete(0,'end')
def on_leave(e):
    name=entry_username.get()    


def drt_click():
    
    root=Toplevel(window)
    #root.config(bg="BLACK",padx=50,pady=70)
    root.title("انشاء حساب")
    root.geometry("500x400+200+500")
    root.state('zoomed')
    root.iconbitmap("C:/Users/PC/Desktop/server/m_icon.ico")
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
    label.place(x=549,y=47)
# إنشاء عناصر واجهة المستخدم
    def on_enter(e):
        entry_username.delete(0,'end')
    def on_leave(e):
        name=entry_username.get()
        if name=='':
            entry_username.insert(0,'اكتب الاسم هنا') 
    entry_username = Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),relief=SOLID,justify="center")
    entry_username.place(x=540,y=327)
    entry_username.insert(0,'اكتب الاسم هنا')
    entry_username.bind('<FocusIn>',on_enter)
    entry_username.bind('<FocusOut>',on_leave) 

    def on_enter(e):
        coode.delete(0,'end')
    def on_leave(e):
        name=coode.get()
        if name=='':
            coode.insert(0,'إســم الـمستخـدم') 
    coode=Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),justify="center",show="*")
    coode.place(x=531,y=376)
    coode.insert(0,'اكتب كلمة المرور الخاصة بك')
    coode.bind('<FocusIn>',on_enter)
    coode.bind('<FocusOut>',on_leave)
    def on_enter(e):
        email.delete(0,'end')
    def on_leave(e):
        name=email.get()
        if name=='':
            email.insert(0,'البــريد الإلكتــروني')         
    email=Entry(root,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',14,'bold'))
    email.place(x=530,y=420)
    email.insert(0,'البــريد الإلكتــروني')
    email.bind('<FocusIn>',on_enter)
    email.bind('<FocusOut>',on_leave)
    
    
    button_login = Button(root,width=15, text="انشــاء حســاب ",font=('Arial',12,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=vrt_pio)
    button_login.place(x=565,y=475)
    button_login1 = Button(root,width=15, text="لدي حسـاب بالفعــل ",font=('Arial',12,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=vrt_pio)
    button_login1.place(x=560,y=543)
    button_login = Button(root,text="خروج ",activebackground='#ff7f2f',font=('Arial',13,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',border=0,cursor='hand2')
    button_login.place(x=454,y=595)
    #container.config(width="1000",height="850")
 
    root.mainloop()
    
def vrt_pio():
        window1=Toplevel(window)
        window1.config(bg="#66849c",padx=50,pady=70)
        window1.title("بدء المراقبه ")
        window1.geometry("500x400")
        window1.state('zoomed')
        window1.resizable(False,False)
        window1.iconbitmap("C:/Users/PC/Desktop/server/m_icon.ico")
#window.attributes("-alpha",0.3)
        image=Image.open("i.jpg")
        image=image.resize((1300,590),Image.ANTIALIAS)
        background_image=ImageTk.PhotoImage(image)
        background_label=Label(window1,image=background_image)
        background_label.place(x=0,y=0,relwidth=1,relheight=1)
        #container=Frame(window1,border=0,relief=GROOVE,padx=100,pady=20,bg="#D0DEF6")
        #container.pack()
        button_login = Button(window1, width=13,text="بدء المراقبه ",font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2')
        button_login.place(x=860,y=90)
        button_login = Button(window1,width=13, text="عرض النتائج ",font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2')
        button_login.place(x=650,y=160)
        button_login = Button(window1,width=13, text="حذف الحساب  ",font=('Arial',19,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='white',activebackground='#f8c701',border=0,cursor='hand2')
        button_login.place(x=470,y=236)
        button_login = Button(window1, text="خروج  ",font=('Arial',16,'bold'),relief=GROOVE,bg="#f8c701",activeforeground='red',activebackground='#f8c701',border=0,cursor='hand2')
        button_login.place(x=340,y=460)
        #container.config(width="1000",height="850")
        window1.mainloop()
def on_enter(e):
    entry_username.delete(0,'end')
def on_leave(e):
    name=entry_username.get()
    if name=='':
        entry_username.insert(0,'اكتب اسمك هنا من فضلك') 
entry_username = Entry(window,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),relief=SOLID,justify="center")
entry_username.place(x=531,y=335)
entry_username.insert(0,'اكتب اسمك هنا من فضلك')
entry_username.bind('<FocusIn>',on_enter)
entry_username.bind('<FocusOut>',on_leave) 

def on_enter(e):
    coode.delete(0,'end')
def on_leave(e):
    name=coode.get()
    if name=='':
        coode.insert(0,'اكتب كلمة المرور الخاصة بك') 
coode=Entry(window,width=18,fg='gray63',border=0,bg="#eaeaea",font=('Arial',14,'bold'),justify="center",show="*")
coode.place(x=531,y=383)
coode.insert(0,'اكتب كلمة المرور الخاصة بك')
coode.bind('<FocusIn>',on_enter)
coode.bind('<FocusOut>',on_leave)



button_login = Button(window, text="تسجيل الدخول",font=('Arial',15,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=vrt_pio)
button_login.place(x=590,y=476)
label_forgot_password = Label(window, text="هل نسيت كلمة المرور؟",bg='white',font=('Arial ',14,'bold'),fg="red",cursor="hand2")
label_forgot_password.place(x=600,y=417)
label_forgot_password.bind("<Button-1>",lambda event:show_message())
button_create_account = Button(window, text=" إنشاء حساب جديد  ",font=('Arial',15,'bold'),relief=GROOVE,bg="#ff7f2f",activeforeground='white',activebackground='#ff7f2f',border=0,cursor='hand2',command=drt_click)
button_create_account.place(x=575,y=562)
#container.config(width="1000",height="850")
window.mainloop()
