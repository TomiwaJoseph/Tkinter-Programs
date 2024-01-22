from tkinter import Label, Frame, Tk, Canvas, Button, CENTER, IntVar, Checkbutton, messagebox
from PIL import ImageTk, Image


root = Tk
AI_TO_PLAY_BLACK = False


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(HumanPage)

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
        self.root = root
        self.root.title("Naija Checkers")
        self.root.geometry('630x400+368+179')
        self.root.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Naija Checkers', font=('Fiolex Girls', 65),
              fg='#505050', bg='#fff').place(relx=0.5, rely=0.372, anchor="center")
        Label(self.master, text='Naija Checkers', font=('Fiolex Girls', 65),
              fg='#fff', bg='#101820').place(relx=0.5, rely=0.36, anchor="center")
        Button(self.master, text='AI', width=12, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.master.switch_frame(HumanPage)).place(relx=0.25, rely=0.63, anchor="w")
        Button(self.master, text='2 Players', width=14, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.master.switch_frame(HumanPage)).place(relx=0.5, rely=0.63, anchor="w")


class HumanPage(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.root.title("Naija Checkers")
        self.root.geometry('1000x700+200+20')
        self.root.resizable(0, 0)
        # ============ APP Background =============
        self.bg_image = Image.open('./assets/54.jpg')
        self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        Label(self, image=self.bg_image).pack()


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
