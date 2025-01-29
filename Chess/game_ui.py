from tkinter import Tk, Label, Entry, Frame, Canvas, Button, Menu, StringVar
from PIL import ImageTk, Image
from game_logic import Logic
from game_piece import Piece


root = Tk


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(MultiPlayer)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0, y=0, relheight=1, relwidth=1)


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
        # ============ Variables =============
        self.BOARD_DARK_COLOUR = "#AF8968"
        self.BOARD_LIGHT_COLOUR = "#ECDAB9"
        self.promotion_canvas = None
        # ============ Starter functions =============
        self.board_choice = StringVar()
        self.piece_choice = StringVar()
        self.show_app_background()
        # ========= MENUBAR ==============
        self.create_menubar()
        self.init_all_images()
        self.create_game_board()
        self.create_testing_pieces()
        # self.show_game_outcome(None, "Because Ayra Starr is goddamn sexy...")
        # self.create_game_pieces()
        # self.show_promotion_options("W", "E0", "0 4")

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

    def init_all_images(self):
        self.all_images = {}
        pieces = [("white_king", "wK"), ("white_queen", "wQ"), ("white_rook", "wR"), ("white_bishop", "wB"), ("white_knight", "wN"), ("white_pawn", "wP"),
                  ("black_king", "bK"), ("black_queen", "bQ"), ("black_rook", "bR"), ("black_bishop", "bB"), ("black_knight", "bN"), ("black_pawn", "bP")]

        for piece, symbol in pieces:
            image = Image.open(f"./assets/pieces/{symbol}.png")
            image.thumbnail((50, 50))
            image.save("new_img.png")
            self.all_images[piece] = ImageTk.PhotoImage(image)

    def create_game_board(self):
        self.board = [[" "]*8 for i in range(8)]
        self.gameboard_frame = Canvas(
            bg=self.BOARD_DARK_COLOUR, width=620, height=620)
        self.gameboard_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.game_canvas = Canvas(
            self.gameboard_frame, bg='red', width=600, height=600)
        self.game_canvas.place(relx=0.5, rely=0.5, anchor="center")
        rows = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}

        for i, value in enumerate("ABCDEFGH"):
            for j in range(8):
                x0 = (i * 75) + 0.6
                x1 = x0 + 75
                y0 = (j * 75) + 0.6
                y1 = y0 + 75
                if (i + j) % 2 == 0:
                    self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=self.BOARD_LIGHT_COLOUR, outline=self.BOARD_LIGHT_COLOUR, tags=(f"board-{value}{j}", f"{j} {rows[value]}"))
                else:
                    self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=self.BOARD_DARK_COLOUR, outline=self.BOARD_DARK_COLOUR, tags=(f"board-{value}{j}", f"{j} {rows[value]}"))

    def create_testing_pieces(self):
        """ create testing positions """

        piece_symbol = {"rook": "R", "knight": "N",
                        "king": "K", "queen": "Q", "bishop": "B"}
        rows = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        white_pawns = [("C", 3)]
        black_pawns = [("E", 1)]
        black_rooks = [("H", 6), ("B", 6)]
        white_rooks = []
        white_knights = []
        black_knights = []
        white_bishops = []
        black_bishops = []
        Piece.white_king_has_moved = True
        Piece.black_king_has_moved = True

        for bishop in white_bishops+black_bishops:
            alpha, i = bishop
            if bishop in white_bishops:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "bishop"
                self.board[i][rows[alpha]] = f"w{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(x1, y1, image=self.all_images[f"white_{piece_type}"], tags=(
                    f'w{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "W")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.white_pieces.append(the_piece)
            if bishop in black_bishops:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "bishop"
                self.board[i][rows[alpha]] = f"b{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(
                    x1, y1, image=self.all_images[f"black_{piece_type}"], tags=(f'b{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "B")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.black_pieces.append(the_piece)

        for knight in white_knights+black_knights:
            alpha, i = knight
            if knight in white_knights:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "knight"
                self.board[i][rows[alpha]] = f"w{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(x1, y1, image=self.all_images[f"white_{piece_type}"], tags=(
                    f'w{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "W")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.white_pieces.append(the_piece)
            if knight in black_knights:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "knight"
                self.board[i][rows[alpha]] = f"b{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(
                    x1, y1, image=self.all_images[f"black_{piece_type}"], tags=(f'b{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "B")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.black_pieces.append(the_piece)

        for rook in white_rooks+black_rooks:
            alpha, i = rook
            if rook in white_rooks:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "rook"
                self.board[i][rows[alpha]] = f"w{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(x1, y1, image=self.all_images[f"white_{piece_type}"], tags=(
                    f'w{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "W")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.white_pieces.append(the_piece)
            if rook in black_rooks:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_type = "rook"
                self.board[i][rows[alpha]] = f"b{piece_symbol[piece_type]}"
                piece_id = self.game_canvas.create_image(
                    x1, y1, image=self.all_images[f"black_{piece_type}"], tags=(f'b{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                the_piece = Piece(
                    i, rows[alpha], piece_type, piece_id, "B")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.black_pieces.append(the_piece)

        for _ in range(1):
            alpha, i = "B", 7
            find_tag = self.game_canvas.find_withtag(
                f"board-{alpha}{i}")
            tag_coord = self.game_canvas.coords(find_tag[0])
            get_center = Logic.get_coordinate_center(tag_coord)
            x1, y1 = get_center
            piece_type = "king"
            self.board[i][rows[alpha]] = f"w{piece_symbol[piece_type]}"
            piece_id = self.game_canvas.create_image(x1, y1, image=self.all_images[f"white_{piece_type}"], tags=(
                f'w{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
            the_piece = Piece(
                i, rows[alpha], piece_type, piece_id, "W")
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
            Logic.white_pieces.append(the_piece)

        for _ in range(1):
            alpha, i = "H", 0
            find_tag = self.game_canvas.find_withtag(
                f"board-{alpha}{i}")
            tag_coord = self.game_canvas.coords(find_tag[0])
            get_center = Logic.get_coordinate_center(tag_coord)
            x1, y1 = get_center
            piece_type = "king"
            self.board[i][rows[alpha]] = f"b{piece_symbol[piece_type]}"
            piece_id = self.game_canvas.create_image(
                x1, y1, image=self.all_images[f"black_{piece_type}"], tags=(f'b{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
            the_piece = Piece(
                i, rows[alpha], piece_type, piece_id, "B")
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
            Logic.black_pieces.append(the_piece)

        for pawn in white_pawns+black_pawns:
            alpha, i = pawn
            if pawn in white_pawns:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_id = self.game_canvas.create_image(
                    x1, y1, image=self.all_images['white_pawn'], tags=('wP', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                self.board[i][rows[alpha]] = "wP"
                the_piece = Piece(i, rows[alpha], "pawn", piece_id, "W")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.white_pieces.append(the_piece)
            else:
                find_tag = self.game_canvas.find_withtag(
                    f"board-{alpha}{i}")
                tag_coord = self.game_canvas.coords(find_tag[0])
                get_center = Logic.get_coordinate_center(tag_coord)
                x1, y1 = get_center
                piece_id = self.game_canvas.create_image(
                    x1, y1, image=self.all_images['black_pawn'], tags=('bP', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                self.board[i][rows[alpha]] = "bP"
                the_piece = Piece(i, rows[alpha], "pawn", piece_id, "B")
                self.game_canvas.tag_bind(
                    piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                Logic.black_pieces.append(the_piece)

    def create_game_pieces(self):
        """ places all the pieces at their starting positions """

        piece_symbol = {"rook": "R", "knight": "N",
                        "king": "K", "queen": "Q", "bishop": "B"}
        rows = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        for alpha in "ABCDEFGH":
            for i in range(8):
                if i == 0:
                    find_tag = self.game_canvas.find_withtag(
                        f"board-{alpha}{i}")
                    tag_coord = self.game_canvas.coords(find_tag[0])
                    get_center = Logic.get_coordinate_center(tag_coord)
                    x1, y1 = get_center
                    piece_type = self.get_piece_color(alpha, i)
                    self.board[i][rows[alpha]] = f"b{piece_symbol[piece_type]}"
                    piece_id = self.game_canvas.create_image(
                        x1, y1, image=self.all_images[f"black_{piece_type}"], tags=(f'b{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                    the_piece = Piece(
                        i, rows[alpha], piece_type, piece_id, "B")
                    self.game_canvas.tag_bind(
                        piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                    Logic.black_pieces.append(the_piece)
                elif i == 1:
                    find_tag = self.game_canvas.find_withtag(
                        f"board-{alpha}{i}")
                    tag_coord = self.game_canvas.coords(find_tag[0])
                    get_center = Logic.get_coordinate_center(tag_coord)
                    x1, y1 = get_center
                    piece_id = self.game_canvas.create_image(
                        x1, y1, image=self.all_images['black_pawn'], tags=('bP', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                    self.board[i][rows[alpha]] = "bP"
                    the_piece = Piece(i, rows[alpha], "pawn", piece_id, "B")
                    self.game_canvas.tag_bind(
                        piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                    Logic.black_pieces.append(the_piece)
                elif i == 6:
                    find_tag = self.game_canvas.find_withtag(
                        f"board-{alpha}{i}")
                    tag_coord = self.game_canvas.coords(find_tag[0])
                    get_center = Logic.get_coordinate_center(tag_coord)
                    x1, y1 = get_center
                    piece_id = self.game_canvas.create_image(
                        x1, y1, image=self.all_images['white_pawn'], tags=('wP', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                    self.board[i][rows[alpha]] = "wP"
                    the_piece = Piece(i, rows[alpha], "pawn", piece_id, "W")
                    self.game_canvas.tag_bind(
                        piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                    Logic.white_pieces.append(the_piece)
                if i == 7:
                    find_tag = self.game_canvas.find_withtag(
                        f"board-{alpha}{i}")
                    tag_coord = self.game_canvas.coords(find_tag[0])
                    get_center = Logic.get_coordinate_center(tag_coord)
                    x1, y1 = get_center
                    piece_type = self.get_piece_color(alpha, i)
                    self.board[i][rows[alpha]] = f"w{piece_symbol[piece_type]}"
                    piece_id = self.game_canvas.create_image(x1, y1, image=self.all_images[f"white_{piece_type}"], tags=(
                        f'w{piece_symbol[piece_type]}', f"{alpha}{i}", f"{i}-{rows[alpha]}"))
                    the_piece = Piece(
                        i, rows[alpha], piece_type, piece_id, "W")
                    self.game_canvas.tag_bind(
                        piece_id, "<Button-1>", lambda x: Logic.handle_piece_click(self))
                    Logic.white_pieces.append(the_piece)

        # Logic.display_board(self.board)

    def get_piece_color(self, alpha, number):
        black_pieces = {"A0": "rook", "B0": "knight", "C0": "bishop", "D0": "queen",
                        "E0": "king", "F0": "bishop", "G0": "knight", "H0": "rook"}
        white_pieces = {"A7": "rook", "B7": "knight", "C7": "bishop", "D7": "queen",
                        "E7": "king", "F7": "bishop", "G7": "knight", "H7": "rook"}

        if number == 0:
            return black_pieces[f"{alpha}{number}"]
        return white_pieces[f"{alpha}{number}"]

    def change_board(self):
        print(self.board_choice.get())

    def change_piece(self):
        print(self.piece_choice.get())

    def set_game_duration(self):
        pass

    def show_promotion_options(self, player_color, square, destination):
        self.promotion_canvas = Canvas(
            bg=self.BOARD_DARK_COLOUR, width=150, height=36)
        self.promotion_canvas.place(relx=0.5, rely=0.026, anchor="center")
        # color = Logic.color_dict[player_color]
        player_color = player_color.lower()

        queen_image = Image.open(f'./assets/pieces/{player_color}Q.png')
        queen_image.thumbnail((30, 30))
        self.queen_image = ImageTk.PhotoImage(queen_image)
        self.queen_label = Label(
            self.promotion_canvas, bg=self.BOARD_DARK_COLOUR, border=0, image=self.queen_image)
        self.queen_label.place(relx=0.05, rely=0.5, anchor="w")
        self.queen_label.bind(
            "<Button-1>", lambda r: self.choose_piece("queen", square, destination))

        rook_image = Image.open(f'./assets/pieces/{player_color}R.png')
        rook_image.thumbnail((26, 26))
        self.rook_image = ImageTk.PhotoImage(rook_image)
        self.rook_label = Label(
            self.promotion_canvas, bg=self.BOARD_DARK_COLOUR, border=0, image=self.rook_image)
        self.rook_label.place(relx=0.3, rely=0.5, anchor="w")
        self.rook_label.bind(
            "<Button-1>", lambda r: self.choose_piece("rook", square, destination))

        knight_image = Image.open(f'./assets/pieces/{player_color}N.png')
        knight_image.thumbnail((27, 27))
        self.knight_image = ImageTk.PhotoImage(knight_image)
        self.knight_label = Label(
            self.promotion_canvas, bg=self.BOARD_DARK_COLOUR, border=0, image=self.knight_image)
        self.knight_label.place(relx=0.52, rely=0.5, anchor="w")
        self.knight_label.bind(
            "<Button-1>", lambda r: self.choose_piece("knight", square, destination))

        bishop_image = Image.open(f'./assets/pieces/{player_color}B.png')
        bishop_image.thumbnail((28, 28))
        self.bishop_image = ImageTk.PhotoImage(bishop_image)
        self.bishop_label = Label(
            self.promotion_canvas, bg=self.BOARD_DARK_COLOUR, border=0, image=self.bishop_image)
        self.bishop_label.place(relx=0.752, rely=0.5, anchor="w")
        self.bishop_label.bind(
            "<Button-1>", lambda r: self.choose_piece("bishop", square, destination))

    def choose_piece(self, piece, square, destination):
        Piece.promotion_choice = piece, square, destination
        Logic.promotion_happenning = True
        Logic.move_piece_to_square(self)

    def show_game_outcome(self, winner, reason=None):
        # print('result in show game outcome:', reason)
        self.game_result_veil = Frame(width=1000, bg="orangered", height=700)
        self.game_result_veil.place(x=0, y=0)
        # ============ APP Background =============
        self.winner_image = Image.open('./assets/bg.jpg')
        self.winner_image = self.winner_image.resize(
            (1000, 700), Image.LANCZOS)
        self.winner_image = ImageTk.PhotoImage(self.winner_image)
        Label(self.game_result_veil, border=0,
              image=self.winner_image).pack()
        winner_canvas = Canvas(self.game_result_veil, width=600, height=400)
        winner_canvas.place(relx=0.5, rely=0.5, anchor="center")
        if winner:
            winner_canvas.create_text(
                310, 160, justify="center", text=f"{winner}", fill="#0A1310", font=('Fiolex Girls', 80))
        else:
            winner_canvas.create_text(
                320, 130, justify="center", text="It is a draw!", fill="#0A1310", font=('Fiolex Girls', 80))
            winner_canvas.create_text(
                305, 200, justify="center", text=f"{reason}", fill="#0A1310", font=('fira code', 12))
        Button(winner_canvas, text='Play again', width=12, font=('fira code medium', 14),
               bd=0, bg='#0A1310', fg='#fff', command=self.start_new_game).place(relx=0.25, rely=0.63, anchor="center")
        Button(winner_canvas, text='View board', width=12, font=('fira code medium', 14),
               bd=0, bg='#0A1310', fg='#fff', command=self.hide_game_result).place(relx=0.5, rely=0.63, anchor="center")
        Button(winner_canvas, text='Exit game', width=12, font=('fira code medium', 14),
               bd=0, bg='#0A1310', fg='#fff', command=lambda: self.master.destroy()).place(relx=0.75, rely=0.63, anchor="center")

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
            Label(self.game_help_veil, text="  ABOUT APP  ", font=("Mosk Bold 700", 22)).place(
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
                "fira code medium", 14), width=15, command=self.hide_game_help_veil).place(relx=0.395, rely=0.72, anchor="center")
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
                "fira code medium", 14), width=18, command=self.hide_game_help_veil).place(relx=0.305, rely=0.78, anchor="center")

    def hide_game_help_veil(self):
        self.game_help_veil.place_forget()

    def hide_promotion_option(self):
        self.promotion_canvas.place_forget()

    def hide_game_result(self):
        self.game_result_veil.place_forget()
        for piece in Piece.white_partner_pieces + Piece.black_partner_pieces:
            the_tag = self.game_canvas.find_withtag(piece)
            self.game_canvas.tag_unbind(the_tag, "<Button-1>")

    def start_new_game(self):
        return self.master.switch_frame(MultiPlayer)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
