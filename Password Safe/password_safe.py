import bcrypt
from tkinter import *
from tkinter import ttk
import random, pyperclip
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
from tkinter.scrolledtext import ScrolledText

root = Tk
conn = sqlite3.connect('pass_safe.db')
cur = conn.cursor()
current_username = ""

secret_questions = (
    'Wealth or Peace of Mind?', 'Where did you meet your parents?',
    'Who is your musical GOAT?', 'What do you want most in life?'
)


def create_table():
    user_table = """ CREATE TABLE IF NOT EXISTS Users (
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        secret_question VARCHAR(255) NOT NULL,
        secret_answer VARCHAR(255) NOT NULL
    )
    """
    
    password_table = """ CREATE TABLE IF NOT EXISTS SavedPasswords (
        website VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        password_owner VARCHAR NOT NULL
    )
    """
    
    cur.execute(user_table)
    cur.execute(password_table)
    conn.commit()

create_table()

# GLOBAL FUNCTIONS

def about_app():
    newWindow = Toplevel()
    newWindow.title('About App')
    newWindow.config(bg='#222')
    newWindow.geometry('550x260')
    Label(newWindow,text='The app is a tool for saving your passwords.\
        \nUse as follows:\
        \nSign up or Login\
        \nPress the generate button to generate passwords\
        \nCopy the password that you like\
        \nPress paste and write the website used for\
        \nPress save\
        \nPress View Passwords to view your saved passwords.',fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))

