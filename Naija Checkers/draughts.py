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
        # ============ COLOR SCHEME =============
        self.BOARD_DARK_COLOUR = "#AF8968"
        self.BOARD_LIGHT_COLOUR = "#ECDAB9"
        # ============ Variables =============
        self.board_positions = {}
        self.piece_positions = {}
        # ============ STARTER FUNCTIONS =============
        self.show_utility_icons()
        self.init_all_images()
        self.create_game_board()

        # print(self.board_positions)

    def init_all_images(self):
        self.all_images = {
            'light_piece': ImageTk.PhotoImage(Image.open('./assets/light-piece.png').resize((48, 48), Image.LANCZOS)),
            'dark_piece': ImageTk.PhotoImage(Image.open('./assets/dark-piece.png').resize((48, 48), Image.LANCZOS)),
            'light_king': ImageTk.PhotoImage(Image.open('./assets/light-king.png').resize((48, 48), Image.LANCZOS)),
            'dark_king': ImageTk.PhotoImage(Image.open('./assets/dark-king.png').resize((48, 48), Image.LANCZOS))
        }

    def create_game_board(self):
        self.board = [[" "]*10 for i in range(10)]
        self.gameboard_frame = Canvas(
            bg=self.BOARD_DARK_COLOUR, width=625, height=625)
        self.gameboard_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.game_canvas = Canvas(
            self.gameboard_frame, bg=self.BOARD_DARK_COLOUR, width=600, height=600)
        self.game_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        for i, value in enumerate("ABCDEFGHIJ"):
            for j in range(10):
                x0 = (i * 60) + 0.6
                x1 = x0 + 60
                y0 = (j * 60) + 0.6
                y1 = y0 + 60
                if (i + j) % 2 == 0:
                    piece = self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=self.BOARD_DARK_COLOUR, outline=self.BOARD_LIGHT_COLOUR, tags=(f"{value}{j}", (i, j)))
                else:
                    piece = self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=self.BOARD_LIGHT_COLOUR, outline=self.BOARD_LIGHT_COLOUR)

                self.board_positions[f"{value}{j}"] = (piece, x0, y0, x1, y1)

    def show_utility_icons(self):
        # ======== Back Button ============
        self.back_image = Image.open('./assets/back_icon.png')
        self.back_bg = self.back_image.resize((35, 35), Image.LANCZOS)
        self.back_bg = ImageTk.PhotoImage(self.back_bg)
        Button(image=self.back_bg, bg="#fff",
               command=self.go_back).place(relx=0.05, rely=0.08, anchor=CENTER)
        # ======== Help Button ============
        self.help_image = Image.open('./assets/help_icon.png')
        self.help_bg = self.help_image.resize((35, 35), Image.LANCZOS)
        self.help_bg = ImageTk.PhotoImage(self.help_bg)
        Button(image=self.help_bg, bg="#fff", command=self.show_help).place(
            relx=0.95, rely=0.08, anchor=CENTER)

    def go_back(self):
        self.master.switch_frame(StartPage)

    def show_help(self):
        self.game_help_veil = Frame(width=1000, height=700)
        self.game_help_veil.place(x=0, y=0)
        # ============ APP Background =============
        self.help_image = Image.open('54.jpg')
        self.help_image = self.help_image.resize((1000, 700), Image.LANCZOS)
        self.help_image = ImageTk.PhotoImage(self.help_image)
        Label(self.game_help_veil, border=0,
              image=self.help_image).pack()
        # ============ Back button =============
        self.about_bg = Image.open('back_icon.png')
        self.about_bg = self.about_bg.resize((30, 30), Image.LANCZOS)
        self.about_bg = ImageTk.PhotoImage(self.about_bg)
        Button(self.game_help_veil, image=self.about_bg, bg="#fff",
               command=self.hide_game_help).place(relx=0.05, rely=0.06, anchor=CENTER)

        help_canvas = Canvas(self.game_help_veil, width=800,
                             height=600)
        help_canvas.place(relx=0.5, rely=0.5, anchor='center')

        a = f"The object of the game is to have the majority of your\n discs' color facing up on the board at the end of the game"
        b = "\n\n How to move:\n A move consist of \"outflanking\" your opponent's disc(s), then\n flipping the outflanked disc(s) to your color"
        help_canvas.create_text(400, 50, justify='center',
                                text=a, font=("fira code", 16))
        help_canvas.create_text(400, 100, justify='center',
                                text=b, font=("fira code", 16))

        # c = "\nTo outflank means to place your disc on the board in a way\n that the opposing color is bordered at each end by a disc of your color"
        # d = "\n\n Rules: \n==> Black always moves first\n==> If you cannot outflank any disc on your turn, \nyou forfeit your turn and your opponent moves"
        # e = "\n==> You cannot skip over your own color to outflank an opposing disc"
        # f = "\n==> If both players cannot move, the game is over"
        # g = "\n\n Enjoy!"
        # about_text = a + b + c + d + e + f + g
        # Label(self.game_help_veil, text=about_text, font=("fira code", 16), fg='#fff', bg='#101820').place(
        #     relx=0.5, rely=0.5, anchor="center")

    def hide_game_help(self):
        self.game_help_veil.place_forget()


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
