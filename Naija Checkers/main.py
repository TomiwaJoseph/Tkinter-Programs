from tkinter import Label, Frame, Tk, Button, IntVar, Checkbutton
from ai.versus_ai_ui import VersusAI
from shared.logic import Logic, AILogic


root = Tk


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(AISettings)

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
        self.master.title("Naija Checkers")
        self.master.geometry('630x400+368+179')
        self.master.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Naija Checkers', font=('Fiolex Girls', 65),
              fg='#505050', bg='#fff').place(relx=0.5, rely=0.372, anchor="center")
        Label(self.master, text='Naija Checkers', font=('Fiolex Girls', 65),
              fg='#fff', bg='#101820').place(relx=0.5, rely=0.36, anchor="center")
        Button(self.master, text='AI', width=12, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.set_game_mode("AI")).place(relx=0.25, rely=0.63, anchor="w")
        Button(self.master, text='2 Players', width=14, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=lambda: self.set_game_mode("multiplayer")).place(relx=0.5, rely=0.63, anchor="w")

    def set_game_mode(self, mode):
        Logic.game_mode = mode
        if mode == "multiplayer":
            from multiplayer.multiplayer_ui import MultiPlayer
            self.master.switch_frame(MultiPlayer)
        else:
            self.master.switch_frame(AISettings)


class AISettings(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg="#101820")
        self.master = root
        self.master.title("Naija Checkers | Settings")
        self.master.geometry('630x400+368+179')
        self.master.resizable(0, 0)
        # ======= Variables ===========
        self.AI_WHITE = IntVar()
        self.AI_FIRST = IntVar()
        # ======= UI =====================
        Checkbutton(self.master, text=" " * 2 + 'AI should play as WHITE',  font=('fira code medium', 14), fg='#fff', bg='#101820',
                    activebackground='#101820', selectcolor='#101820', variable=self.AI_WHITE).place(relx=0.23, rely=0.35, anchor="w")
        Checkbutton(self.master, text=" " * 2 + 'AI should play first',  font=('fira code medium', 14), fg='#fff', bg='#101820',
                    activebackground='#101820', selectcolor='#101820', variable=self.AI_FIRST).place(relx=0.23, rely=0.48, anchor="w")
        Button(self.master, text='Save and continue', width=20, font=('fira code medium', 14), bd=0, fg='#101820', bg='#fff',
               command=self.save_ai_settings).place(relx=0.24, rely=0.63, anchor="w")

    def save_ai_settings(self):
        Logic.game_mode = "AI"  # delete this later
        AILogic.AI_plays_white = self.AI_WHITE.get()
        AILogic.AI_plays_first = self.AI_FIRST.get()
        self.master.switch_frame(VersusAI)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
