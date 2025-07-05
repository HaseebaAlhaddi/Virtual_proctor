from tkinter import *
from PIL import ImageTk,Image
#import log_in1 as lo
window=Tk()
window.resizable(False,False)
window.geometry('985x620+150+0')
window.state('zoomed')
window.title("المراقب الافتراضي")
window.configure(bg="#6ca8a3")
#=====================================================#
def open_new_window():
    root=Toplevel(window)
    root.title("تغير كلمــة المــرور")
    root.geometry('400x490+0+110')
    root.configure(bg="#6ca8a3")
    root.resizable(False,False)
    root.iconbitmap("images/m_icon.ico")
    Label(root,width=20,text='تغيير كلمــة المــرور',font=('Micrsoft YaHei UI Light ',20,'bold'),fg='black',bg='#6ca8a3',border=0).place(x=40,y=9)
    Label(root,width=30,text='يرجى إدخال أسم المستخـدم مع كلمة المرورجديد',font=('Micrsoft YaHei UI Light ',15,'bold'),fg='white',bg='#6ca8a3',border=0).place(x=35,y=65)
    user1=Entry(root,width=20,fg='black',border=0,bg='white',font=('Micrsoft YaHei UI Light ',20,'bold'))
    user1.place(x=40,y=130)
    coode1=Entry(root,width=20,fg='#ff686b',border=0,bg="white",font=('Micrsoft YaHei UI Light ',20,'bold'))
    coode1.place(x=40,y=190)
    Button(root,text="التـــالــي",font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='tan2',width=30,cursor='hand2',activebackground='#ee1111').place(x=40,y=260)
#=======================================================#
def open_new_window_up():
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
    Button(window1,text="افتح الكـاميـرا",width=10,font=('yu gothic ui',12,'bold'),activeforeground='black',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=762,y=462)
    Label(window1,width=46,height=20,bg='snow2').place(x=332,y=318)
    Button(window1,text=" جـديـد حســاب أنشــاء ",width=16,font=('yu gothic ui',11,'bold'),activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea').place(x=735,y=578)
    Button(window1,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=760,y=510)
    window1.mainloop()


#=======================================================#
window.iconbitmap("images/m_icon.ico")
logo_image2=ImageTk.PhotoImage(Image.open("images/m.jpg"))  
Label(window,image=logo_image2,bg='#6ca8a3').place(x=100,y=7)
btn=Button(window,width=10,text='تسجيــل الـدخــول',font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=793,y=248)
btn_up=Button(window,width=10,text='انشاء حسـاب جديد',command=open_new_window_up,font=('Arial',17,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='white',bg="#098d72",border=0)
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

Button(window,text="افتـح الكاميـرا ",width=9,font=('Arial',12,'bold'),activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=757,y=470)
Label(window,width=47,height=19,bg='snow2').place(x=330,y=331)
btn=Button(window,width=15,command=open_new_window,text='لا اتذكر كلمـة المرور',font=('Arial',14,'bold'),fg='white',cursor='hand2',activebackground='#12b28e',activeforeground='#12b28e',bg="#12b28e",border=0)
btn.place(x=735,y=413)
Button(window,text="التقـط صـورة",width=9,font=('Arial',12,'bold'),activeforeground='white',fg='black',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=760,y=524)
Button(window,text=" تسجــل الـدخــول ",width=16,font=('Arial',11,'bold'),activeforeground='black',fg='black',bd=0, bg='#eaeaea',cursor='hand2',activebackground='#eaeaea').place(x=735,y=585)

window.mainloop()