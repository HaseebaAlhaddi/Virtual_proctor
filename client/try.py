from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
def view_start_exam_window():
    global subject_name,canvas_start_exam
    window4=Tk()
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
    Button(window4,text='صـورة التقط',width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=510)
    Button(window4,text='فتح الكاميرا',width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=450)
    Button(window4,text='ارسال',width=12,font=('yu gothic ui',14,'bold'),activeforeground='white',fg='white',bd=0, bg='#ff7f2f',cursor='hand2',activebackground='#ff7f2f').place(x=250,y=567)
    window4.mainloop()
view_start_exam_window()