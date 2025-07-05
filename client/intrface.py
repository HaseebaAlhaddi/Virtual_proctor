from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
window=Tk()
window.geometry('985x620+150+0')
window.state('zoomed')
window.title('المراقب الافتراضي')
window.resizable(False,False)
#window.configure(bg="#031634")
#=====================================================#
def open_new_window4():
    window3=Toplevel(window)
    window3.title("تغير كلمة المـرور")
    window3.geometry('985x900+150+0')
    window3.state('zoomed')
    window3.configure(bg="#97f8e4")
    window3.iconbitmap("images/m_icon.ico")
    logo_image2=ImageTk.PhotoImage(Image.open("images/m6.jpg"))  
    Label(window3,image=logo_image2,bg='#97f8e4').place(x=100,y=0)
    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        name=user.get()
        if name=='':
            user.insert(0,'كـلمــــة المــــرور')
    user=Entry(window3,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
    user.place(x=550,y=390)
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
    coode=Entry(window3,width=15,fg='gray63',border=0,bg="#eaeaea",font=('Micrsoft YaHei UI Light ',20,'bold'))
    coode.place(x=550,y=327)
    coode.insert(0,'إســم الـمستخـدم')
    coode.bind('<FocusIn>',on_enter)
    coode.bind('<FocusOut>',on_leave)
        #---------------------------------------------
    Button(window3,text=" تغييـــر ",width=13,font=('yu gothic ui',16,'bold'),activeforeground='black',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=555,y=490)

    window3.mainloop()
    
#=====================================================#
def open_new_window3():
    window2=Toplevel(window)
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
    
    tch_name =ttk.Combobox(window2,values=['1','2'],width=25,state='readonly')
    tch_name.place(x=200,y=100)
    tch_name.set('اسم الأستــاذ')
    
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
    sab_name =ttk.Combobox(window2,values=['أفتراضيه','مباشرة'],width=25,state='readonly')
    sab_name.place(x=219,y=210)
    sab_name.set('نــوع المرقبة')
    #entry=Entry(window2)
    #Comb.bind("<<ComboboxSelected>>",lambda event:show_entry())
    #============================================================
    Label(window2,width=35,height=14,bg='white').place(x=195,y=320)
    Button(window2,text='صـورة التقط',width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=570)
    window2.mainloop()
#=====================================================#
def open_new_window2():
    window1=Toplevel(window)
    window1.title("التـعليمــــات")
    #window1.geometry('400x490+0+110')
   # window1.configure(bg='#031634')
    window1.state('zoomed')
    window1.iconbitmap("images/m_icon.ico")
    pic=ImageTk.PhotoImage(Image.open("images/m4.jpg"))
    Label(window1,image=pic,bg='white').place(x=0,y=0)
    Button(window1,text="فهمت لقد",width=10,command=open_new_window3,font=('yu gothic ui',17,'bold'),activeforeground='white',fg='white',bd=3, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=10,y=600)
    window1.mainloop()
#=======================================================#
window.iconbitmap("images/m_icon.ico")
logo_image=ImageTk.PhotoImage(Image.open("images/m3 .jpg"))  
Label(window,image=logo_image,bg='white').place(x=0,y=0)
Button(window,text="الإختبــار بدا",width=10,command=open_new_window2,font=('yu gothic ui',13,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=1128,y=28)
Button(window,text="السابق الإختبار عرض",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=900,y=29)
Button(window,text="الـحســـاب حـذف",width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=680,y=28)
Button(window,text="المـرور كلمـة تغيير",command=open_new_window4,width=13,font=('yu gothic ui',12,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=450,y=28)

window.mainloop()