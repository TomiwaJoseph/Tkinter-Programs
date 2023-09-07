from tkinter import *
import numpy as np
import random
import math
from tkinter import messagebox


root = Tk
ROW_COUNT = 6
COLUMN_COUNT = 7
GAME_TIME = 0


class Switch(root):
    """ Helps in `switching` windows """

    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(SetTime)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0, y=0, relheight=1, relwidth=1)


class StartPage(Frame):
    """ Displays the startpage of the application """

    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='#1a1a1a')
        self.root = root
        self.root.title("Start Page")
        self.root.geometry('400x500+483+134')
        self.root.resizable(0, 0)
        # # ============== UI ================= #
        # ======= Title =====================
        Label(self.master, text='Connect Four', font=('Concert One', 42),
              fg='#505050', bg='#f2aa4c').place(relx=0.5, rely=0.395, anchor=CENTER)
        Label(self.master, text='Connect Four', font=('Concert One', 42),
              fg='#fff', bg='#1a1a1a').place(relx=0.5, rely=0.39, anchor=CENTER)
        # =========== Buttons ==================
        self.human = Button(self.master, text='Human', width=10, font=('montserrat medium', 14), bd=0,
                            fg='#101820', bg='#fff', command=lambda: self.master.switch_frame(SetTime))
        self.human.place(relx=0.32, rely=0.53, anchor=CENTER)
        self.AI = Button(self.master, text='Computer', width=10, font=('montserrat medium', 14), bd=0,
                         fg='#101820', bg='#fff', command=lambda: self.master.switch_frame(AIPage))
        self.AI.place(relx=0.68, rely=0.53, anchor=CENTER)


