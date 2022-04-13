from datetime import datetime
import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk
current_user = 'STAFF'

#============= Initialize Database ===================
conn = sqlite3.connect('hotel.db')
cur = conn.cursor()

class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(AdminLogin)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class StartPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#fff')
        self.root = root
        self.root.title('Serenity Hotel')
        #======= Bg Image ===============
        # self.bg = Image.open('./images/logo.jpg')
        # self.bg = self.bg.resize((1366,768), Image.ANTIALIAS)
        # self.bg = ImageTk.PhotoImage(self.bg)
        # self.bg_image = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        #======= Hotel Logo ===============
        self.bcg = Image.open('./images/hotel_logo.PNG')
        self.bcg = self.bcg.resize((120,100), Image.ANTIALIAS)
        self.bcg = ImageTk.PhotoImage(self.bcg)
        self.bcg_image = Label(self.master,image=self.bcg,bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.38)
        # ======= Hotel Name =====================
        Label(self.master,text='SERENITY',font='garamond 40',fg='#505050',bg='teal').place(anchor=CENTER,relx=0.5,rely=0.483)
        Label(self.master,text='SERENITY',font='garamond 40',fg='teal',bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.48)
        Label(self.master,text='HOTEL AND RESORTS',font='montserrat 16',fg='orangered',bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.56)
        #=========== Buttons ==================
        self.admin_button = Button(self.master,text='ADMIN',font='montserrat 14',bd=0,width=15,fg='white',bg='teal',
            command=lambda:self.master.switch_frame(AdminLogin))
        self.admin_button.place(x=45,y=680)
        self.staff_button = Button(self.master,text='STAFF',font='montserrat 14',bd=0,width=15,fg='white',bg='teal',
            command=lambda:self.master.switch_frame(HotelCRM))
        self.staff_button.place(x=1135,y=680)


