from tkinter import Tk, Label, Frame, Button, StringVar, Radiobutton
from PIL import ImageTk, Image
from game_ui import MainPage
from game_logic import Logic

root = Tk


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
        Frame.configure(self, bg="#006633")
        self.master = root
        self.master.geometry("500x600+433+84")
        self.master.resizable(0, 0)
        # ================== UI =================
        self.bg = Image.open("./static/solitaire.png")
        width, height = self.bg.size
        self.bg = self.bg.resize((width//2, height//2))
        self.the_logo = ImageTk.PhotoImage(self.bg)
        Label(self.master, image=self.the_logo).place(
            relx=0.5, rely=0.35, anchor="center")

        Label(self.master, text="Solitaire", font=("Mosk Medium 500", 48),
              fg="#505050", bg="white").place(relx=0.5, rely=0.66, anchor="center")
        Label(self.master, text="Solitaire", font=("Mosk Medium 500", 48),
              fg="#fff", bg="#006633").place(relx=0.5, rely=0.655, anchor="center")
        Button(self.master, text="Start", width=16, font=("Mosk Normal 400", 16), bd=0,
               fg="#006633", command=self.start_game).place(relx=0.5, rely=0.82, anchor="center")

    def start_game(self):
        self.master.switch_frame(SettingsPage)


class SettingsPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#006633")
        self.master = root
        self.master.geometry("500x600+433+84")
        self.master.resizable(0, 0)
        # ======= Variables ===========
        self.suit_type = StringVar()
        self.suit_type.set("spades")
        # ================== UI =================
        self.select_suit_type = Frame(
            self.master, width=500, height=600, relief='ridge', bg='#006633', bd=3)
        self.select_suit_type.place(anchor="center", relx=0.5, rely=0.5)

        Label(self.select_suit_type, text='Select suit type', font=("Mosk Medium 500", 28), fg='#fff', bg='#006633').place(
            relx=0.19, rely=0.35, anchor="w")

        self.spades_label = Label(self.select_suit_type, text='Spades', font=(
            "Mosk Medium 500", 18), fg='#fff', bg='#006633')
        self.spades_label.place(relx=0.19, rely=0.45, anchor="w")
        self.spades_label.bind(
            "<Button-1>", lambda event: self.set_suit_type("spades"))
        spades_radio_btn = Radiobutton(self.select_suit_type, activebackground='#006633', fg='#fff',
                                       value="spades", width=2, variable=self.suit_type, bg='#006633', selectcolor='#006633')
        spades_radio_btn.place(relx=0.1, rely=0.45, anchor="w")

        self.diamonds_label = Label(self.select_suit_type, text='Diamonds', font=(
            "Mosk Medium 500", 18), fg='#fff', bg='#006633')
        self.diamonds_label.place(relx=0.59, rely=0.45, anchor="w")
        self.diamonds_label.bind(
            "<Button-1>", lambda event: self.set_suit_type("diamonds"))
        diamonds_radio_btn = Radiobutton(self.select_suit_type, activebackground='#006633', fg='#fff',
                                         value="diamonds", width=2, variable=self.suit_type, bg='#006633', selectcolor='#006633')
        diamonds_radio_btn.place(relx=0.5, rely=0.45, anchor="w")

        self.clubs_label = Label(self.select_suit_type, text='Clubs', font=(
            "Mosk Medium 500", 18), fg='#fff', bg='#006633')
        self.clubs_label.place(relx=0.19, rely=0.53, anchor="w")
        self.clubs_label.bind(
            "<Button-1>", lambda event: self.set_suit_type("clubs"))
        clubs_radio_btn = Radiobutton(self.select_suit_type, activebackground='#006633', fg='#fff',
                                      value="clubs", width=2, variable=self.suit_type, bg='#006633', selectcolor='#006633')
        clubs_radio_btn.place(relx=0.1, rely=0.53, anchor="w")

        self.hearts_label = Label(self.select_suit_type, text='Hearts', font=(
            "Mosk Medium 500", 18), fg='#fff', bg='#006633')
        self.hearts_label.place(relx=0.59, rely=0.53, anchor="w")
        self.hearts_label.bind(
            "<Button-1>", lambda event: self.set_suit_type("hearts"))
        hearts_radio_btn = Radiobutton(self.select_suit_type, activebackground='#006633', fg='#fff',
                                       value="hearts", width=2, variable=self.suit_type, bg='#006633', selectcolor='#006633')
        hearts_radio_btn.place(relx=0.5, rely=0.53, anchor="w")

        Button(self.select_suit_type, text="Start", width=16, font=("Mosk Normal 400", 16), bd=0,
               fg="#006633", command=self.save_settings_and_start).place(relx=0.19, rely=0.65, anchor="w")

    def set_suit_type(self, value, event=None):
        self.suit_type.set(value)
        all_suites = {"hearts": self.hearts_label, "diamonds": self.diamonds_label,
                      "clubs": self.clubs_label, "spades": self.spades_label}

        # return all of the labels to their default foreground colors
        for label in all_suites.values():
            label.config(fg="#fff")

        # change color of the selected suite
        selected = all_suites[value]
        selected.config(fg="#FFDE24")

    def save_settings_and_start(self):
        suit_selected = self.suit_type.get()
        Logic.SUIT_TYPE = suit_selected
        self.master.switch_frame(MainPage)


if __name__ == "__main__":
    app = Switch()
    app.title("Solitaire")
    app.iconbitmap(r"./static/icon.ico")
    app.mainloop()
