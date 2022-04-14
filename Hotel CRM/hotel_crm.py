from datetime import datetime
import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

root = Tk
current_user = 'STAFF'

#============= Initialize Database ===================
conn = sqlite3.connect('hotel_crm.db')
cur = conn.cursor()

def create_table_if_not_exist():
    admin_table = """ CREATE TABLE IF NOT EXISTS Admin_Details (
        id INTEGER PRIMARY KEY autoincrement,
        admin_username VARCHAR(255) NOT NULL,
        admin_password VARCHAR(255) NOT NULL
    )
    """
    staff_table = """ CREATE TABLE IF NOT EXISTS Staff_Details (
        id INTEGER PRIMARY KEY autoincrement,
        staff_name VARCHAR(255) NOT NULL,
        staff_extension VARCHAR(255) NOT NULL,
        staff_email VARCHAR(255) NOT NULL
    )
    """
    customer_table = """ CREATE TABLE IF NOT EXISTS Customer_Details (
        id INTEGER PRIMARY KEY autoincrement,
        first_name VARCHAR(255) NOT NULL,
        middle_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        contact_number VARCHAR(255) NOT NULL
        email VARCHAR(255) NOT NULL
        customer_address VARCHAR(255) NOT NULL,
        room_id VARCHAR(255) NOT NULL,
        transaction_datetime VARCHAR(255) NOT NULL
        payment_method VARCHAR(255) NOT NULL
    )
    """
    hotel_table = """ CREATE TABLE IF NOT EXISTS Hotel_Details (
        id INTEGER PRIMARY KEY autoincrement,
        total_rooms VARCHAR(255) NOT NULL,
        available_rooms VARCHAR(255) NOT NULL,
        total_customers VARCHAR(255) NOT NULL,
        total_staff VARCHAR(255) NOT NULL
    )
    """
    room_table = """ CREATE TABLE IF NOT EXISTS Room_Details (
        id INTEGER PRIMARY KEY autoincrement,
        beds VARCHAR(255) NOT NULL,
        ac VARCHAR(255) NOT NULL,
        tv VARCHAR(255) NOT NULL,
        wiFi VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL,
        room_status VARCHAR(255) NOT NULL
    )
    """
    cur.execute(admin_table)
    cur.execute(staff_table)
    cur.execute(customer_table)
    cur.execute(hotel_table)
    cur.execute(room_table)
    conn.commit()

