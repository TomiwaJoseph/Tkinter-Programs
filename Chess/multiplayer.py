from tkinter import Label, Entry, Frame, Canvas, Button, Menu, StringVar
from PIL import ImageTk, Image
# from .multiplayer_logic import Logic
# from .multiplayer_piece import Piece


# ====== Themes ===========
board_color_schemes = {
    'Default': '#000-#fff',
    'Greygarious': '#83406A-#D1D4D1-#83406A',
    'Aquamarine': '#5B8340-#D1E7E0-#5B8340',
    'Bold Beige': '#4B4620-#FFF0E1-#4B4620',
    'Cobalt Blue': '#ffffBB-#3333aa-#fff',
    'Olive Green': '#D1E7E0-#5B8340-#D1E7E0',
    'Night Mode': '#fff-#000-#fff',
    "Black 'N Yellow": '#ff0-#000-#ff0'
}
piece_color_schemes = {
    'Default': '#000-#fff',
    'Greygarious': '#83406A-#D1D4D1-#83406A',
    'Aquamarine': '#5B8340-#D1E7E0-#5B8340',
    'Bold Beige': '#4B4620-#FFF0E1-#4B4620',
    'Cobalt Blue': '#ffffBB-#3333aa-#fff',
}


class MultiPlayer(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.master = root
        self.master.title("Chess")
        self.master.geometry('1000x700+200+10')
        self.master.resizable(0, 0)
        # ============ Starter functions =============
        self.board_choice = StringVar()
        self.piece_choice = StringVar()
        self.show_app_background()
        # ========= MENUBAR ==============
        self.create_menubar()

    def show_app_background(self):
        self.bg_image = Image.open('./assets/bg.jpg')
        self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        Label(self, image=self.bg_image).pack()

    def create_menubar(self):
        menubar = Menu()
        # ===================================
        game_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Game', menu=game_menu)
        game_menu.add_command(label='New Game')
        # Add line between New Game and Exit
        game_menu.add_separator()
        game_menu.add_command(label='Exit', command=self.master.destroy)
        self.master.config(menu=menubar)
        # ===================================
        options_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Options', menu=options_menu)
        # options_menu.add_command(label='Boards')
        board_themes_menu = Menu(options_menu, bg='orange', tearoff=0)
        options_menu.add_cascade(label='Boards', menu=board_themes_menu)

        self.board_choice.set('Default')
        for keys in board_color_schemes:
            board_themes_menu.add_radiobutton(
                label=keys, variable=self.board_choice, command=self.change_board)
            board_themes_menu.add_separator()
        options_menu.add_separator()

        piece_themes_menu = Menu(options_menu, bg='orange', tearoff=0)
        options_menu.add_cascade(label='Pieces', menu=piece_themes_menu)
        self.piece_choice.set('Default')
        for keys in piece_color_schemes:
            piece_themes_menu.add_radiobutton(
                label=keys, variable=self.piece_choice, command=self.change_piece)
            piece_themes_menu.add_separator()
        options_menu.add_separator()
        options_menu.add_command(label='Clock', command=self.set_game_duration)
        # ===================================
        info_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=info_menu,
                            command=lambda: print("here......."))
        info_menu.add_command(
            label="About app", command=lambda: self.show_about("app"))
        info_menu.add_command(label="About Developer",
                              command=lambda: self.show_about("developer"))

    def change_board(self):
        print(self.board_choice.get())

    def change_piece(self):
        print(self.piece_choice.get())

    def set_game_duration(self):
        pass

    def show_about(self, section):
        self.game_help_veil = Frame(width=1000, height=700)
        self.game_help_veil.place(x=0, y=0)
        # ============ APP Background =============
        self.help_image = Image.open('./assets/bg.jpg')
        self.help_image = self.help_image.resize((1000, 700), Image.LANCZOS)
        self.help_image = ImageTk.PhotoImage(self.help_image)
        Label(self.game_help_veil, border=0,
              image=self.help_image).pack()

        if section == "app":
            help_canvas = Canvas(self.game_help_veil, width=500,
                                 height=450, border=3, relief="ridge", borderwidth=3)
            help_canvas.place(relx=0.5, rely=0.5, anchor='center')
            Label(self.game_help_veil, text="  ABOUT APP  ", font=("Mosk Bold 700", 24)).place(
                relx=0.5, rely=0.17, anchor="center")
            a = "A simple chess application"
            b = "Features includes:"
            c = "◾ Initial pawn move (Two Squares)"
            c = "◾ Castling (King and Queen side)"
            d = "◾ Pawn Promotion"
            e = "◾ En passant"
            f = "◾ ... and others."

            help_canvas.create_text(60, 70, anchor="w",
                                    text=a, font=("Mosk Normal 400", 18))
            help_canvas.create_text(
                60, 120, anchor="w", text=b, font=("Mosk Bold 700", 18))
            help_canvas.create_text(
                60, 170, anchor="w", text=c, font=("Mosk Normal 400", 18))
            help_canvas.create_text(
                60, 220, anchor="w", text=d, font=("Mosk Normal 400", 18))
            help_canvas.create_text(
                60, 270, anchor="w", text=e, font=("Mosk Normal 400", 18))
            help_canvas.create_text(
                60, 320, anchor="w", text=f, font=("Mosk Normal 400", 18))

            Button(self.game_help_veil, text="Close", bd=0, fg='#fff', bg='#101820', font=(
                "fira code medium", 14), width=15, command=self.hide_game_help_veil).place(relx=0.395, rely=0.74, anchor="center")
        else:
            help_canvas = Canvas(self.game_help_veil, width=700,
                                 height=500, border=3, relief="ridge", borderwidth=3)
            help_canvas.place(relx=0.5, rely=0.5, anchor='center')
            help_canvas.create_text(60, 70, font=("Mosk Normal 400", 18), anchor='w',
                                    text="I am Tomiwa Joseph, an experienced software developer.")
            help_canvas.create_text(60, 120, font=(
                "Mosk Bold 700", 18), anchor="w", text="Here is my portfolio:")
            help_canvas.create_text(60, 170, font=(
                "Mosk Normal 400", 18), anchor="w", text="https://tomiwajoseph.vercel.app")
            help_canvas.create_text(60, 220, font=(
                "Mosk Bold 700", 18), anchor="w", text="My socials:")
            help_canvas.create_text(60, 270, font=(
                "Mosk Normal 400", 18), anchor="w", text="https://github.com/TomiwaJoseph")
            help_canvas.create_text(60, 320, font=(
                "Mosk Normal 400", 18), anchor="w", text="https://www.linkedin.com/in/tomiwa-joseph/")
            help_canvas.create_text(60, 370, font=(
                "Mosk Normal 400", 18), anchor="w", text="https://www.x.com/tomiwajoseph10/")

            Button(self.game_help_veil, text="Close", bd=0, fg='#fff', bg='#101820', font=(
                "fira code medium", 14), width=15, command=self.hide_game_help_veil).place(relx=0.5, rely=0.78, anchor="center")

    def hide_game_help_veil(self):
        self.game_help_veil.place_forget()
