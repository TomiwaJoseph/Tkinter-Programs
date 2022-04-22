import sqlite3
import bcrypt
from random import choice
import names as rand_names
from datetime import datetime, timedelta


conn = sqlite3.connect('hotel_crm.db')
cur = conn.cursor()

admin_username = 'tommy'
password = 'a'

salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(bytes(password,'utf-8'), salt)

total_rooms = 20
available_rooms = 9
total_customers = 35
total_staff = 23

all_bed = [1, 2, 3]
beds = [choice(all_bed) for i in range(20)]
all_ac = ["YES", "NO"]
ac = [choice(all_ac) for i in range(20)]
all_tv = ["YES", "NO"]
tv = [choice(all_tv) for i in range(20)]
all_wiFi = ["YES", "NO"]
wiFi = [choice(all_wiFi) for i in range(20)]
all_price = [2000, 2500, 3000]
price = [choice(all_price) for i in range(20)]
all_status = ["UNAVAILABLE", "AVAILABLE"]
room_status = [choice(all_status) for i in range(20)]

names = ['Mr. Tomiwa Joseph', 'Mr. Clement Smith', 'Mrs. Jane Doe', 'Mrs. Mary Stone']
extensions = ['001', '002', '003', '004']
emails = ['tomiwajoseph88@gmail.com', 'clementsmith@gmail.com',
          'janedoe@gmail.com', 'marystone@gmail.com']

customer_first_name = [rand_names.get_first_name() for i in range(11)]
customer_middle_name = [rand_names.get_last_name() for i in range(11)]
customer_last_name = [rand_names.get_first_name() for i in range(11)]
customer_contact_number = '+789 123456789'
customer_email = [customer_first_name[i].lower()+customer_last_name[i].lower()+'@gmail.com' 
                  for i in range(11)]
customer_customer_address = [f'13, Some Address, {customer_first_name[i]} Avenue' 
                             for i in range(11)]
customer_room_id = []
while len(customer_room_id) != 11:
    id = [i for i in range(1,21)]
    choosen = choice(id)
    if choosen not in customer_room_id:
        customer_room_id.append(choosen)
customer_transaction_datetime = []
customer_expiry_datetime = []
for i in range(1,12):
    the_time = datetime.now()
    formatted_time = f'{the_time.year}/{the_time.month}/{the_time.day} {the_time.hour}:{the_time.minute}:{the_time.second}'
    customer_transaction_datetime.append(formatted_time)
for i in range(1,12):
    the_time = datetime.now() + timedelta(days=i)
    formatted_time = f'{the_time.year}/{the_time.month}/{the_time.day} {the_time.hour}:{the_time.minute}:{the_time.second}'
    customer_expiry_datetime.append(formatted_time)
methods = ['card', 'cash']
customer_payment_method = [choice(methods) for i in range(11)]
time_now = datetime.now()
time_now = f'{time_now.year}/{time_now.month}/{time_now.day} {time_now.hour}:{time_now.minute}:{time_now.second}'


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
        contact_number VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        customer_address VARCHAR(255) NOT NULL,
        room_id VARCHAR(255) NOT NULL,
        payment_method VARCHAR(255) NOT NULL,
        transaction_datetime VARCHAR(255) NOT NULL,
        expiry_datetime VARCHAR(255) NOT NULL
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

all_tables_are_created = cur.execute("SELECT name FROM sqlite_master where type='table'")

if not all_tables_are_created.fetchall():
    create_table_if_not_exist()

    cur.execute("INSERT INTO Admin_Details (admin_username,\
        admin_password) VALUES(?,?)",
        (admin_username,hashed))
    for i in range(4):
        cur.execute("INSERT INTO Staff_Details (staff_name,staff_extension,\
            staff_email) VALUES(?,?,?)",
            (names[i],extensions[i],emails[i]))
    for i in range(11):
        cur.execute("INSERT INTO Customer_Details (first_name,middle_name,last_name,contact_number,\
            email,customer_address,room_id,payment_method,transaction_datetime,expiry_datetime) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (customer_first_name[i],customer_middle_name[i],customer_last_name[i],
             customer_contact_number,customer_email[i],customer_customer_address[i],
             customer_room_id[i],customer_payment_method[i],customer_transaction_datetime[i],
             customer_expiry_datetime[i]))
    cur.execute("INSERT INTO Hotel_Details (total_rooms,available_rooms,\
        total_customers,total_staff) VALUES(?,?,?,?)",
        (total_rooms,available_rooms,total_customers,total_staff))
    for i in range(20):
        cur.execute("INSERT INTO Room_Details (beds,ac,tv,wiFi,\
            price,room_status) VALUES(?,?,?,?,?,?)",
            (beds[i],ac[i],tv[i],wiFi[i],price[i],room_status[i]))

    conn.commit()

print('data inserted')
print()