# all_tables_are_created = cur.execute("SELECT * FROM sqlite_master where type='table'")
# print(all_tables_are_created)
# individual_table = [table for table in all_tables_are_created.fetchall()]
# print(individual_table)
print()
# if not all_tables_are_created:
#     print('tables not created')
#     # create_table_if_not_exist()


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(HotelCRM)

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
        self.bg_image = Label(self.master,image=self.bg,bg='#fff').place(x=240,y=35)
        Label(text='SERENITY HOTEL AND RESORTS',font='montserrat 36',bg='#fff',
              fg='orangered',bd=0).place(x=350,y=35)
        # ========== Display Sidebar ==============
        self.display_sidebar()
        # ========== Bigger Frames Hidden Until Clicked on ========================
        self.reservation_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)
        self.status_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)
        self.filter_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)
        self.rooms_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)
        self.contacts_frame = Frame(self.utils,borderwidth=2,relief='ridge',width=880,
                height=560,bg='cornsilk',bd=5)

        self.reservation_message = Label(self.reservation_frame,font='montserrat 16',bg='cornsilk')
        self.buttons = [self.reserve,self.status,self.contacts,self.rooms,self.filter]
        self.all_frames = [self.reservation_frame,self.status_frame,self.filter_frame,
            self.rooms_frame,self.contacts_frame,self.reservation_message]

        self.reservation_section()
        
    def display_sidebar(self):
        # =============== Side Bar =================
        self.status_img = Image.open('./images/hotelstatus.png')
        self.status_img = self.status_img.resize((50,50), Image.ANTIALIAS)
        self.status_img = ImageTk.PhotoImage(self.status_img)
        self.status = Button(image=self.status_img,command=self.status_section,text='  Status',
            width=280,fg='teal',font='montserrat 14',compound='left',bg='cornsilk')
        self.status.place(x=85,y=147)
        
        self.rooms_img = Image.open('./images/rooms.png')
        self.rooms_img = self.rooms_img.resize((50,50), Image.ANTIALIAS)
        self.rooms_img = ImageTk.PhotoImage(self.rooms_img)
        self.rooms = Button(image=self.rooms_img,command=self.rooms_section,text='  Rooms',
            width=280,fg='teal',font='montserrat 14',compound='left',bg='cornsilk')
        self.rooms.place(x=85,y=267)

        self.filter_img = Image.open('./images/payments.png')
        self.filter_img = self.filter_img.resize((50,50), Image.ANTIALIAS)
        self.filter_img = ImageTk.PhotoImage(self.filter_img)
        self.filter = Button(image=self.filter_img,command=self.filter_section,text='  Filter Rooms',
            width=280,fg='teal',font='montserrat 14',compound='left',bg='cornsilk')
        self.filter.place(x=85,y=387) 
        
        self.reserve_img = Image.open('./images/bookroom.png')
        self.reserve_img = self.reserve_img.resize((50,50), Image.ANTIALIAS)
        self.reserve_img = ImageTk.PhotoImage(self.reserve_img)
        self.reserve = Button(image=self.reserve_img,command=self.reservation_section,text='  Reservations',
            width=280,fg='teal',font='montserrat 14',compound='left',bg='cornsilk')
        self.reserve.place(x=85,y=507)
        
        self.contact_img = Image.open('./images/guests.png')
        self.contact_img = self.contact_img.resize((50,50), Image.ANTIALIAS)
        self.contact_img = ImageTk.PhotoImage(self.contact_img)
        self.contacts = Button(image=self.contact_img,command=self.contacts_section,text='  Contacts',
            width=280,fg='teal',font='montserrat 14',compound='left',bg='cornsilk')
        self.contacts.place(x=85,y=627)        

    def change_look(self, button):
        for but in self.buttons:
            but.config(fg='teal',bg='cornsilk',relief='groove')
        button.config(fg='#fff',bg='#dd4735',relief='ridge')
        
    def delete_frames(self):
        for frame in self.all_frames:
            frame.place_forget()
    
    def reservation_section(self):
        self.change_look(self.reserve)
        self.delete_frames()
        self.reservation_frame.place(x=365,y=15)
        
        # Label(self.reservation_frame,font='montserrat 24',bg='cornsilk',fg='teal',
        #     text='Reservation area').place(anchor=CENTER,relx=0.5,rely=0.05)
        reservation_form_frame = Frame(self.reservation_frame,width=750,height=450,relief='ridge',bg='cornsilk',bd=3)
        reservation_form_frame.place(x=60,y=50)
        
        Label(reservation_form_frame,font='montserrat 16',bg='cornsilk',fg='teal',
            text='Personal Information').place(x=27,y=10)
        self.first_name = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.first_name.insert(0, 'First Name *')
        self.first_name.place(x=27,y=60)
        self.middle_name = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.middle_name.insert(0, 'Middle Name *')
        self.middle_name.place(x=267,y=60)
        self.last_name = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.last_name.insert(0, 'Last Name *')
        self.last_name.place(x=507,y=60)
        
        Label(reservation_form_frame,font='montserrat 16',bg='cornsilk',fg='teal',
            text='Contact Information').place(x=27,y=100)
        self.contact_number = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.contact_number.insert(0, 'Phone No. *')
        self.contact_number.place(x=27,y=150)
        self.email = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.email.insert(0, 'Email *')
        self.email.place(x=267,y=150)
        self.address = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.address.insert(0, 'Address *')
        self.address.place(x=507,y=150)
        
        Label(reservation_form_frame,font='montserrat 16',bg='cornsilk',fg='teal',
            text='Reservation Information').place(x=27,y=190)
        self.children_number = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.children_number.insert(0, 'No. of Children *')
        self.children_number.place(x=27,y=240)
        self.adult_number = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.adult_number.insert(0, 'No. of Adults *')
        self.adult_number.place(x=267,y=240)
        self.days_number = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.days_number.insert(0, 'No. of Days *')
        self.days_number.place(x=507,y=240)
        
        Label(reservation_form_frame,font='montserrat 16',bg='cornsilk',fg='teal',
            text='Book Here').place(x=20,y=280)
        self.room_number = Entry(reservation_form_frame,bg='#dadada',fg='#222',font='montserrat 12',width=19)
        self.room_number.insert(0, 'Room No. *')
        self.room_number.place(x=27,y=330)
        combostyle = ttk.Style()
        combostyle.theme_use('winnative')
        self.pay_option = ttk.Combobox(reservation_form_frame,font='montserrat 12',
            values=['Payment Method...','Card','Cash'],state='readonly',width=17)
        self.pay_option.current(0)
        self.pay_option.place(x=267,y=330)
        
        Button(reservation_form_frame,command=self.reserve_it,width=57,text='Reserve',
            fg='#fff',bg='#dd4735',font='montserrat 14').place(anchor=CENTER,relx=0.5,rely=0.9)
        
        def entry_click(event):
            if self.first_name.get() == 'First Name *':
                self.first_name.delete(0, END)
                
        def entry_click2(event):
            if self.middle_name.get() == 'Middle Name *':
                self.middle_name.delete(0, END)
                
        def entry_click3(event):
            if self.last_name.get() == 'Last Name *':
                self.last_name.delete(0, END)

        def out_click(event):
            if self.first_name.get() == '':
                self.first_name.insert(0, 'First Name *')
                
        def out_click2(event):
            if self.middle_name.get() == '':
                self.middle_name.insert(0, 'Middle Name *')
                
        def out_click3(event):
            if self.last_name.get() == '':
                self.last_name.insert(0, 'Last Name *')
        
        def entry_click4(event):
            if self.contact_number.get() == 'Phone No. *':
                self.contact_number.delete(0, END)
                
        def entry_click5(event):
            if self.email.get() == 'Email *':
                self.email.delete(0, END)
                
        def entry_click6(event):
            if self.address.get() == 'Address *':
                self.address.delete(0, END)

        def out_click4(event):
            if self.contact_number.get() == '':
                self.contact_number.insert(0, 'Phone No. *')
                
        def out_click5(event):
            if self.email.get() == '':
                self.email.insert(0, 'Email *')
                
        def out_click6(event):
            if self.address.get() == '':
                self.address.insert(0, 'Address *')
          
        def entry_click7(event):
            if self.children_number.get() == 'No. of Children *':
                self.children_number.delete(0, END)
                
        def entry_click8(event):
            if self.adult_number.get() == 'No. of Adults *':
                self.adult_number.delete(0, END)
                
        def entry_click9(event):
            if self.days_number.get() == 'No. of Days *':
                self.days_number.delete(0, END)
                
        def entry_click10(event):
            if self.room_number.get() == 'Room No. *':
                self.room_number.delete(0, END)

        def out_click7(event):
            if self.children_number.get() == '':
                self.children_number.insert(0, 'No. of Children *')
                
        def out_click8(event):
            if self.adult_number.get() == '':
                self.adult_number.insert(0, 'No. of Adults *')
                
        def out_click9(event):
            if self.days_number.get() == '':
                self.days_number.insert(0, 'No. of Days *')
                
        def out_click10(event):
            if self.room_number.get() == '':
                self.room_number.insert(0, 'Room No. *')
                
        self.first_name.bind('<FocusIn>', entry_click)
        self.middle_name.bind('<FocusIn>', entry_click2)
        self.last_name.bind('<FocusIn>', entry_click3)
        self.first_name.bind('<FocusOut>', out_click)
        self.middle_name.bind('<FocusOut>', out_click2)
        self.last_name.bind('<FocusOut>', out_click3)

        self.contact_number.bind('<FocusIn>', entry_click4)
        self.email.bind('<FocusIn>', entry_click5)
        self.address.bind('<FocusIn>', entry_click6)
        self.contact_number.bind('<FocusOut>', out_click4)
        self.email.bind('<FocusOut>', out_click5)
        self.address.bind('<FocusOut>', out_click6)

        self.children_number.bind('<FocusIn>', entry_click7)
        self.adult_number.bind('<FocusIn>', entry_click8)
        self.days_number.bind('<FocusIn>', entry_click9)
        self.children_number.bind('<FocusOut>', out_click7)
        self.adult_number.bind('<FocusOut>', out_click8)
        self.days_number.bind('<FocusOut>', out_click9)

        self.room_number.bind('<FocusIn>', entry_click10)
        self.room_number.bind('<FocusOut>', out_click10)
        
    def reserve_it(self):
        f_name = self.first_name.get()
        m_name = self.middle_name.get()
        l_name = self.last_name.get()
        contact_no = self.contact_number.get()
        email = self.email.get()
        address = self.address.get()
        children_no = self.children_number.get()
        adult_no = self.adult_number.get()
        days_no = self.days_number.get()
        room_no = self.room_number.get()
        pay_meth = self.pay_option.get()
        
        # know_if_room_is_available = cur.execute(f"SELECT room_status from Room_Details where id='{room_no}'").fetchone()
        know_if_room_is_available = ['Available']
        
        if f_name in ['', 'First Name *'] or m_name in ['', 'Middle Name *'] or l_name in ['', 'Last Name *'] or\
            contact_no in ['Phone No. *'] or email in ['', 'Email *'] or address in ['', 'Address *'] or\
            children_no in ['', 'No. of Children *'] or adult_no in ['', 'No. of Adults *'] or\
            days_no in ['', 'No. of Days *'] or room_no in ['', 'Room No. *'] or pay_meth == 'Payment Method...':
            self.reservation_message.config(text='Please fill the form completely & correctly.',fg='red')
            self.reservation_message.place(anchor=CENTER,relx=0.5,rely=0.05)
        elif know_if_room_is_available[0] != 'Available':
            self.reservation_message.config(text='Room in use. Please choose another.',fg='red')
            self.reservation_message.place(anchor=CENTER,relx=0.5,rely=0.05)
        else:
            # cur.execute("INSERT INTO Customer_Details\
            #     (first_name,middle_name,last_name,contact_number,email,address,room_id,\
            #     transaction_datetime,payment_method) VALUES(?,?,?,?,?,?,?,?,?)",
            #     (f_name,m_name,l_name,contact_no,email,address,room_no,datetime.now(),pay_meth))
            # # Make the room unavailable in database
            # cur.execute("UPDATE Room_Details SET room_status=? WHERE id=?",
            #     ('Unavailable', room_no))
            # # Get no. of available rooms and decrement by 1
            # avail = cur.execute("SELECT available_rooms from Hotel_Details").fetchone()
            # value = int(avail[0]) - 1
            # cur.execute("UPDATE Hotel_Details SET available_rooms=?",
            #     (str(value)))
            # conn.commit()
            self.reservation_message.config(text='Room have been booked successfully.',fg='green')
            self.reservation_message.place(anchor=CENTER,relx=0.5,rely=0.05)
    
    def rooms_section(self):
        self.change_look(self.rooms)
        self.delete_frames()
        self.rooms_frame.place(x=365,y=15)
        # ======= Variables ==========
        hotel_rooms = 20
        x_coordinates = [67, 217, 367, 517, 667]
        y_coordinates = [20, 100, 180, 260]
        """set availabily from database"""
        from random import choice
        available_choice = ['available', 'busy']
        available = [choice(available_choice) for i in range(20)]
        # ======= Get rooms ==========
        button_count = 0
        for y_coord in y_coordinates:
            for x_coord in x_coordinates:
                if available[button_count] == "available":
                    button_count += 1
                    but = Button(self.rooms_frame,text=f'Room {button_count}',font='montserrat 16',fg='#fff',
                        bg='teal',width=9,relief='groove')
                else:
                    button_count += 1
                    but = Button(self.rooms_frame,text=f'Room {button_count}',font='montserrat 16',fg='#fff',
                        bg='#dd4735',width=9,relief='groove')
                but.config(command=lambda but=button_count: self.fetch_room_details(but))
                but.place(x=x_coord,y=y_coord)

        show_room_details = Frame(self.rooms_frame,width=750,height=200,relief='ridge',bg='cornsilk',bd=3)
        show_room_details.place(x=60,y=330)

        self.show_room_id = Label(show_room_details,bg='cornsilk',fg='#dd4735')
        self.show_bed = Label(show_room_details,font='montserrat 16',bg='cornsilk',fg='teal')
        self.show_ac = Label(show_room_details,font='montserrat 16',bg='cornsilk',fg='teal')
        self.show_tv = Label(show_room_details,font='montserrat 16',bg='cornsilk',fg='teal')
        self.show_wifi = Label(show_room_details,font='montserrat 16',bg='cornsilk',fg='teal')
        self.show_price = Label(show_room_details,bg='cornsilk',fg='teal')
        self.show_status = Label(show_room_details,font='montserrat 16',bg='cornsilk')
        self.show_unavailability = Label(show_room_details,font='montserrat 16',bg='cornsilk')
    
    def fetch_room_details(self, button):
        for label in [self.show_room_id, self.show_bed, self.show_ac, self.show_tv,
            self.show_wifi, self.show_price, self.show_status,self.show_unavailability]:
            label.place_forget()
        # Query database according to button press
        # data = cur.execute(f"SELECT * FROM Room_Details WHERE id='{button}'").fetchall()
        data = [['1','3',"YES", "YES","YES", '5000', "Available"],'another']
        room_id = data[0][0]
        no_of_beds = data[0][1]
        avail_ac = data[0][2]
        avail_tv = data[0][3]
        avail_wifi = data[0][4]
        room_price = data[0][5]
        # room_available = data[0][6]
        room_available = data[0][6]
        from random import choice
        available_choice = ['Available', 'busy']
        room_available = choice(available_choice)
        
        # if staff presses available button, show room details else show unavailable
        if room_available == 'Available':
            self.show_room_id.config(text=f'Room NO: {room_id}',font='montserrat 18 bold')
            self.show_room_id.place(x=40,y=30)
            self.show_bed.config(text=f'Bed(s): {no_of_beds}')
            self.show_bed.place(x=40,y=70)
            self.show_ac.config(text=f'AC: {avail_ac}')
            self.show_ac.place(x=240,y=70)
            self.show_tv.config(text=f'TV: {avail_tv}')
            self.show_tv.place(x=40,y=110)
            self.show_wifi.config(text=f'WiFi: {avail_wifi}')
            self.show_wifi.place(x=240,y=110)
            self.show_price.config(text=f'${room_price}',font='montserrat 42')
            self.show_price.place(x=435,y=60)
            # self.show_status.config(text=f'Available?: {room_available}',fg='green')
            # self.show_status.place(x=205,y=122)
        else:
            self.show_unavailability.config(text="Unavailable",font='montserrat 36',fg='#dd4735')
            self.show_unavailability.place(anchor=CENTER,relx=0.5,rely=0.5)
    
    def filter_section(self):
        self.change_look(self.filter)
        self.delete_frames()
        self.filter_frame.place(x=365,y=15)
        # ========= Filter form ===========
        filter_form_frame = Frame(self.filter_frame,width=750,height=260,relief='ridge',bg='cornsilk',bd=3)
        filter_form_frame.place(x=60,y=90)
        Label(filter_form_frame,font='montserrat 28',bg='cornsilk',fg='teal',
            text='Search Rooms by Preference').place(anchor=CENTER,relx=0.5,rely=0.15)

        Label(filter_form_frame,text='Bed(s):',font='montserrat 18',
            bg='cornsilk',fg='teal').place(x=50,y=70)
        self.bed_option = ttk.Combobox(filter_form_frame,font='montserrat 16',
            values=[' _ _'*8,'1','2','3'],state='readonly',width=12)
        self.bed_option.current(0)
        self.bed_option.place(x=150,y=76)
        
        Label(filter_form_frame,text='AC:',font='montserrat 18',
            bg='cornsilk',fg='teal').place(x=415,y=70)
        self.ac_option = ttk.Combobox(filter_form_frame,font='montserrat 16',
            values=[' _ _'*8,'YES','NO'],state='readonly',width=12)
        self.ac_option.current(0)
        self.ac_option.place(x=495,y=76)
        
        Label(filter_form_frame,text='TV:',font='montserrat 18',
            bg='cornsilk',fg='teal').place(x=95,y=125)
        self.tv_option = ttk.Combobox(filter_form_frame,font='montserrat 16',
            values=[' _ _'*8,'YES','NO'],state='readonly',width=12)
        self.tv_option.current(0)
        self.tv_option.place(x=150,y=131)
        
        Label(filter_form_frame,text='WiFi:',font='montserrat 18',
            bg='cornsilk',fg='teal').place(x=415,y=125)
        self.wifi_option = ttk.Combobox(filter_form_frame,font='montserrat 16',
            values=[' _ _'*8,'YES','NO'],state='readonly',width=12)
        self.wifi_option.current(0)
        self.wifi_option.place(x=495,y=131)
        
        Button(filter_form_frame,command=self.find_it,width=44,text='Search rooms',
            fg='#fff',bg='#dd4735',font='montserrat 16').place(anchor=CENTER,relx=0.5,rely=0.82)
    
    def find_it(self):
        bed = self.bed_option.get()
        ac = self.ac_option.get()
        tv = self.tv_option.get()
        wifi = self.wifi_option.get()
        # data = cur.execute(f"SELECT id, price FROM Room_Details WHERE room_status='Available'\
        #     and beds='{bed}' and tv='{tv}' and ac='{ac}' and wiFi='{wifi}' ").fetchall()
        
        # but = Label(self.filter_frame,text=f'No room match your search parameters...',font='montserrat 24',fg='#dd4735',
        #     bg='cornsilk')
        # but.place(anchor=CENTER,relx=0.5,rely=0.72)
        # but = Button(self.filter_frame,text=f'Room 3',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=63,y=370)
        # but = Button(self.filter_frame,text=f'Room 9',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=323,y=370)
        # but = Button(self.filter_frame,text=f'Room 15',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=583,y=370)
        # but = Button(self.filter_frame,text=f'Room 18',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=63,y=430)
        # but = Button(self.filter_frame,text=f'Room 19',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=323,y=430)
        # but = Button(self.filter_frame,text=f'Room 20',font='montserrat 16',fg='#fff',
        #     bg='teal',width=15,relief='groove')
        # but.place(x=583,y=430)
        
        x_coordinates = [63, 323, 583]
        y_coordinates = [370, 430]
        joined_coordinates = []
        for i in range(2):
            for x_coord in x_coordinates:
                for y_coord in y_coordinates:
                    pass
                joined_coordinates.append((x_coord, y_coordinates[i]))
        from random import sample
        bad = sample(range(1,21),4)
        data = [str(i) for i in bad]
        # data = []
        if data:
            for i in range(len(data)):
                but = Button(self.filter_frame,text=f'Room {data[i]}',font='montserrat 16',fg='#fff',
                    bg='teal',width=15,relief='groove')
                but.place(x=joined_coordinates[i][0],y=joined_coordinates[i][1])
        else:
            but = Label(self.filter_frame,text=f'No room match your search parameters...',font='montserrat 24',fg='#dd4735',
                bg='cornsilk')
            but.place(anchor=CENTER,relx=0.5,rely=0.72)
        
    def status_section(self):
        self.change_look(self.status)
        self.delete_frames()
        self.status_frame.place(x=365,y=15)
        
        total_rooms = 20
        available_rooms = 9
        total_customers = 0
        total_staff = 23
        
        Label(self.status_frame,text=f' Total rooms: {total_rooms} ',bg='cornsilk',fg='teal',
            font='montserrat 28',borderwidth=5,relief='groove').place(x=60,y=80)
        Label(self.status_frame,text=f' Available rooms: {available_rooms} ',bg='cornsilk',fg='teal',
            font='montserrat 28',borderwidth=5,relief='groove').place(x=60,y=190)
        Label(self.status_frame,text=f' Total number of customer: {total_customers} ',bg='cornsilk',fg='teal',
            font='montserrat 28',borderwidth=5,relief='groove').place(x=60,y=300)
        Label(self.status_frame,text=f' Total number of staff: {total_staff} ',bg='cornsilk',fg='teal',
            font='montserrat 28',borderwidth=5,relief='groove').place(x=60,y=410)
  
    def contacts_section(self):
        self.change_look(self.contacts)
        self.delete_frames()
        self.contacts_frame.place(x=365,y=15)
        #======= variables ===============
        manager_name = 'Mr. Tomiwa Joseph'
        manager_extension = '001'
        manager_email = 'tomiwajoseph88@gmail.com'
        
        chef_name = 'Mr. Clement Smith'
        chef_extension = '002'
        chef_email = 'clementsmith@gmail.com'
        
        room_service_name = 'Mrs. Jane Doe'
        room_service_extension = '003'
        room_service_email = 'janedoe@gmail.com'
        
        customer_service_name = 'Mrs. Mary Stone'
        customer_service_extension = '004'
        customer_service_email = 'marystone@gmail.com'
        
        #======= Manager ===============
        self.manager_img = Image.open('./images/newman.jpg')
        self.manager_img = self.manager_img.resize((80,90), Image.ANTIALIAS)
        self.manager_img = ImageTk.PhotoImage(self.manager_img)
        Label(self.contacts_frame,image=self.manager_img,bg='#fff',
            borderwidth=2,relief='ridge').place(x=60,y=140)
        manager_frame = Frame(self.contacts_frame,width=255,height=90,relief='ridge',bg='cornsilk',bd=0)
        manager_frame.place(anchor=CENTER,relx=0.335,rely=0.34)
        Label(manager_frame,text='Manager',bg='#fff',fg='#dd4735',
            font='montserrat 12 bold').place(x=0,y=0)
        Label(manager_frame,text=f'{manager_name}',bg='#fff',
            font='montserrat 10').place(x=0,y=25)
        Label(manager_frame,text=f'Extension: {manager_extension}',bg='#fff',
            font='montserrat 10').place(x=0,y=45)
        Label(manager_frame,text=f'Email: {manager_email}',bg='#fff',
            font='montserrat 10').place(x=0,y=65)
        
        #======= Restaurant ===================
        self.chef_img = Image.open('./images/chef.jpg')
        self.chef_img = self.chef_img.resize((80,90), Image.ANTIALIAS)
        self.chef_img = ImageTk.PhotoImage(self.chef_img)
        Label(self.contacts_frame,image=self.chef_img,bg='#fff',
            borderwidth=2,relief='ridge').place(x=440,y=140)
        restaurant_frame = Frame(self.contacts_frame,width=255,height=90,relief='ridge',bg='cornsilk',bd=0)
        restaurant_frame.place(anchor=CENTER,relx=0.77,rely=0.34)
        Label(restaurant_frame,text='Restaurant',bg='#fff',fg='#dd4735',
            font='montserrat 12 bold').place(x=0,y=0)
        Label(restaurant_frame,text=f'{chef_name}',bg='#fff',
            font='montserrat 10').place(x=0,y=25)
        Label(restaurant_frame,text=f'Extension: {chef_extension}',bg='#fff',
            font='montserrat 10').place(x=0,y=45)
        Label(restaurant_frame,text=f'Email: {chef_email}',bg='#fff',
            font='montserrat 10').place(x=0,y=65)

        #======= Room Service ===================
        self.room_img = Image.open('./images/roomservicenew.jpg')
        self.room_img = self.room_img.resize((80,90), Image.ANTIALIAS)
        self.room_img = ImageTk.PhotoImage(self.room_img)
        Label(self.contacts_frame,image=self.room_img,bg='#fff',
            borderwidth=2,relief='ridge').place(x=60,y=290)
        room_service_frame = Frame(self.contacts_frame,width=255,height=90,relief='ridge',bg='cornsilk',bd=0)
        room_service_frame.place(anchor=CENTER,relx=0.335,rely=0.61)
        Label(room_service_frame,text='Room Service',bg='#fff',fg='#dd4735',
            font='montserrat 12 bold').place(x=0,y=0)
        Label(room_service_frame,text=f'{room_service_name}',bg='#fff',
            font='montserrat 10').place(x=0,y=25)
        Label(room_service_frame,text=f'Extension: {room_service_extension}',bg='#fff',
            font='montserrat 10').place(x=0,y=45)
        Label(room_service_frame,text=f'Email: {room_service_email}',bg='#fff',
            font='montserrat 10').place(x=0,y=65)

        #======= Customer Service ===================
        self.customer_img = Image.open('./images/receptionnew.jpg')
        self.customer_img = self.customer_img.resize((80,90), Image.ANTIALIAS)
        self.customer_img = ImageTk.PhotoImage(self.customer_img)
        Label(self.contacts_frame,image=self.customer_img,bg='#fff',
            borderwidth=2,relief='ridge').place(x=440,y=290)
        customer_service_frame = Frame(self.contacts_frame,width=255,height=90,relief='ridge',bg='cornsilk',bd=0)
        customer_service_frame.place(anchor=CENTER,relx=0.77,rely=0.61)
        Label(customer_service_frame,text='Customer Service',bg='#fff',fg='#dd4735',
            font='montserrat 12 bold').place(x=0,y=0)
        Label(customer_service_frame,text=f'{customer_service_name}',bg='#fff',
            font='montserrat 10').place(x=0,y=25)
        Label(customer_service_frame,text=f'Extension: {customer_service_extension}',bg='#fff',
            font='montserrat 10').place(x=0,y=45)
        Label(customer_service_frame,text=f'Email: {customer_service_email}',bg='#fff',
            font='montserrat 10').place(x=0,y=65)



if __name__ == '__main__':
    app = Switch()
    app.state('zoomed')
    # app.attributes('-fullscreen', True)
    ico = Image.open('./images/hotel_logo.PNG')
    photo = ImageTk.PhotoImage(ico)
    app.wm_iconphoto(False, photo)
    app.mainloop()