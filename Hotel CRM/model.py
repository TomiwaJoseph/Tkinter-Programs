import sqlite3
import bcrypt


conn = sqlite3.connect('hotel_crm.db')
cur = conn.cursor()

admin_username = 'tommy'
password = 'a'

salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(bytes(password,'utf-8'), salt)

total_rooms = 20
available_rooms = 9
total_customers = 0
total_staff = 23

beds = 1
ac = "YES"
tv = "YES"
wiFi = "YES"
price = 3000
room_status = "AVAILABLE"

names = []
extension = []
email = []

cur.execute("INSERT INTO Admin_Details (admin_username,\
    admin_password) VALUES(?,?)",
    (admin_username,hashed))
cur.execute("INSERT INTO Hotel_Details (total_rooms,available_rooms,\
    total_customers,total_staff) VALUES(?,?,?,?)",
    (total_rooms,available_rooms,total_customers,total_staff))
for i in range(20):
    cur.execute("INSERT INTO Room_Details (beds,ac,tv,wiFi,\
        price,room_status) VALUES(?,?,?,?,?,?)",
        (beds,ac,tv,wiFi,price,room_status))
for i in range(4):
    cur.execute("INSERT INTO Staff_Details (staff_name,staff_extension,\
        staff_email) VALUES(?,?,?)",
        (names[i],extension[i],email[i]))


conn.commit()
print('done')
print()