from tkinter import Label, Frame, Canvas, Button
from PIL import ImageTk, Image
from .multiplayer_logic import Logic
from .multiplayer_piece import Piece


#  BOARD COLOR SCHEME =============
BOARD_DARK_COLOUR = "#AF8968"
BOARD_LIGHT_COLOUR = "#ECDAB9"


class MultiPlayer(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.master = root
        self.master.title("Naija Checkers")
        self.master.geometry('1000x700+200+20')
        self.master.resizable(0, 0)
        # ============ Starter functions =============
        self.show_app_background()
        self.show_game_icons()
        self.init_all_images()
        Logic.reset_all_variables()
        self.create_game_board()
        # self.create_testing_pieces()
        self.create_game_pieces()

    def show_app_background(self):
        self.bg_image = Image.open('./assets/bg.jpg')
        self.bg_image = self.bg_image.resize((1000, 700), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        Label(self, image=self.bg_image).pack()

    def show_game_icons(self):
        # ======== Help Button ============
        self.help_image = Image.open('./assets/help_icon.png')
        self.help_bg = self.help_image.resize((35, 35), Image.LANCZOS)
        self.help_bg = ImageTk.PhotoImage(self.help_bg)
        Button(image=self.help_bg, bg="#fff", command=self.show_help).place(
            relx=0.95, rely=0.08, anchor="center")

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
            bg=BOARD_DARK_COLOUR, width=625, height=625)
        self.gameboard_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.game_canvas = Canvas(
            self.gameboard_frame, bg=BOARD_DARK_COLOUR, width=600, height=600)
        self.game_canvas.place(relx=0.5, rely=0.5, anchor="center")

        for i, value in enumerate("ABCDEFGHIJ"):
            for j in range(10):
                x0 = (i * 60) + 0.6
                x1 = x0 + 60
                y0 = (j * 60) + 0.6
                y1 = y0 + 60
                if (i + j) % 2 == 0:
                    self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=BOARD_DARK_COLOUR, outline=BOARD_LIGHT_COLOUR, tags=(f"{value}{j}", (j, i)))
                else:
                    self.game_canvas.create_rectangle(
                        x0, y0, x1, y1, fill=BOARD_LIGHT_COLOUR, outline=BOARD_LIGHT_COLOUR)

    def create_testing_pieces(self):
        black_pieces = []
        white_pieces = []
        white_king = [(7, 3), (5, 3), (3, 3)]
        black_king = [(9, 3)]

        for j, i in white_king:
            x1 = (i * 60) + 30 + 0.6
            y1 = (j * 60) + 30 + 0.6
            self.board[j][i] = "WK"
            piece_id = self.game_canvas.create_image(
                x1, y1, image=self.all_images['light_king'], tags=('W', (j, i), f"W{j}{i}", "WKING"))
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
            piece = Piece(j, i, "W", True, piece_id)
            Logic.white_pieces.append((piece_id, piece))

        for j, i in black_king:
            x1 = (i * 60) + 30 + 0.6
            y1 = (j * 60) + 30 + 0.6
            self.board[j][i] = "BK"
            piece_id = self.game_canvas.create_image(
                x1, y1, image=self.all_images['dark_king'], tags=('B', (j, i), f"B{j}{i}", "BKING"))
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
            piece = Piece(j, i, "B", True, piece_id)
            Logic.black_pieces.append((piece_id, piece))

        for j, i in white_pieces:
            x1 = (i * 60) + 30 + 0.6
            y1 = (j * 60) + 30 + 0.6
            self.board[j][i] = "W"
            piece_id = self.game_canvas.create_image(
                x1, y1, image=self.all_images['light_piece'], tags=('W', (j, i), f"W{j}{i}"))
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
            piece = Piece(j, i, "W", False, piece_id)
            Logic.white_pieces.append((piece_id, piece))

        for j, i in black_pieces:
            x1 = (i * 60) + 30 + 0.6
            y1 = (j * 60) + 30 + 0.6
            self.board[j][i] = "B"
            piece_id = self.game_canvas.create_image(
                x1, y1, image=self.all_images['dark_piece'], tags=('B', (j, i), f"B{j}{i}"))
            self.game_canvas.tag_bind(
                piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
            piece = Piece(j, i, "B", False, piece_id)
            Logic.black_pieces.append((piece_id, piece))

        board_copy = [r[:] for r in self.board]
        Logic.all_positions.append(board_copy)

    def create_game_pieces(self):
        """ places all the pieces at their starting positions """

        for i in range(10):
            for j in range(10):
                x1 = (i * 60) + 30 + 0.6
                y1 = (j * 60) + 30 + 0.6
                if j < 4:
                    if (i + j) % 2 == 0:
                        self.board[j][i] = "B"
                        piece_id = self.game_canvas.create_image(
                            x1, y1, image=self.all_images['dark_piece'], tags=('B', (j, i), f"B{j}{i}"))
                        self.game_canvas.tag_bind(
                            piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                        piece = Piece(j, i, "B", False, piece_id)
                        Logic.black_pieces.append((piece_id, piece))

                if j > 5:
                    if (i + j) % 2 == 0:
                        self.board[j][i] = "W"
                        piece_id = self.game_canvas.create_image(
                            x1, y1, image=self.all_images['light_piece'], tags=('W', (j, i), f"W{j}{i}"))
                        self.game_canvas.tag_bind(
                            piece_id, "<Button-1>", lambda e: Logic.handle_piece_click(self))
                        piece = Piece(j, i, "W", False, piece_id)
                        Logic.white_pieces.append((piece_id, piece))

        board_copy = [r[:] for r in self.board]
        Logic.all_positions.append(board_copy)

    def show_help(self):
        self.game_help_veil = Frame(width=1000, height=700)
        self.game_help_veil.place(x=0, y=0)
        # ============ APP Background =============
        self.help_image = Image.open('./assets/bg.jpg')
        self.help_image = self.help_image.resize((1000, 700), Image.LANCZOS)
        self.help_image = ImageTk.PhotoImage(self.help_image)
        Label(self.game_help_veil, border=0,
              image=self.help_image).pack()

        help_canvas = Canvas(self.game_help_veil, width=700,
                             height=500, border=3, relief="ridge", borderwidth=3)
        help_canvas.place(relx=0.5, rely=0.5, anchor='center')
        Label(self.game_help_veil, text="  RULES  ", font=("Mosk Bold 700", 24)).place(
            relx=0.5, rely=0.12, anchor="center")
        a = "A player loses if they cannot move"
        b = "A player loses if all their pieces are captured"
        c = "Pieces may only move diagonally"
        d = "Captures are mandatory (compulsory)"
        e = "If multiple captures can happen, a player may choose"
        f = "Captures are possible in any direction"
        g = "King/Queen may move in any direction"

        help_canvas.create_text(350, 70, justify='center',
                                text=a, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 120, justify='center', text=b, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 170, justify='center', text=c, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 220, justify='center', text=d, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 270, justify='center', text=e, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 320, justify='center', text=f, font=("Mosk Normal 400", 18))
        help_canvas.create_text(
            350, 370, justify='center', text=g, font=("Mosk Normal 400", 18))

        Button(self.game_help_veil, text="Close", bd=0, fg='#fff', bg='#101820', font=("fira code medium",
               14), width=15, command=self.hide_game_help_veil).place(relx=0.5, rely=0.78, anchor="center")

    def hide_game_help_veil(self):
        self.game_help_veil.place_forget()

    def show_game_outcome(self, winner, reason=None):
        self.game_result_veil = Frame(width=1000, height=700)
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
                300, 200, justify="center", text=f"{reason}", fill="#0A1310", font=('fira code', 12))
        Button(winner_canvas, text='Play again', width=14, font=('fira code medium', 14),
               bd=0, bg='#0A1310', fg='#fff', command=self.start_new_game).place(relx=0.33, rely=0.63, anchor="center")
        Button(winner_canvas, text='Exit game', width=16, font=('fira code medium', 14),
               bd=0, bg='#0A1310', fg='#fff', command=lambda: self.master.destroy()).place(relx=0.67, rely=0.63, anchor="center")

    def start_new_game(self):
        return self.master.switch_frame(MultiPlayer)
