from tkinter import Tk, Frame, Button, Label
from game_ui import MultiPlayer

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
        Frame.configure(self, bg="#101820")
        self.master = root
        self.master.title("Chess")
        self.master.geometry('630x400+368+179')
        self.master.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Chess', font=('Fiolex Girls', 65),
              fg='#505050', bg='#fff').place(relx=0.5, rely=0.372, anchor="center")
        Label(self.master, text='Chess', font=('Fiolex Girls', 65),
              fg='#fff', bg='#101820').place(relx=0.5, rely=0.36, anchor="center")
        Button(self.master, text='Start', width=18, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=self.start_multiplayer).place(relx=0.5, rely=0.63, anchor="center")

    def start_multiplayer(self):
        self.master.switch_frame(MultiPlayer)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
