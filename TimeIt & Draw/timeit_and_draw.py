import tkinter as tk
from tkinter import *
from random import shuffle
from threading import Timer
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilenames


root = Tk
PICTURES_TO_DRAW = []
SESSION_TIMING = 0
SHUFFLE = False


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
        self._frame.place(x=0, y=0, relheight=1, relwidth=1)


class StartPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#143d59')
        self.root = root
        self.root.title('Time It & Draw')
        self.root.geometry('500x400+433+184')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text="Time It & Draw", font='raleway 40',
              fg='#505050', bg='#f4b41a').place(relx=0.5, rely=0.445, anchor=CENTER)
        Label(self.master, text="Time It & Draw", font='raleway 40',
              fg='#f4b41a', bg='#143d59').place(relx=0.5, rely=0.44, anchor=CENTER)
        # ======= SHOW STARTPAGE FOR 3 ONLY SECONDS =====================
        r = Timer(3.0, lambda: self.master.switch_frame(SettingsPage))
        r.start()


class SettingsPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#143d59')
        self.root = root
        self.root.geometry('500x550+433+109')
        self.root.title('Settings')
        self.root.resizable(0, 0)
        # ======= Variables ===========
        self.time = IntVar()
        self.shuffle_or_not = IntVar()
        self.custom_time = StringVar()
        # =========== Frames ===============
        self.select_picture_frame = Frame(
            self.master, width=380, height=150, relief='ridge', bg='#143d59', bd=3)
        self.select_picture_frame.place(anchor=CENTER, relx=0.5, rely=0.2)
        self.select_time_frame = Frame(
            self.master, width=380, height=220, relief='ridge', bg='#143d59', bd=3)
        self.select_time_frame.place(anchor=CENTER, relx=0.5, rely=0.6)
        # =========== Picture Frame Insides ===============
        self.pictures_status = Label(
            self.select_picture_frame, bg='#143d59', font='raleway 14')
        self.select_image = Button(self.select_picture_frame, text='Select images', font='raleway 14', bd=2, width=20,
                                   borderwidth=0, fg='#143d59', bg='#f4b41a', command=self.openfile_name)
        self.select_image.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(self.select_picture_frame, text='Shuffle images?', font='raleway 14', fg='#fff', bg='#143d59').place(
            relx=0.23, rely=0.8, anchor=W)
        Checkbutton(self.select_picture_frame, activebackground='#143d59', fg='#f4b41a', bg='#143d59',
                    selectcolor='#143d59', variable=self.shuffle_or_not).place(relx=0.65, rely=0.81, anchor=W)
        # =========== Time Frame Insides ===============
        self.SESSION_TIMING_status = Label(self.select_time_frame, bg='#143d59', text='foggy day in london town',
                                           font='raleway 14')
        Label(self.select_time_frame, text='30 seconds', font='raleway 14', fg='#fff', bg='#143d59').place(
            relx=0.19, rely=0.26, anchor=W)
        self.thirty_seconds = Radiobutton(self.select_time_frame, activebackground='#143d59', fg='#f4b41a',
                                          value=30, width=2, variable=self.time, bg='#143d59', selectcolor='#143d59')
        self.thirty_seconds.place(relx=0.06, rely=0.28, anchor=W)
        Label(self.select_time_frame, text='1 minute', font='raleway 14', fg='#fff', bg='#143d59').place(
            relx=0.19, rely=0.46, anchor=W)
        self.one_minute = Radiobutton(self.select_time_frame, activebackground='#143d59', fg='#f4b41a',
                                      value=60, width=2, variable=self.time, bg='#143d59', selectcolor='#143d59')
        self.one_minute.place(relx=0.06, rely=0.48, anchor=W)
        Label(self.select_time_frame, text='5 minutes', font='raleway 14', fg='#fff', bg='#143d59').place(
            relx=0.19, rely=0.66, anchor=W)
        self.five_minutes = Radiobutton(self.select_time_frame, activebackground='#143d59', fg='#f4b41a',
                                        value=300, width=2, variable=self.time, bg='#143d59', selectcolor='#143d59')
        self.five_minutes.place(relx=0.06, rely=0.68, anchor=W)
        Label(self.select_time_frame, text='Custom time in secs', font='raleway 14', fg='#fff', bg='#143d59').place(
            relx=0.08, rely=0.835, anchor=W)
        self.custom_entry = Entry(self.select_time_frame, justify=CENTER,
                                  width=10, font='raleway', textvariable=self.custom_time)
        self.custom_entry.insert(0, '120 / 3mins')
        self.custom_entry.place(relx=0.6, rely=0.855, anchor=W)
        # =========== Mouse Events Bindings ===============
        self.custom_entry.bind('<FocusIn>', self.in_click)
        self.custom_entry.bind('<FocusOut>', self.out_click)
        self.root.bind_all('<1>', lambda event: event.widget.focus_set())
        # =========== Start Button ===============
        self.start = Button(text='Start drawing', font='raleway 14', bd=2, width=15, borderwidth=0,
                            fg='#143d59', bg='#f4b41a', cursor='hand2', command=self.validate_inputs)
        self.start.place(relx=0.5, rely=0.89, anchor=CENTER)

    def validate_inputs(self):
        global SHUFFLE, SESSION_TIMING
        SHUFFLE = self.shuffle_or_not.get()
        picture_pass = False
        time_pass = False
        if (self.custom_time.get() in ['0', '120 / 3mins'] and self.time.get() == 0) \
                or self.time.get() != 0 and self.custom_time.get() not in ['0', '120 / 3mins']:
            self.SESSION_TIMING_status.config(
                text='Use either provided time or custom time', fg='red')
            self.SESSION_TIMING_status.place(anchor=CENTER, relx=0.5, rely=0.1)
        else:
            self.SESSION_TIMING_status.config(
                text='Time set successfully!', fg='#f2aa4c')
            self.SESSION_TIMING_status.place(anchor=CENTER, relx=0.5, rely=0.1)
            SESSION_TIMING = self.time.get()
            time_pass = True
        if PICTURES_TO_DRAW == []:
            self.pictures_status.config(
                text='No pictures were selected', fg='red')
            self.pictures_status.place(anchor=CENTER, relx=0.5, rely=0.17)
        else:
            picture_pass = True
        self.switch_page(picture_pass, time_pass)

    def switch_page(self, picture_check, time_check):
        if picture_check and time_check:
            return self.master.switch_frame(MainPage)

    def openfile_name(self):
        global PICTURES_TO_DRAW
        selected_pictures = askopenfilenames(
            filetypes=[('image files', '*.png *.jpg')])
        if selected_pictures:
            for picture in selected_pictures:
                PICTURES_TO_DRAW.append(picture)
            self.pictures_status.config(
                text='Image(s) loaded successfully!', fg='#f2aa4c')
            self.pictures_status.place(anchor=CENTER, relx=0.5, rely=0.17)
        else:
            PICTURES_TO_DRAW = []
            self.pictures_status.config(
                text='No pictures were selected', fg='red')
            self.pictures_status.place(anchor=CENTER, relx=0.5, rely=0.17)

    def in_click(self, event=None):
        self.time.set(0)
        if self.custom_time.get() == '120 / 3mins':
            self.custom_entry.config(width=5)
            self.custom_entry.delete(0, END)

    def out_click(self, event=None):
        if self.custom_time.get() == '':
            self.custom_entry.config(width=10)
            self.custom_entry.insert(0, "120 / 3mins")


class MainPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#143d59')
        self.root = root
        self.root.geometry('1000x700+183+20')
        self.root.title('Time It & Draw')
        self.root.resizable(0, 0)
        # ======= Variables ========
        self.session_over = False
        self.is_drawing = False
        self.drawn_pictures = []
        self.shuffled_pictures = PICTURES_TO_DRAW
        self.current_picture = ''
        self.current_picture_index = 0
        self.time_frame = SESSION_TIMING
        self._counter = None
        # ======= Time Frame ========
        self.time_label = Label(bg='#143d59', font='candara 38')
        self.time_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        # ======= Picture Frame ========
        self.picture_frame = Frame(
            self.master, width=770, height=520, relief='ridge', bd=3)
        self.picture_frame.place(anchor=N, relx=0.5, rely=0.12)
        # ======= Session over Frame ========
        self.session_over_frame = Frame(
            self.master, bg='#143d59', width=1000, height=700, relief='ridge', bd=3)
        # ======= Image ========
        self.scale = float(1.0)
        self.image_to_draw = Label(self.picture_frame)
        self.image_to_draw.place(anchor=CENTER, rely=0.5, relx=0.5)
        # ======= Action Buttons ========
        self.next_button = Button(text='Next image', font='raleway 14', bd=2, width=15, borderwidth=0,
                                  fg='#143d59', bg='#f2aa4c', cursor='hand2', command=self.next_image)
        self.next_button.place(relx=0.5, rely=0.94, anchor=CENTER)
        self.pause_button = Button(text='Pause', font='raleway 14', bd=2, width=15, borderwidth=0,
                                   fg='#143d59', bg='#f2aa4c', cursor='hand2', command=self.pause_session)
        self.pause_button.place(relx=0.25, rely=0.94, anchor=CENTER)
        self.settings_button = Button(text='Settings', font='raleway 14', bd=2, width=15, borderwidth=0,
                                      fg='#143d59', bg='#f2aa4c', cursor='hand2', command=self.stop_session)
        self.settings_button.place(relx=0.75, rely=0.94, anchor=CENTER)
        if SHUFFLE:
            shuffle(self.shuffled_pictures)
        self.pick_a_picture()

    def resize_images(self, image):
        screenwidth = int(950//1.3)
        screenheight = int(500//1.3)
        w, h = image.width, image.height
        if w > h:
            delta = screenwidth / w
            new_width, new_height = screenwidth, int(h*delta)
        else:
            delta = screenheight / h
            new_width, new_height = int(w*delta), screenheight
        return new_width, new_height

    def pick_a_picture(self):
        picture_list = self.shuffled_pictures if SHUFFLE else PICTURES_TO_DRAW
        if self.current_picture_index == len(PICTURES_TO_DRAW) - 1:
            self.next_button.config(state=DISABLED)
        self.current_picture = picture_list[self.current_picture_index]
        self.time_frame = SESSION_TIMING

        try:
            self.img = Image.open(self.current_picture)
            test = self.resize_images(self.img)
            self.image = ImageTk.PhotoImage(
                self.img.resize((test[0], test[1])))
            self.image_to_draw.config(image=self.image)
        except FileNotFoundError:
            self.check_session_done()

        self.is_drawing = True
        self.count_down()

    def check_session_done(self):
        if len(PICTURES_TO_DRAW) == len(self.drawn_pictures):
            self.is_drawing = False
            self.show_session_over()
        else:
            self.current_picture_index += 1
            self.pick_a_picture()

    def count_down(self):
        if self.is_drawing == True:
            if self.time_frame >= 10:
                mins, secs = divmod(self.time_frame, 60)
                self.time_label.config(text='{:02d}:{:02d}'.format(
                    mins, secs), bg='#143d59', fg='#fff')
                self.time_frame -= 1
                self._counter = self.time_label.after(1000, self.count_down)
            elif self.time_frame < 10 and self.time_frame >= 5:
                mins, secs = divmod(self.time_frame, 60)
                self.time_label.config(text='{:02d}:{:02d}'.format(
                    mins, secs), bg='#143d59', fg='yellow')
                self.time_frame -= 1
                self._counter = self.time_label.after(1000, self.count_down)
            elif self.time_frame < 5 and self.time_frame != -1:
                mins, secs = divmod(self.time_frame, 60)
                self.time_label.config(text='{:02d}:{:02d}'.format(
                    mins, secs), bg='#143d59', fg='orangered')
                self.time_frame -= 1
                self._counter = self.time_label.after(1000, self.count_down)
            else:
                self.drawn_pictures.append(self.current_picture)
                self.check_session_done()

    def next_image(self):
        self.is_drawing = False
        self.time_label.after_cancel(self._counter)
        self.drawn_pictures.append(self.current_picture)
        self.current_picture_index += 1
        self.pick_a_picture()

    def pause_session(self):
        if self.is_drawing:
            self.pause_button.config(text='Continue')
            self.is_drawing = False
        else:
            self.pause_button.config(text='Pause')
            self.is_drawing = True
            self.count_down()

    def show_session_over(self):
        global PICTURES_TO_DRAW, SESSION_TIMING, SHUFFLE
        PICTURES_TO_DRAW = []
        SESSION_TIMING = 0
        SHUFFLE = False
        self.session_over_frame.place(x=0, y=0)
        self.pause_button.place_forget()
        self.next_button.place_forget()
        self.settings_button.place(relx=0.5, rely=0.55)
        Label(text='Drawing session is over', fg='#fff',
              bg='#143d59', font='raleway 32').place(relx=0.5, rely=0.45, anchor=CENTER)

    def stop_session(self):
        global PICTURES_TO_DRAW, SESSION_TIMING, SHUFFLE
        PICTURES_TO_DRAW = []
        SESSION_TIMING = 0
        SHUFFLE = False
        self.master.switch_frame(SettingsPage)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