def about_developer():
    newWindow = Toplevel()
    newWindow.title('About Developer')
    newWindow.config(bg='#222')
    newWindow.geometry('580x170')
    Label(newWindow,text='I am an experienced python desktop\n\
        application and web programmer!\
        \nFind more of my works at:',fg='#fff',bg='#222',font='montserrat 14').pack(pady=(20,5))
    the_github = Entry(newWindow,width=30, justify='center',font='montserrat 14')
    the_github.insert(0, "https://github.com/TomiwaJoseph")
    the_github.configure(fg='#fff',state="readonly",readonlybackground="#222")
    the_github.place(x=85,y=110)


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(Choose)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class Choose(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Log In | Sign Up')
        self.master.resizable(False,False)
        #===== MenuBars =========
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Help',menu=self.filemenu)
        self.filemenu.add_command(label='About App',command=about_app)
        self.filemenu.add_command(label='About Developer',command=about_developer)
        self.master.config(menu=self.menubar)
        #======= Bg Image ===============
        self.bg = Image.open(r'C:\Users\dretech\Documents\VS Python Stuff\Util Scripts\Tkinter Programs\Password Safe\bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #========== Box ============
        intro = Frame(self.master, width=400,height=250,bg='#dab88b')
        intro.place(x=150,y=90)
        #======= Title =====================
        Label(text='Password Safe',font='montserrat 30',bg='#0059ab').place(x=200,y=153)
        Label(text='Password Safe',font='montserrat 30',fg='#0059ab',bg='#dab88b').place(x=200,y=150)
        #=========== Buttons ==================
        Button(self.master,text='Log In',width=8,font='montserrat 14',bd=0,fg='#0059ab',bg='white',command=lambda:self.master.switch_frame(LogIn)).place(x=355,y=230)
        Button(self.master,text='Sign Up',width=8,font='montserrat 14',bd=0,fg='#0059ab',bg='white',command=lambda:self.master.switch_frame(SignUp)).place(x=240,y=230)


class SignUp(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Password Safe | Sign Up')
        self.master.resizable(False,False)
         #======= Bg Image ===============
        self.bg = Image.open(r'C:\Users\dretech\Documents\VS Python Stuff\Util Scripts\Tkinter Programs\Password Safe\bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #====== Variables =============
        self.username = StringVar()
        self.password = StringVar()
        self.secret = StringVar()
        self.secret_answer = StringVar()
        #====== Box ==========
        log = Frame(self.master,width=350,height=315,bg='#dab88b')
        log.place(x=190,y=70)
        #======== Title ================
        Label(text='Sign Up',font='candara 28 bold',fg='#0059ab',bg='#dab88b').place(x=210,y=70)
        underline = Frame(self.master,width=125,height=3,bg='#0059ab')
        underline.place(x=210,y=120)
        #======== UI ================
        Label(text='Username',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=125)
        self.useEnter = Entry(self.master,textvariable=self.username,font='calibri 12',bg='light gray',width=38)
        self.useEnter.place(x=210,y=155)
        Label(text='Password',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=185)
        self.pasEnter = Entry(self.master,textvariable=self.password,font='calibri 12',show='*',bg='light gray',width=38)
        self.pasEnter.place(x=210,y=215)
        Label(text='Secret Question',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=245)
        self.secret = ttk.Combobox(width=35,textvariable=self.secret,font='calibri 12')
        self.secret['values'] = secret_questions
        self.secret.place(x=210,y=275)
        Label(text='Answer',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=305)
        self.answer = Entry(self.master,textvariable=self.secret_answer,font='calibri 12',bg='light gray',width=38)
        self.answer.place(x=210,y=335)
        self.answer.bind('<Return>', lambda dummy=0: self.sign_it())
        self.sign = Button(text='Sign Up',command=self.sign_it,width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14')
        self.sign.place(x=310,y=370)
        Button(text='Log In',command=lambda:self.master.switch_frame(LogIn),width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14').place(x=10,y=398)
        self.flash = Label(text='Successfull Sign Up! Click Log In.', font='montserrat 14',bg='#dab88b',fg='green')

    def sign_it(self):
        username, password, secret_question, secret_answer = self.username.get(),self.password.get(),self.secret.get(),self.secret_answer.get()
        user = cur.execute(f"SELECT username FROM Users WHERE username='{username}'")
        check = [i[0] for i in user]
        if not all([username, password, secret_question, secret_answer]):
            self.flash.place(x=258,y=22)
            self.flash.config(text='Fill the form correctly!', font='montserrat 14',bg='cornsilk',fg='red')
        elif check:
            self.flash.place(x=218,y=22)
            self.flash.config(text='Username in use! Use another.', font='montserrat 14',bg='cornsilk',fg='red')
        else:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(bytes(password,'utf-8'), salt)
            cur.execute('INSERT INTO Users(username,password,secret_question,secret_answer) VALUES(?,?,?,?)',
                (username,hashed,secret_question,secret_answer))
            conn.commit()
            self.flash.place(x=208,y=22)
            self.flash.config(text='Successful Sign Up! Click Log In.', font='montserrat 14',bg='cornsilk',fg='green')
            self.secret.config(state=DISABLED)
            self.useEnter.config(state=DISABLED)
            self.pasEnter.config(state=DISABLED)
            self.answer.config(state=DISABLED)
            self.sign.config(state=DISABLED)


class LogIn(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Password Safe | Log In')
        self.master.resizable(False,False)
        #========= Variables ===========
        self.username = StringVar()
        self.password = StringVar()
        #======= Bg Image ===============
        self.bg = Image.open('bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #====== Box ==========
        log = Frame(self.master,width=350,height=250,bg='#dab88b')
        log.place(x=190,y=100)
        #======== Title ================
        Label(text='Log In',font='candara 28 bold',bg='#dab88b',fg='#0059ab').place(x=210,y=110)
        underline = Frame(self.master,width=110,height=3,bg='#0059ab')
        underline.place(x=210,y=160)
        #======== UI ================
        Label(text='Username',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=170)
        self.useEnter = Entry(self.master,textvariable=self.username,font='calibri 12',bg='light gray',width=38)
        self.useEnter.place(x=210,y=200)
        Label(text='Password',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=230)
        self.pasEnter = Entry(self.master,textvariable=self.password,font='calibri 12',show='*',bg='light gray',width=38)
        self.pasEnter.place(x=210,y=260)
        self.pasEnter.bind('<Return>', lambda dummy=0: self.LoginSystem())
        Button(text='forgot password?',cursor='hand1',bd=0,bg='#dab88b',fg='#0059ab',font='calibri 12',command=self.forgot_it).place(x=210,y=290)
        Button(text='Login',width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14',command=self.LoginSystem).place(x=310,y=330)
        Button(text='Sign Up',width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14',command=lambda:self.master.switch_frame(SignUp)).place(x=10,y=398)
        self.status = Label(text='Unsuccessful Login! Check your credentials.', font='montserrat 14',bg='cornsilk',fg='red')

    def LoginSystem(self):
        global current_username
        user_entry = self.username.get()
        pas_entry = self.password.get()
        user = cur.execute(f"SELECT username FROM Users WHERE username='{user_entry}'")
        username = [i[0] for i in user]
        passw = cur.execute(f"SELECT password FROM Users WHERE username='{user_entry}'")
        try:
            password = [i[0] for i in passw][0]
        except:
            self.status.place(x=155,y=40)
            self.useEnter.focus()
        if [user_entry] == username and bcrypt.checkpw(bytes(pas_entry,'utf-8'), password):
            a = cur.execute(f"SELECT username FROM Users WHERE username='{user_entry}'")
            current_username = [i[0] for i in a][0]
            self.master.switch_frame(MainPage)
        else:
            self.status.place(x=155,y=40)
            self.useEnter.focus()
    
    def forgot_it(self):
        self.master.switch_frame(ForgotPage)


class ForgotPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Password Safe | Forgot Password')
        self.master.resizable(False,False)
        #======= Bg Image ===============
        self.bg = Image.open('bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #====== Variables =============
        self.username = StringVar()
        self.password = StringVar()
        self.secret = StringVar()
        self.secret_answer = StringVar()
        #====== Box ==========
        log = Frame(self.master,width=350,height=300,bg='#dab88b')
        log.place(x=190,y=80)
        #======== Title ================
        self.recover_password = Label(text='Recover Password',font='candara 28 bold',fg='#0059ab',bg='#dab88b')
        self.recover_password.place(x=210,y=90)
        self.underline = Frame(self.master,width=300,height=3,bg='#0059ab')
        self.underline.place(x=210,y=140)
        #========== UI ===========
        self.usern = Label(text='Username',font='calibri 12 bold',bg='#dab88b',fg='#222')
        self.usern.place(x=210,y=150)
        self.user_name = Entry(self.master,textvariable=self.username,font='calibri 12',bg='#999',width=38)
        self.user_name.place(x=210,y=180)
        self.sec = Label(text='Secret Question',font='calibri 12 bold',bg='#dab88b',fg='#222')
        self.sec.place(x=210,y=205)
        self.secret = ttk.Combobox(width=35,textvariable=self.secret,font='calibri 12')
        self.secret['values'] = secret_questions
        self.secret.place(x=210,y=235)
        self.answ = Label(text='Answer',font='calibri 12 bold',bg='#dab88b',fg='#222')
        self.answ.place(x=210,y=260)
        self.answer = Entry(self.master,textvariable=self.secret_answer,font='calibri 12',bg='#999',width=38)
        self.answer.place(x=210,y=290)
        self.answer.bind('<Return>', lambda dummy=0: self.verify())
        self.check = Button(text='Check',command=self.verify,width=30,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14')
        self.check.place(x=210,y=325)
        Button(text='Log In',command=lambda:self.master.switch_frame(LogIn),width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14').place(x=10,y=398)
        self.flash = Label()
        
    def verify(self):
        global current_username
        username = self.username.get()
        secret_q_selected = self.secret.get()
        secret_answer = self.secret_answer.get()
        the_user = cur.execute(
            f"SELECT username FROM Users WHERE username='{username}'"
        )
        select_user = [i[0] for i in the_user]
        if select_user:
            user_question = cur.execute(
                f"SELECT secret_question FROM Users WHERE username='{select_user[0]}'"
            )
            select_question = [i[0] for i in user_question]
            if select_question[0] == secret_q_selected:
                user_answer = cur.execute(
                    f"SELECT secret_answer FROM Users WHERE username='{select_user[0]}'"
                )
                select_answer = [i[0] for i in user_answer]
                if select_answer[0] == secret_answer:
                    current_username = select_user[0]
                    #======= Show success message ===========
                    self.flash.place(x=135,y=32)
                    self.flash.config(text='Successful verification! Now update your details.', font='montserrat 14',bg='cornsilk',fg='green')
                    #===== Hide the queries widgets =============
                    self.recover_password.place_forget()
                    self.underline.place_forget()
                    self.usern.place_forget()
                    self.user_name.place_forget()
                    self.sec.place_forget()
                    self.secret.place_forget()
                    self.answ.place_forget()
                    self.answer.place_forget()
                    self.check.place_forget()
                    self.secret_answer.set('')
                    #======= Show the update widgets =========
                    self.recover_password = Label(text='Update Details',font='candara 28 bold',fg='#0059ab',bg='#dab88b')
                    self.recover_password.place(x=210,y=90)
                    self.underline = Frame(self.master,width=240,height=3,bg='#0059ab')
                    self.underline.place(x=210,y=140)
                    self.passw = Label(text='Password',font='calibri 12 bold',bg='#dab88b',fg='#222')
                    self.passw.place(x=210,y=150)
                    self.pass_word = Entry(self.master,textvariable=self.password,font='calibri 12',show="*",bg='#999',width=38)
                    self.pass_word.place(x=210,y=180)
                    self.sec = Label(text='Secret Question',font='calibri 12 bold',bg='#dab88b',fg='#222')
                    self.sec.place(x=210,y=205)
                    self.secret = ttk.Combobox(width=35,textvariable=self.secret,font='calibri 12')
                    self.secret['values'] = secret_questions
                    self.secret.place(x=210,y=235)
                    self.answ = Label(text='Answer',font='calibri 12 bold',bg='#dab88b',fg='#222')
                    self.answ.place(x=210,y=260)
                    self.answer = Entry(self.master,textvariable=self.secret_answer,font='calibri 12',bg='#999',width=38)
                    self.answer.place(x=210,y=290)
                    self.answer.bind('<Return>', lambda dummy=0: self.update_details())                    
                    self.update_btn = Button(text='Update',command=self.update_details,width=30,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14')
                    self.update_btn.place(x=210,y=325)
                else:
                    self.flash.place(x=255,y=32)
                    self.flash.config(text='Invalid details! Be sure.', font='montserrat 14',bg='cornsilk',fg='red')
            else:
                self.flash.place(x=255,y=32)
                self.flash.config(text='Invalid details! Be sure.', font='montserrat 14',bg='cornsilk',fg='red')
        else:
            self.flash.place(x=255,y=32)
            self.flash.config(text='Invalid details! Be sure.', font='montserrat 14',bg='cornsilk',fg='red')
        
    def update_details(self):
        global current_username
        password, secret_question, secret_answer = self.password.get(),self.secret.get(),self.secret_answer.get()
        if not all([password, secret_question, secret_answer]):
            self.flash.place(x=258,y=32)
            self.flash.config(text='Fill the form correctly!', font='montserrat 14',bg='cornsilk',fg='red')
        else:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(bytes(password,'utf-8'), salt)
            cur.execute("UPDATE Users SET password=?,secret_question=?,secret_answer=? WHERE username=?",
                (hashed,secret_question,secret_answer,current_username))
            conn.commit()
            self.flash.place(x=180,y=32)
            self.flash.config(text='Successful details change! Click Log In.', font='montserrat 14',bg='cornsilk',fg='green')
            self.pass_word.config(state=DISABLED)
            self.secret.config(state=DISABLED)
            self.answer.config(state=DISABLED)
            self.update_btn.config(state=DISABLED)
        
        
class MainPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Password Safe')
        self.master.resizable(0,0)
        self.password_variable = StringVar()
        self.website_variable = StringVar()
        #===== MenuBars =========
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Help',menu=self.filemenu)
        self.filemenu.add_command(label='About App',command=about_app)
        self.filemenu.add_command(label='About Developer',command=about_developer)
        self.master.config(menu=self.menubar)
        #======= Bg Image ===============
        self.bg = Image.open('bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #================= Create and Save Frame ======================
        self.CreateFrame = Frame(self.master,width=300,height=360,relief='ridge',bg='#dab88b',bd=5)
        self.CreateFrame.place(x=30,y=60)
        self.SaveFrame = Frame(self.master,width=300,height=360,relief='ridge',bg='#dab88b',bd=5)
        self.SaveFrame.place(x=370,y=60)
        #=================================== Frames ==================================================
        self.createLabel = Label(self.master,text=' '*10+'Create'+' '*10,bd=5,relief="ridge",font='poppins 16',bg='#dab88b',fg='#0059ab').place(x=75,y=43)
        self.createLabel = Label(self.master,text=' '*10+'Save'+' '*10,bd=5,relief="ridge",font='poppins 16',bg='#dab88b',fg='#0059ab').place(x=430,y=43)
        # self.saveLabel = Label(self.master,text='Save',font='poppins 14',bg='#dab88b',fg='#0059ab').place(x=600,y=45)
        #================ Password Labels =================================
        self.pass1 = Label(self.CreateFrame,text='password123456',bg='#dab88b',fg='#0059ab',font='montserrat 15')
        self.pass1.place(x=10,y=45)
        self.pass2 = Label(self.CreateFrame,text='password123456',bg='#dab88b',fg='#0059ab',font='montserrat 15')
        self.pass2.place(x=10,y=95)
        self.pass3 = Label(self.CreateFrame,text='password123456',bg='#dab88b',fg='#0059ab',font='montserrat 15')
        self.pass3.place(x=10,y=145)
        self.pass4 = Label(self.CreateFrame,text='password123456',bg='#dab88b',fg='#0059ab',font='montserrat 15')
        self.pass4.place(x=10,y=195)
        self.pass5 = Label(self.CreateFrame,text='password123456',bg='#dab88b',fg='#0059ab',font='montserrat 15')
        self.pass5.place(x=10,y=245)
        #============================ Copy Buttons & Generate =============================
        self.copy1 = Button(self.CreateFrame,fg='#d77337',text='copy',font='montserrat 12',command=self.copy_function).place(x=225,y=45)
        self.copy2 = Button(self.CreateFrame,fg='#d77337',text='copy',font='montserrat 12',command=self.copy_function2).place(x=225,y=95)
        self.copy3 = Button(self.CreateFrame,fg='#d77337',text='copy',font='montserrat 12',command=self.copy_function3).place(x=225,y=145)
        self.copy4 = Button(self.CreateFrame,fg='#d77337',text='copy',font='montserrat 12',command=self.copy_function4).place(x=225,y=195)
        self.copy5 = Button(self.CreateFrame,fg='#d77337',text='copy',font='montserrat 12',command=self.copy_function5).place(x=225,y=245)
        self.generate = Button(self.CreateFrame,cursor='hand1',fg='cornsilk',bg='#d77337',text='Generate',font='montserrat 14',
            width=21,command=self.generate_password).place(x=11,y=295)
        #=========================== Entry, Clear, Save, View & Quit ========================
        Label(self.SaveFrame,text='Password',bg='#dab88b',fg='#0059ab',font='montserrat 14').place(x=10,y=35)
        self.passEntry = Entry(self.SaveFrame,bg='light gray',textvariable=self.password_variable,font='montserrat 14',width=20)
        self.passEntry.place(x=10,y=70)
        Label(self.SaveFrame,text='Website',bg='#dab88b',fg='#0059ab',font='montserrat 14').place(x=10,y=160)
        self.webEntry = Entry(self.SaveFrame,bg='light gray',textvariable=self.website_variable,font='montserrat 14',width=20)
        self.webEntry.place(x=10,y=195)
        self.clear_it = Button(self.SaveFrame,text='clear',fg='#d77337',width=12,font='montserrat 12',command=self.clear_function)
        self.clear_it.place(x=10,y=110)
        self.paste_it = Button(self.SaveFrame,text='paste',fg='#d77337',width=12,font='montserrat 12',command=self.paste_function)
        self.paste_it.place(x=145,y=110)
        Button(self.SaveFrame,cursor='hand1',fg='cornsilk',bg='#d77337',text='Save',width=21,font='montserrat 14',command=self.save_function).place(x=10,y=235)
        Button(self.SaveFrame,cursor='hand1',fg='cornsilk',bg='#0059ab',text='View Passwords',font='montserrat 12',command=lambda:self.master.switch_frame(ViewPage)).place(x=10,y=300)
        Button(self.SaveFrame,cursor='hand1',fg='cornsilk',bg='#0059ab',text='Logout',width=10,font='montserrat 12',command=self.log_out).place(x=160,y=300)
        self.flash = Label()
        
    def generate_password(self):
        for lab in [self.pass1,self.pass2,self.pass3,self.pass4,self.pass5]:
            aa = [chr(i) for i in range(48,65)]
            alpha_Cap = [chr(i) for i in range(65,91)]
            alpha_Small = [chr(i) for i in range(97,123)]
            a,b,c = random.sample(aa,4),random.sample(alpha_Cap,5),random.sample(alpha_Small,5)
            d = a+b+c
            random.shuffle(d)
            lab.config(text='{}'.format(''.join(d)))
        
    def copy_function(self):
        gen = self.pass1['text']
        pyperclip.copy(gen)
        
    def copy_function2(self):
        gen = self.pass2['text']
        pyperclip.copy(gen)
        
    def copy_function3(self):
        gen = self.pass3['text']
        pyperclip.copy(gen)
        
    def copy_function4(self):
        gen = self.pass4['text']
        pyperclip.copy(gen)
        
    def copy_function5(self):
        gen = self.pass5['text']
        pyperclip.copy(gen)
        
    def paste_function(self):
        self.passEntry.event_generate('<<Paste>>')
        self.webEntry.focus()
        
    def clear_function(self):
        self.password_variable.set('')
        self.passEntry.focus()
        
    def save_function(self):
        password = self.password_variable.get()
        website = self.website_variable.get()
        if not all([password,website]):
            self.flash.config(text='Save unsuccessful. Fill spaces properly.',font='montserrat 14',bg='cornsilk',fg='red')
            self.flash.place(x=180,y=6)
        else:
            cur.execute('INSERT INTO SavedPasswords(website,password,password_owner) VALUES(?,?,?)',
                (website,password,current_username))            
            conn.commit()
            self.password_variable.set('')
            self.website_variable.set('')
            self.flash.config(text='Password saved successfully!', font='montserrat 14',bg='cornsilk',fg='green')
            self.flash.place(x=210,y=6)
        
    def log_out(self):
        global current_username
        current_username = ""
        self.master.switch_frame(LogIn)


class ViewPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry('700x450')
        self.master.title('Password Safe | Forgot Password')
        self.master.resizable(False,False)
        #======= Bg Image ===============
        self.bg = Image.open('bcg.jpg')
        self.bg = self.bg.resize((700,450), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #======= UI =============
        self.views_ = ScrolledText(height=15,width=45,font='montserrat 12')
        self.views_.place(x=120,y=40)
        Button(text='Go back',command=lambda:self.master.switch_frame(MainPage),width=10,cursor='hand1',fg='white',bg='#0059ab',font='calibri 14').place(x=10,y=398)
        self.populate()
        
    def populate(self):
        saved = conn.execute(f"SELECT password, website FROM SavedPasswords WHERE password_owner='{current_username}'")
        self.views_.insert(END, '\n' + ' ' * 5 + 'Password' + ' '*15 + '|' + ' '*15 + 'Website' + '\n')
        self.views_.insert(END, ' ' * 5 + '_ ' * 30 + "\n")
        
        for password, website in saved:
            self.views_.insert(END, '\n' + ' ' * 5 + f'{password}' + ' '*5 + '|' + ' '*5 + f'{website}' + '\n')
        self.views_.insert(END, ' ' * 5 + '_ ' * 30 + "\n")

        
if __name__ == "__main__":
    app = Switch()
    # app.eval('tk::PlaceWindow . center')
    app.mainloop()