class SetTime(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.configure(self, bg='#1a1a1a')
        self.root = root
        self.root.title('Settings Page')
        self.root.geometry('300x300+533+234')
        self.root.resizable(0, 0)
        # ======== Variables ==========
        self.time_variable = StringVar()
        self.time_variable.set("3")
        # ============ UI =============
        Label(text='Mins:', font=('Concert One', 14),
              bg='#1a1a1a', fg='white').place(relx=0.4, rely=0.4, anchor=CENTER)
        self.game_time = Entry(textvariable=self.time_variable, width=4,
                               font=('Concert One', 14), justify=CENTER)
        self.game_time.place(relx=0.6, rely=0.4, anchor=CENTER)

        Button(text='START!', font=('Concert One', 14), bg='#1a1a1a', fg='orange', width=9,
               command=self.start_game).place(relx=0.5, rely=0.55, anchor=CENTER)

    def start_game(self):
        global GAME_TIME
        try:
            game_time = int(self.time_variable.get())
            GAME_TIME = game_time * 60
            self.master.switch_frame(HumanPage)
        except ValueError:
            messagebox.showerror("Error", "Type in a number, stupe!")


class HumanPage(Frame):
    """ Displays the Human vs Human part of the application """

    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='#1a1a1a')
        self.root = root
        self.root.title("Connect Four")
        self.root.geometry('900x600+233+84')
        self.root.resizable(0, 0)
        # ============== UI ================= #
        self.canvas = Canvas(bg='#1a1a1a', width=395, height=430)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.bind("<Button-1>", self.drop_chip)
        self.colors = {1: 'YELLOW', 2: 'RED'}
        self.game_over = False
        self.player_turn = 1
        self.moves = []
        self.winning_directions = []
        self.animation_done = True
        # ======== Chip and Time ============
        self.player1_canvas = Canvas(bg='#1a1a1a', width=150, height=150)
        self.player1_canvas.place(relx=0.15, rely=0.5, anchor=CENTER)
        self.player1_canvas.create_oval(
            50, 20, 100, 70, fill=self.colors.get(1), outline='')
        self.player1_time = Label(
            self.player1_canvas, text="03:23", bg='#1a1a1a', fg='#cbcbcb', font=('Concert One', 32))
        self.player1_time.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.player2_canvas = Canvas(bg='#1a1a1a', width=150, height=150)
        self.player2_canvas.place(relx=0.85, rely=0.5, anchor=CENTER)
        self.player2_canvas.create_oval(
            50, 20, 100, 70, fill=self.colors.get(2), outline='')
        self.player2_time = Label(
            self.player2_canvas, text="03:23", bg='#1a1a1a', fg='#cbcbcb', font=('Concert One', 32))
        self.player2_time.place(relx=0.5, rely=0.7, anchor=CENTER)
        # ======== Back Button ============
        self.the_image = PhotoImage(file='./static/back_arrow.png')
        self.back = self.the_image.subsample(2, 2)
        Button(image=self.back, bg="#fff",
               command=self.go_back).place(x=20, y=20)
        # ======== Undo Button ============
        self.undo_image = PhotoImage(file='./static/undo.png')
        self.undo = self.undo_image.subsample(2, 2)
        self.undo_btn = Button(image=self.undo, bg="#fff",
                               command=self.undo_move)
        self.undo_btn.place(x=850, y=20)
        # ======== Board ============
        self.draw_top_chips()
        self.draw_board()
        self.set_players_time()
        self.start_countdown()
        self.board = self.create_board()

    def set_players_time(self):
        mins, secs = divmod(GAME_TIME, 60)
        self.player1_time.config(text='{:02d}:{:02d}'.format(mins, secs))
        self.player2_time.config(text='{:02d}:{:02d}'.format(mins, secs))
        self.player1_minutes = GAME_TIME
        self.player2_minutes = GAME_TIME

    def undo_move(self):
        try:
            if self.game_over == False and self.moves != []:
                last_move = self.moves.pop()
                chip_to_undo = self.parse_row_col(last_move[0], last_move[1])
                self.drop_piece(
                    self.board, last_move[0], last_move[1], 0)
                self.canvas.delete('chip' + chip_to_undo)
                self.player_turn = 2 if self.player_turn == 1 else 1
                self.redraw_top_chips()
        except IndexError:
            print("Stack Overflow")

    def start_countdown(self):
        if self.player_turn == 1 and self.game_over == False:
            if self.player1_minutes > -1:
                mins, secs = divmod(self.player1_minutes, 60)
                self.player1_time.config(text='{:02d}:{:02d}'.format(
                    mins, secs))
                self.player1_minutes -= 1
                self.player1_time.after(
                    1000, self.start_countdown)
            else:
                self.winner1_label = Label(
                    text=f'{self.colors.get(2)} wins!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                self.winner1_label.place(
                    relx=0.5, rely=0.08, anchor=CENTER)
                self.restart_button = Button(
                    text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                self.restart_button.place(
                    relx=0.5, rely=0.92, anchor=CENTER)
                self.game_over = True
        elif self.player_turn == 2 and self.game_over == False:
            if self.player2_minutes > -1:
                mins, secs = divmod(self.player2_minutes, 60)
                self.player2_time.config(text='{:02d}:{:02d}'.format(
                    mins, secs))
                self.player2_minutes -= 1
                self.player2_time.after(
                    1000, self.start_countdown)
            else:
                self.winner2_label = Label(
                    text=f'{self.colors.get(1)} wins!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                self.winner2_label.place(
                    relx=0.5, rely=0.08, anchor=CENTER)
                self.restart_button = Button(
                    text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                self.restart_button.place(
                    relx=0.5, rely=0.92, anchor=CENTER)
                self.game_over = True

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def draw_winning_line(self, directions):
        orientation = directions[0]
        winning_chips = []
        for i in directions[1]:
            chip_destination = self.canvas.coords(i)
            winning_chips.append(chip_destination)

        if orientation == 'horizontal':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0-3, y0+25, x1+3, y1-25, fill='#1a1a1a', width=3)
        elif orientation == 'vertical':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0+25, y0-3, x1-25, y1+3, fill='#1a1a1a', width=3)
        elif orientation == 'positive':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x1, y0, x0, y1, fill='#1a1a1a', width=3)
        else:
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0, y0, x1, y1, fill='#1a1a1a', width=3)

    def is_valid_location(self, board,  col):
        return board[ROW_COUNT-1][col] == 0

    def clear_board(self):
        self.canvas.delete('all')

        if self.player_turn == 1:
            self.winner1_label.place_forget()
        else:
            self.winner2_label.place_forget()

        self.restart_button.place_forget()
        self.game_over = False
        self.player_turn = 1
        self.winning_directions = []
        self.moves = []
        self.animation_done = True
        self.draw_top_chips()
        self.draw_board()
        self.set_players_time()
        self.start_countdown()
        self.board = self.create_board()

    def parse_row_col(self, row, col):
        positions = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',  6: 'G'
        }
        return f'{positions.get(col)}{row}'

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r, c+1), (r, c+2), (r, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['horizontal', parsed]
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    parsed = []
                    directions = [(r, c), (r+1, c), (r+2, c), (r+3, c)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['vertical', parsed]
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['positive', parsed]
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['negative', parsed]
                    return True

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def redraw_top_chips(self):
        for i in "ABCDEFG":
            self.canvas.delete(i)
        self.draw_top_chips()

    def draw_top_chips(self):
        for index, value in enumerate(list('ABCDEFG')):
            DISTANCE = 55
            x0 = 10 + (index * DISTANCE)
            x1 = 50 + x0
            self.canvas.create_rectangle(
                x0, 10, x1, 60, fill='', outline='')
            self.canvas.create_oval(
                x0, 10, x1, 60, fill=f'{self.colors.get(self.player_turn)}', outline='', tags=value)

    def move_chip(self, disc, dy):
        self.canvas.move(disc, 0, 1)
        pos = self.canvas.coords(disc)
        if pos[1] < dy:
            self.animation_done = False
            self.canvas.after(2, self.move_chip, disc, dy)
        else:
            self.animation_done = True

    def drop_chip(self, event):
        current_tag = self.canvas.gettags('current')
        positions = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,  'G': 6
        }
        if current_tag:
            if current_tag[0] in "ABCDEFG" and self.game_over == False:
                chip_pressed_coordinates = self.canvas.coords(current_tag[0])
                if self.player_turn == 1 and self.animation_done:
                    col = positions.get(current_tag[0])
                    if self.is_valid_location(self.board, col):
                        row = self.get_next_open_row(self.board, col)
                        self.drop_piece(self.board, row, col, self.player_turn)
                        self.moves.append((row, col))
                        chip_pressed = self.parse_row_col(row, col)
                        chip_destination = self.canvas.coords(chip_pressed)
                        y0 = chip_destination[1]
                        p0, q0, p1, q1 = chip_pressed_coordinates[0], chip_pressed_coordinates[
                            1], chip_pressed_coordinates[2], chip_pressed_coordinates[3]
                        disc = self.canvas.create_oval(
                            p0, q0, p1, q1, tags='chip'+chip_pressed, fill=f'{self.colors.get(self.player_turn)}', outline="")
                        self.move_chip(disc, y0)
                        if self.winning_move(self.board, 1):
                            self.winner1_label = Label(
                                text=f'{self.colors.get(self.player_turn)} wins!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                            self.winner1_label.place(
                                relx=0.5, rely=0.08, anchor=CENTER)
                            self.restart_button = Button(
                                text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                            self.restart_button.place(
                                relx=0.5, rely=0.92, anchor=CENTER)
                            self.draw_winning_line(self.winning_directions)
                            self.game_over = True
                        else:
                            self.player_turn = 2
                            self.redraw_top_chips()
                elif self.player_turn == 2 and self.animation_done:
                    col = positions.get(current_tag[0])
                    if self.is_valid_location(self.board, col):
                        row = self.get_next_open_row(self.board, col)
                        self.drop_piece(self.board, row, col, self.player_turn)
                        self.moves.append((row, col))
                        chip_pressed = self.parse_row_col(row, col)
                        chip_destination = self.canvas.coords(chip_pressed)
                        y0 = chip_destination[1]
                        p0, q0, p1, q1 = chip_pressed_coordinates[0], chip_pressed_coordinates[
                            1], chip_pressed_coordinates[2], chip_pressed_coordinates[3]
                        disc = self.canvas.create_oval(
                            p0, q0, p1, q1, tags='chip'+chip_pressed, fill=f'{self.colors.get(self.player_turn)}', outline="")
                        self.move_chip(disc, y0)
                        if self.winning_move(self.board, 2):
                            self.winner2_label = Label(
                                text=f'{self.colors.get(self.player_turn)} wins!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                            self.winner2_label.place(
                                relx=0.5, rely=0.08, anchor=CENTER)
                            self.restart_button = Button(
                                text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                            self.restart_button.place(
                                relx=0.5, rely=0.92, anchor=CENTER)
                            self.draw_winning_line(self.winning_directions)
                            self.game_over = True
                        else:
                            self.player_turn = 1
                            self.redraw_top_chips()

    def draw_board(self):
        for i, letter in enumerate('ABCDEFG'):
            chip_number = 5
            increment = 55
            x0 = 10 + (i * increment)
            x1 = x0 + 50
            for j in range(6):
                INCREMENT = 60
                y0 = 70 + (j * INCREMENT)
                y1 = y0 + 50
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill='gray', outline='', tags=f'{letter}{chip_number}')
                chip_number -= 1

    def go_back(self):
        self.master.switch_frame(StartPage)


class AIPage(Frame):
    """ Displays the Human vs AI part of the application """

    def __init__(self, root):
        Frame.__init__(self, root)
        Frame.config(self, bg='#1a1a1a')
        self.root = root
        self.root.title("Connect Four")
        self.root.geometry('500x600+433+84')
        self.root.resizable(0, 0)
        # ============== UI ================= #
        self.canvas = Canvas(
            bg='#1e90ff', highlightthickness=0, width=400, height=430)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.canvas.bind("<Button-1>", self.drop_chip)
        self.colors = {1: '#fed800', 2: '#f00'}
        self.game_over = False
        self.game_started = False
        self.player_turn = 1
        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.WINDOW_LENGTH = 4
        self.moves = []
        self.winning_directions = []
        # ======== Back Button ============
        self.back_image = PhotoImage(file='./static/back_arrow.png')
        self.back = self.back_image.subsample(2, 2)
        Button(image=self.back, bg="#fff",
               command=self.go_back).place(x=20, y=20)
        # ======== AI Start First? ============
        self.know_if_computer_first = IntVar()
        self.AIfirst = Checkbutton(text='Allow AI to play first', font='montserrat 14', activebackground='#1a1a1a',
                                   activeforeground='#f2aa4c', fg='#f2aa4c', bg='#1a1a1a', var=self.know_if_computer_first, command=self.AI_play_first)
        self.AIfirst.place(anchor=CENTER, relx=0.5, rely=0.055)
        # ======== Undo Button ============
        self.undo_image = PhotoImage(file='./static/undo.png')
        self.undo = self.undo_image.subsample(2, 2)
        self.undo_btn = Button(image=self.undo, bg="#fff",
                               command=self.undo_move)
        self.undo_btn.place(x=450, y=20)
        # ======== Board ============
        self.draw_top_chips()
        self.draw_board()
        self.board = self.create_board()

    def AI_play_first(self):
        check = self.know_if_computer_first.get()
        if check:
            self.player_turn = 2
            self.AIfirst.place_forget()
            self.get_AI_move()

    def draw_winning_line(self, directions):
        orientation = directions[0]
        winning_chips = []
        for i in directions[1]:
            chip_destination = self.canvas.coords(i)
            winning_chips.append(chip_destination)

        if orientation == 'horizontal':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0-3, y0+25, x1+3, y1-25, fill='#1a1a1a', width=3)
        elif orientation == 'vertical':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0+25, y0-3, x1-25, y1+3, fill='#1a1a1a', width=3)
        elif orientation == 'positive':
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x1, y0, x0, y1, fill='#1a1a1a', width=3)
        else:
            for chip in winning_chips:
                x0, y0, x1, y1 = chip[0], chip[1], chip[2], chip[3]
                self.canvas.create_line(
                    x0, y0, x1, y1, fill='#1a1a1a', width=3)

    def get_AI_move(self):
        if self.player_turn == 2 and not self.game_over:
            col, minimax_score = self.minimax(
                self.board, 6, -math.inf, math.inf, True)
            if self.is_valid_location(self.board, col):
                row = self.get_next_open_row(self.board, col)
                self.drop_piece(self.board, row, col, self.AI_PIECE)
                self.moves.append((row, col))
                chip_selected = self.parse_row_col(row, col)
                chip_destination = self.canvas.coords(chip_selected)
                chip_selected_coordinates = self.canvas.coords(
                    chip_selected[0])
                y0 = chip_destination[1]
                p0, q0, p1, q1 = chip_selected_coordinates[0], chip_selected_coordinates[
                    1], chip_selected_coordinates[2], chip_selected_coordinates[3]
                disc = self.canvas.create_oval(
                    p0, q0, p1, q1, tags='chip'+chip_selected, fill=f'{self.colors.get(self.AI_PIECE)}', outline="")
                self.move_chip(disc, y0)
                if self.winning_move(self.board, self.AI_PIECE):
                    self.ai_winner_label = Label(
                        text='AI wins!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                    self.ai_winner_label.place(
                        relx=0.5, rely=0.055, anchor=CENTER)
                    self.restart_button = Button(
                        text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                    self.restart_button.place(
                        relx=0.5, rely=0.92, anchor=CENTER)
                    self.undo_btn.place_forget()
                    self.game_over = True
                    return

                self.player_turn = 1

    def undo_move(self):
        try:
            if len(self.moves) >= 2:
                for i in range(2):
                    last_move = self.moves.pop()
                    chip_to_undo = self.parse_row_col(
                        last_move[0], last_move[1])
                    self.drop_piece(
                        self.board, last_move[0], last_move[1], 0)
                    self.canvas.delete('chip' + chip_to_undo)
            else:
                last_move = self.moves.pop()
                chip_to_undo = self.parse_row_col(last_move[0], last_move[1])
                self.drop_piece(
                    self.board, last_move[0], last_move[1], 0)
                self.canvas.delete('chip' + chip_to_undo)
            if self.moves == []:
                self.know_if_computer_first.set(0)
                self.AIfirst.place(anchor=CENTER, relx=0.5, rely=0.055)
        except IndexError:
            print("Stack Overflow")

    def print_board(self, board):
        print(np.flip(board, 0))

    def create_board(self):
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def clear_board(self):
        self.canvas.delete('all')
        if self.player_turn == 1:
            self.human_winner_label.place_forget()
        else:
            self.ai_winner_label.place_forget()
        self.restart_button.place_forget()
        self.game_over = False
        self.game_started = False
        self.player_turn = 1
        self.moves = []
        self.winning_directions = []
        self.know_if_computer_first.set(0)
        self.AIfirst.place(anchor=CENTER, relx=0.5, rely=0.055)
        self.undo_btn.place(x=450, y=20)
        self.draw_top_chips()
        self.draw_board()
        self.board = self.create_board()

    def parse_row_col(self, row, col):
        positions = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',  6: 'G'
        }
        return f'{positions.get(col)}{row}'

    def is_valid_location(self, board,  col):
        return board[ROW_COUNT-1][col] == 0

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def draw_top_chips(self):
        for index, value in enumerate(list('ABCDEFG')):
            DISTANCE = 55
            x0 = 10 + (index * DISTANCE)
            x1 = 50 + x0
            self.canvas.create_rectangle(
                x0, 10, x1, 60, fill='', outline='')
            self.canvas.create_oval(
                x0, 10, x1, 60, fill=f'{self.colors.get(self.player_turn)}', outline='', tags=value)

    def draw_board(self):
        for i, letter in enumerate('ABCDEFG'):
            chip_number = 5
            increment = 55
            x0 = 10 + (i * increment)
            x1 = x0 + 50
            for j in range(6):
                INCREMENT = 60
                y0 = 70 + (j * INCREMENT)
                y1 = y0 + 50
                self.canvas.create_rectangle(
                    x0, y0, x1, y1, fill='white', outline='', tags=f'{letter}{chip_number}')
                chip_number -= 1

    def move_chip(self, disc, dy):
        self.canvas.move(disc, 0, 1)
        pos = self.canvas.coords(disc)
        try:
            if pos[1] < dy:
                self.canvas.after(2, self.move_chip, disc, dy)
            else:
                if self.game_over == False:
                    if self.player_turn == 2:
                        self.get_AI_move()
                else:
                    self.draw_winning_line(self.winning_directions)
        except IndexError:
            print('Animation truncated midway...')
            print('Wait for your turn...')

    def drop_chip(self, event):
        current_tag = self.canvas.gettags('current')
        positions = {
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5,  'G': 6
        }

        if current_tag:
            if current_tag[0] in "ABCDEFG" and self.player_turn == 1 and self.game_over == False:
                if self.game_started == False:
                    self.AIfirst.place_forget()
                chip_pressed_coordinates = self.canvas.coords(current_tag[0])
                col = positions.get(current_tag[0])
                if self.is_valid_location(self.board, col):
                    row = self.get_next_open_row(self.board, col)
                    self.drop_piece(self.board, row, col, self.PLAYER_PIECE)
                    self.moves.append((row, col))
                    chip_pressed = self.parse_row_col(row, col)
                    chip_destination = self.canvas.coords(chip_pressed)
                    y0 = chip_destination[1]
                    p0, q0, p1, q1 = chip_pressed_coordinates[0], chip_pressed_coordinates[
                        1], chip_pressed_coordinates[2], chip_pressed_coordinates[3]
                    disc = self.canvas.create_oval(
                        p0, q0, p1, q1, tags='chip'+chip_pressed, fill=f'{self.colors.get(self.player_turn)}', outline="")
                    self.move_chip(disc, y0)

                    if self.winning_move(self.board, self.PLAYER_PIECE):
                        self.human_winner_label = Label(
                            text=f'You win. Amazing!!!', fg='#fff', bg='#1a1a1a', font=('Concert One', 20))
                        self.human_winner_label.place(
                            relx=0.5, rely=0.055, anchor=CENTER)
                        self.restart_button = Button(
                            text='Restart', fg='#101820', command=self.clear_board, bg='#fff', font=('Concert One', 18))
                        self.restart_button.place(
                            relx=0.5, rely=0.92, anchor=CENTER)
                        self.game_over = True
                        return

                    self.player_turn = 2

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r, c+1), (r, c+2), (r, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['horizontal', parsed]
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    parsed = []
                    directions = [(r, c), (r+1, c), (r+2, c), (r+3, c)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['vertical', parsed]
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['positive', parsed]
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    parsed = []
                    directions = [(r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)]
                    for i in directions:
                        parsed.append(self.parse_row_col(i[0], i[1]))
                    self.winning_directions = ['negative', parsed]
                    return True

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board, self.PLAYER_PIECE):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(board, self.AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(
                    b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, board, piece):
        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def go_back(self):
        self.master.switch_frame(StartPage)


if __name__ == "__main__":
    app = Switch()
    app.mainloop()