class AdminLogin(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#fff')
        self.root = root
        self.root.title('Serenity Hotel Admin Login')
        #======= Hotel Logo ===============
        self.bcg = Image.open('./images/hotel_logo.PNG')
        self.bcg = self.bcg.resize((120,100), Image.ANTIALIAS)
        self.bcg = ImageTk.PhotoImage(self.bcg)
        self.bcg_image = Label(self.master,image=self.bcg,bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.36)
        # ======= Hotel Name =====================
        Label(self.master,text='SERENITY',font='garamond 40',fg='#505050',bg='teal').place(anchor=CENTER,relx=0.5,rely=0.463)
        Label(self.master,text='SERENITY',font='garamond 40',fg='teal',bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.46)
        Label(self.master,text='HOTEL AND RESORTS',font='montserrat 16',fg='orangered',bg='#fff').place(anchor=CENTER,relx=0.5,rely=0.54)
        #====== Variables =============
        self.username = StringVar()
        self.password = StringVar()
        #======== UI ================
        # Label(text='Username',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=125)
        self.useEnter = Entry(self.master,textvariable=self.username,font='calibri 18',bg='teal',
            justify=CENTER,width=25,fg='#fff')
        self.useEnter.place(anchor=CENTER,relx=0.5,rely=0.6)
        # Label(text='Password',font='calibri 12 bold',bg='#dab88b',fg='#222').place(x=210,y=185)
        self.pasEnter = Entry(self.master,textvariable=self.password,font='calibri 18',show='*',bg='teal',
            justify=CENTER,width=25,fg='#fff')
        self.pasEnter.place(anchor=CENTER,relx=0.5,rely=0.67)
        self.pasEnter.bind('<Return>', lambda dummy=0: self.check_credentials())
        self.go_back_button = Button(self.master,text='GO BACK',font='montserrat 14',bd=0,width=15,fg='white',bg='teal',
            command=lambda:self.master.switch_frame(StartPage))
        self.go_back_button.place(x=45,y=680)
        
    def check_credentials(self):
        username, password = self.username.get(), self.password
        # user = cur.execute(f"SELECT username FROM AdminUsers WHERE username='{username}'")
        # check = [i[0] for i in user]
        # passw = cur.execute(f"SELECT password FROM Users WHERE username='{user_entry}'")
        print('enter db to find out...')


class AdminHotelCRM(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#fff')
        self.root = root
        self.root.title('Serenity Hotel Admin')


class HotelCRM(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#fff')
        self.root = root
        self.root.title('Serenity Hotel Management System')
        # =========== Top Bar ==========
        self.hotel_name_frame = Frame(self.master,width=1300,height=80,relief='ridge',bg='#fff',bd=5)
        self.hotel_name_frame.place(anchor=CENTER,relx=0.5,rely=0.09)
        self.utils = Frame(self.master,width=1300,height=600,relief='ridge',bg='#fff',bd=5)
        self.utils.place(anchor=CENTER,relx=0.5,rely=0.56)
        #======= Hotel Logo ===============
        self.bg = Image.open('./images/hotel_logo.PNG')
        self.bg = self.bg.resize((80,60), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.master,image=self.bg,bg='#fff').place(x=240,y=33)
        Label(text='SERENITY HOTEL AND RESORTS',font='montserrat 36',bg='#fff',
              fg='orangered',bd=0).place(x=350,y=33)
        # ========== Display Sidebar ==============
        self.display_sidebar()
        # ========== Bigger Frames Hidden Until Clicked on ========================
        self.reservation_frame = Frame(borderwidth=2,relief='ridge',width=650,height=550,bg='cornsilk')
        self.status_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)
        self.filter_frame = Frame(borderwidth=2,relief='ridge',width=580,height=530,bg='cornsilk')
        self.rooms_frame = Frame(borderwidth=2,relief='ridge',width=580,height=530,bg='cornsilk')
        self.contacts_frame = Frame(borderwidth=2,relief='ridge',width=580,height=530,bg='cornsilk')

        self.reserve_flash = Label(self.reservation_frame,font='montserrat 18',bg='cornsilk')
        self.buttons = [self.status]
        # self.buttons = [self.reserve,self.status,self.contacts,self.rooms,self.filter]
        self.all_frames = [self.reservation_frame,self.status_frame,self.filter_frame,
            self.rooms_frame,self.contacts_frame,self.reserve_flash]

        self.status_section()
        
    def display_sidebar(self):
        # =============== Side Bar =================
        self.status_img = Image.open('./images/hotelstatus.png')
        self.status_img = self.status_img.resize((50,50), Image.ANTIALIAS)
        self.status_img = ImageTk.PhotoImage(self.status_img)
        self.status = Button(image=self.status_img,command=self.status_section,text='  Status',
            width=280,fg='teal',font='montserrat 12',compound='left',bg='cornsilk')
        self.status.place(x=75,y=140)
        
        # self.rooms_img = Image.open('./images/rooms.png')
        # self.rooms_img = self.rooms_img.resize((50,50), Image.ANTIALIAS)
        # self.rooms_img = ImageTk.PhotoImage(self.rooms_img)
        # self.rooms = Button(image=self.rooms_img,command=self.rooms_section,text='  Rooms',
        #     width=180,fg='teal',font='montserrat 12',compound='left',bg='cornsilk')
        # self.rooms.place(x=12,y=140)

        # self.filter_img = Image.open('./images/payments.png')
        # self.filter_img = self.filter_img.resize((50,50), Image.ANTIALIAS)
        # self.filter_img = ImageTk.PhotoImage(self.filter_img)
        # self.filter = Button(image=self.filter_img,command=self.filter_section,text='  Filter Rooms',
        #     width=180,fg='teal',font='montserrat 12',compound='left',bg='cornsilk')
        # self.filter.place(x=12,y=240) 
        
        # self.reserve_img = Image.open('./images/bookroom.png')
        # self.reserve_img = self.reserve_img.resize((50,50), Image.ANTIALIAS)
        # self.reserve_img = ImageTk.PhotoImage(self.reserve_img)
        # self.reserve = Button(image=self.reserve_img,command=self.reservation_section,text='  Reservations',
        #     width=180,fg='teal',font='montserrat 12',compound='left',bg='cornsilk')
        # self.reserve.place(x=12,y=340)

        # self.contact_img = Image.open('./images/guests.png')
        # self.contact_img = self.contact_img.resize((50,50), Image.ANTIALIAS)
        # self.contact_img = ImageTk.PhotoImage(self.contact_img)
        # self.contacts = Button(image=self.contact_img,command=self.contacts_section,text='  Contacts',
        #     width=180,fg='teal',font='montserrat 12',compound='left',bg='cornsilk')
        # self.contacts.place(x=12,y=440)
    
    def change_look(self, button):
        for but in self.buttons:
            but.config(fg='teal',bg='cornsilk',relief='groove')
        button.config(fg='#fff',bg='teal',relief='ridge')
        
    def delete_frames(self):
        for frame in self.all_frames:
            frame.place_forget()
    
    def reservation_section(self):
        self.change_look(self.reserve)
        self.delete_frames()
        self.reservation_frame.place(x=310,y=10)
    
    def status_section(self):
        self.change_look(self.status)
        self.delete_frames()
        self.status_frame.place(x=360,y=15)
    
    def rooms_section(self):
        self.change_look(self.rooms)
        self.delete_frames()
        self.rooms_frame.place(x=210,y=10)
    
    def room_details(self, button):
        pass
    
    def filter_section(self):
        self.change_look(self.filter)
        self.delete_frames()
        self.filter_frame.place(x=210,y=10)
    
    def find_it(self):
        pass
    
    def contacts_section(self):
        self.change_look(self.contacts)
        self.delete_frames()
        self.contacts_frame.place(x=210,y=10)
    



if __name__ == '__main__':
    app = Switch()
    app.state('zoomed')
    ico = Image.open('./images/hotel_logo.PNG')
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)
    app.mainloop()