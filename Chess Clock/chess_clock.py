from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound
import multiprocessing


# VARIABLES
root = Tk
player1_minutes = 0
player2_minutes = 0
prev_p1_min = 0
prev_p2_min = 0


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class StartPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#222')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('630x310')
        self.root.resizable(0,0)
        #======= Title =====================
        Label(self.master,text='Chess Clock',font='montserrat 40',fg='#505050',bg='#fff').place(x=150,y=83)
        Label(self.master,text='Chess Clock',font='montserrat 40',fg='#fff',bg='#222').place(x=150,y=80)
        #=========== Buttons ==================
        Button(self.master,text='Start',font='montserrat 18',bd=0,fg='yellow',bg='#222',command=lambda:self.master.switch_frame(SetTime)).place(x=280,y=150)


class SetTime(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#222')
        self.root = root
        self.root.title('Settings Page')
        self.root.geometry('630x310')
        self.root.resizable(0,0)
        #======== Variables ==========
        self.p1_mins = StringVar()
        self.p1_mins.set("3")
        self.p1_secs = StringVar()
        self.p1_secs.set("0")
        self.p2_mins = StringVar()
        self.p2_mins.set("3")
        self.p2_secs = StringVar()
        self.p2_secs.set("0")
        #============ UI =============
        Label(text="Player 1",font='poppins 16',bg='#222',fg='orange').place(x=90,y=58)
        Label(text='Mins:',font='montserrat 16',bg='#222',fg='white').place(x=230,y=58)
        self.p1_m = Entry(textvariable=self.p1_mins,width=4,font='montserrat 14',justify=CENTER)
        self.p1_m.place(x=300,y=60)
        Label(text='Secs:',font='montserrat 16',bg='#222',fg='white').place(x=380,y=58)
        self.p1_s = Entry(textvariable=self.p1_secs,width=4,font='montserrat 14',justify=CENTER)
        self.p1_s.place(x=450,y=60)

        Label(text="Player 2",font='poppins 16',bg='#222',fg='orange').place(x=90,y=128)
        Label(text='Mins:',font='montserrat 16',bg='#222',fg='white').place(x=230,y=128)
        self.p2_m = Entry(textvariable=self.p2_mins,width=4,font='montserrat 14',justify=CENTER)
        self.p2_m.place(x=300,y=130)
        Label(text='Secs:',font='montserrat 16',bg='#222',fg='white').place(x=380,y=128)
        self.p2_s = Entry(textvariable=self.p2_secs,width=4,font='montserrat 14',justify=CENTER)
        self.p2_s.place(x=450,y=130)

        Button(text='Start!',font='montserrat 14',bg='#222',fg='orange',width=34,
            command=self.go_without_time_set).place(x=90,y=190)

    def go_without_time_set(self):
        global player1_minutes,player2_minutes,prev_p1_min,prev_p2_min
        try:
            player1_mins = int(self.p1_mins.get())
            player1_secs = int(self.p1_secs.get())
            player2_mins = int(self.p2_mins.get())
            player2_secs = int(self.p2_secs.get())
            player1_minutes = player1_mins * 60 + player1_secs
            player2_minutes = player2_mins * 60 + player2_secs
            prev_p1_min = player1_minutes
            prev_p2_min = player2_minutes
            self.master.switch_frame(ClockIt)
        except ValueError:
            messagebox.showerror("Error", "One of the entry box is empty or an invalid value is entered in it. Please enter a number in the entry box.")


class ClockIt(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#222')
        self.root = root
        self.root.title('Chess Clock')
        self.root.geometry('630x310')
        self.root.resizable(0,0)
        #===== UI ===================
        self.status_img = Image.open('./static/flag.png')
        self.status_img = self.status_img.resize((70,70), Image.LANCZOS)
        self.status_img = ImageTk.PhotoImage(self.status_img)
        
        self.p1 = Button(command=lambda:self.know_player(self.p1),width=8,font='candara 48',bg='#222',fg='white')
        self.p1.place(x=30,y=60)
        self.p2 = Button(command=lambda:self.know_player(self.p2),width=8,font='candara 48',bg='#222',fg='white')
        self.p2.place(x=320,y=60)
        Button(text='Reset',font='montserrat 14',bg='#222',fg='orange',width=12,
            command=self.reset_it).place(x=70,y=210)
        Button(text='Pause',font='montserrat 14',bg='#222',fg='orange',width=12,
            command=self.pause_it).place(x=240,y=210)
        Button(text='Set Time',font='montserrat 14',bg='#222',fg='orange',width=12,
            command=lambda:self.master.switch_frame(SetTime)).place(x=410,y=210)
        
        self.flag_p1 = Button(image=self.status_img,text=' ',
            width=273,font='candara 48',compound='center',bg='#fff')
        self.flag_p2 = Button(image=self.status_img,text=' ',
            width=273,font='candara 48',compound='center',bg='#fff')
                        
        #========= Variables =========
        self.set_it()
        self.game_over = False
        self.p1_paused = True
        self.p2_paused = True

    def pause_it(self):
        self.p1_paused = False
        self.p2_paused = False
        self.sound_player.terminate()
        self.p1.config(state=NORMAL,bg='#222',fg='gray')
        self.p2.config(state=NORMAL,bg='#222',fg='gray')

    def reset_it(self):
        global player1_minutes,player2_minutes,prev_p1_min,prev_p2_min
        self.flag_p1.place_forget()
        self.flag_p2.place_forget()
        player1_minutes = prev_p1_min
        player2_minutes = prev_p2_min
        self.pause_it()
        self.set_it()

    def know_player(self, button):
        self.p1_paused, self.p2_paused = True, True
        if button == self.p1 and self.p1_paused and not self.game_over:
            self.p2_paused = True
            self.p2.config(state=NORMAL)
            self.count_down_2()
            self.p1.config(state=DISABLED)
            self.p1_paused = False
        if button == self.p2 and self.p2_paused and not self.game_over:
            self.p1_paused = True
            self.p1.config(state=NORMAL)
            self.count_down_1()
            self.p2.config(state=DISABLED)
            self.p2_paused = False

    def count_down_1(self):
        global player1_minutes
        if self.p1_paused == True:
            if player1_minutes > -1:
                mins, secs = divmod(player1_minutes,60)
                self.p1.config(text='{:02d}:{:02d}'.format(mins,secs),bg='#fff',fg='green')
                player1_minutes -= 1
                self.p1.after(1000,self.count_down_1)
            else:
                self.flag_p1.place(x=30,y=61)
                self.game_over = True
                self.sound_player = multiprocessing.Process(target=playsound, args=('./static/alarm.wav',))
                self.sound_player.start()
        else:
            self.p1.config(fg='white',bg='#222')

    def count_down_2(self):
        global player2_minutes
        if self.p2_paused == True:
            if player2_minutes > -1:
                mins, secs = divmod(player2_minutes,60)
                self.p2.config(text='{:02d}:{:02d}'.format(mins,secs),bg='#fff',fg='green')
                player2_minutes -= 1
                self.p2.after(1000,self.count_down_2)
            else:
                self.flag_p2.place(x=320,y=61)
                self.game_over = True
                self.sound_player = multiprocessing.Process(target=playsound, args=('./static/alarm.wav',))
                self.sound_player.start()
        else:
            self.p2.config(fg='white',bg='#222')

    def set_it(self):
        self.game_over = False
        mins, secs = divmod(player1_minutes,60)
        self.p1.config(text='{:02d}:{:02d}'.format(mins,secs),fg='#fff',bg='#222',state=NORMAL)
        mins, secs = divmod(player2_minutes,60)
        self.p2.config(text='{:02d}:{:02d}'.format(mins,secs),fg='#fff',bg='#222',state=NORMAL)


if __name__ == '__main__':
    app = Switch()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()