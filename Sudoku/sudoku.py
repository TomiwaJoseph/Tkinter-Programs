from tkinter import *
from tkinter import messagebox
from random import sample
from random import shuffle as sf


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
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='#101820')
        self.master = master
        self.master.title('Intro Page')
        self.master.geometry('400x300+483+234')
        self.master.resizable(0, 0)
        # ======= Title =====================
        Label(self.master, text='Sudoku', font='poppins 50',
              fg='#505050', bg='#f2aa4c').place(x=75, y=63)
        Label(self.master, text='Sudoku', font='poppins 50',
              fg='#f2aa4c', bg='#101820').place(x=75, y=60)
        # =========== Buttons ==================
        self.start = Button(self.master, text='Start', width=8, font='poppins 14', bd=0, fg='#f2aa4c',
                            bg='#101820', command=lambda: self.master.switch_frame(SelectDifficultyPage))
        self.start.place(x=150, y=160)


class SelectDifficultyPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='#101820')
        self.master = master
        self.master.title('Choose Difficulty')
        self.master.geometry('400x300+483+234')
        self.master.resizable(0, 0)
        # ======== BUttons =============
        Button(text='Easy', font='poppins 16', width=15, fg='#101820', bg='#f2aa4c',
               command=lambda: self.master.switch_frame(EasyPage)).pack(pady=(40, 10))
        Button(text='My Wierd Version', font='poppins 16', width=18, fg='#101820', bg='#f2aa4c',
               command=lambda: self.master.switch_frame(MyWierdVersion)).pack(pady=(0, 10))
        Button(text='Really Hard', font='poppins 16', width=15, fg='#101820', bg='#f2aa4c',
               command=lambda: self.master.switch_frame(ExtremePage)).pack()


class EasyPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='#101820')
        self.master = master
        self.master.title('Sudoku | Easy')
        self.master.geometry('400x400+483+184')
        self.master.resizable(0, 0)
        # ======== Variables ==========
        self.playing_board = []
        self.reach_end = False
        self.num = 0
        self.display_ui()
        self.generate_sudoku()

    def display_ui(self):
        # ========= UI and stuff ===========
        self.row1col1 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col1.place(x=82, y=25)
        self.row1col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col2.place(x=140, y=25)
        self.row1col3 = Button(text='', command=lambda: self.change_numbers(
            self.row1col3), bg='white', fg='red', font='candara 22', width=3)
        self.row1col3.place(x=198, y=25)
        self.row1col4 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col4.place(x=256, y=25)

        self.row2col1 = Button(text='', command=lambda: self.change_numbers(
            self.row2col1), bg='white', fg='red', font='candara 22', width=3)
        self.row2col1.place(x=82, y=88)
        self.row2col2 = Button(text='', command=lambda: self.change_numbers(
            self.row2col2), bg='white', fg='red', font='candara 22', width=3)
        self.row2col2.place(x=140, y=88)
        self.row2col3 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row2col3.place(x=198, y=88)
        self.row2col4 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row2col4.place(x=256, y=88)

        self.row3col1 = Button(text='', command=lambda: self.change_numbers(
            self.row3col1), bg='white', fg='red', font='candara 22', width=3)
        self.row3col1.place(x=82, y=151)
        self.row3col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row3col2.place(x=140, y=151)
        self.row3col3 = Button(text='', command=lambda: self.change_numbers(
            self.row3col3), bg='white', fg='red', font='candara 22', width=3)
        self.row3col3.place(x=198, y=151)
        self.row3col4 = Button(text='', command=lambda: self.change_numbers(
            self.row3col4), bg='white', fg='red', font='candara 22', width=3)
        self.row3col4.place(x=256, y=151)

        self.row4col1 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col1.place(x=82, y=214)
        self.row4col2 = Button(text='', command=lambda: self.change_numbers(
            self.row4col2), bg='white', fg='red', font='candara 22', width=3)
        self.row4col2.place(x=140, y=214)
        self.row4col3 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col3.place(x=198, y=214)
        self.row4col4 = Button(text='', command=lambda: self.change_numbers(
            self.row4col4), bg='white', fg='red', font='candara 22', width=3)
        self.row4col4.place(x=256, y=214)

        Button(text='Submit', command=self.check_if_solved, fg='#101820', bg='#f2aa4c', width=15,
               font='montserrat 14').place(anchor=CENTER, relx=0.5, rely=0.77)
        Button(text='Hard Mode', command=lambda: self.master.switch_frame(ExtremePage),
               width=14, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=205, y=340)
        Button(text='My Wierd Mode', command=lambda: self.master.switch_frame(MyWierdVersion),
               width=14, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=15, y=340)

    def change_numbers(self, button):
        if self.num == 4:
            self.reach_end = True
        if self.num == 1:
            self.reach_end = False
        if not self.reach_end:
            self.num += 1
            button.config(text=self.num)
        if self.reach_end:
            self.num -= 1
            button.config(text=self.num)

    def generate_sudoku(self):
        self.playing_board = []
        self.row1col3['text'] = ''
        self.row2col1['text'] = ''
        self.row2col2['text'] = ''
        self.row3col1['text'] = ''
        self.row3col3['text'] = ''
        self.row3col4['text'] = ''
        self.row4col2['text'] = ''
        self.row4col4['text'] = ''

        base = 2
        side = base*base

        def pattern(r, c):
            return (base*(r % base) + r//base+c) % side

        def shuffle(s):
            return sample(s, len(s))
        rbase = range(base)
        rows = [g*base + r for g in shuffle(rbase) for r in shuffle(rbase)]
        cols = [g*base + c for g in shuffle(rbase) for c in shuffle(rbase)]
        nums = shuffle(range(1, base*base+1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        self.playing_board += board

        self.row1col1.config(text=self.playing_board[0][0])
        self.row1col2.config(text=self.playing_board[0][1])
        self.row1col4.config(text=self.playing_board[0][3])
        self.row2col3.config(text=self.playing_board[1][2])
        self.row2col4.config(text=self.playing_board[1][3])
        self.row3col2.config(text=self.playing_board[2][1])
        self.row4col1.config(text=self.playing_board[3][0])
        self.row4col3.config(text=self.playing_board[3][2])

    def check_if_solved(self):
        # known
        k1 = self.row1col1['text']
        k2 = self.row1col2['text']
        k3 = self.row1col4['text']
        k4 = self.row2col3['text']
        k5 = self.row2col4['text']
        k6 = self.row3col2['text']
        k7 = self.row4col1['text']
        k8 = self.row4col3['text']
        # player input
        u1 = self.row1col3['text']
        u2 = self.row2col1['text']
        u3 = self.row2col2['text']
        u4 = self.row3col1['text']
        u5 = self.row3col3['text']
        u6 = self.row3col4['text']
        u7 = self.row4col2['text']
        u8 = self.row4col4['text']

        player_board = [
            [k1, k2, u1, k3],
            [u2, u3, k4, k5],
            [u4, k6, u5, u6],
            [k7, u7, k8, u8]
        ]

        if player_board == self.playing_board:
            messagebox.showinfo('Solved', 'Congratulations! You solved it.')
            self.generate_sudoku()
        else:
            messagebox.showinfo('Unsolved', 'Not quite there yet.')


class MyWierdVersion(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='#101820')
        self.master = master
        self.master.title('Sudoku | My Wierd Version')
        self.master.geometry('520x540+423+114')
        self.master.resizable(0, 0)
        # ========= UI and stuff ===========
        self.row1col1 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col1.place(x=82, y=25)
        self.row1col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col2.place(x=140, y=25)
        self.row1col3 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col3.place(x=198, y=25)
        self.row1col4 = Button(text='', command=lambda: self.change_numbers(
            self.row1col4), bg='white', fg='red', font='candara 22', width=3)
        self.row1col4.place(x=256, y=25)
        self.row1col5 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row1col5.place(x=314, y=25)
        self.row1col6 = Button(text='', command=lambda: self.change_numbers(
            self.row1col6), bg='white', fg='red', font='candara 22', width=3)
        self.row1col6.place(x=372, y=25)

        self.row2col1 = Button(text='', command=lambda: self.change_numbers(
            self.row2col1), bg='white', fg='red', font='candara 22', width=3)
        self.row2col1.place(x=82, y=88)
        self.row2col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row2col2.place(x=140, y=88)
        self.row2col3 = Button(text='', command=lambda: self.change_numbers(
            self.row2col3), bg='white', fg='red', font='candara 22', width=3)
        self.row2col3.place(x=198, y=88)
        self.row2col4 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row2col4.place(x=256, y=88)
        self.row2col5 = Button(text='', command=lambda: self.change_numbers(
            self.row2col5), bg='white', fg='red', font='candara 22', width=3)
        self.row2col5.place(x=314, y=88)
        self.row2col6 = Button(text='', command=lambda: self.change_numbers(
            self.row2col6), bg='white', fg='red', font='candara 22', width=3)
        self.row2col6.place(x=372, y=88)

        self.row3col1 = Button(text='', command=lambda: self.change_numbers(
            self.row3col1), bg='white', fg='red', font='candara 22', width=3)
        self.row3col1.place(x=82, y=151)
        self.row3col2 = Button(text='', command=lambda: self.change_numbers(
            self.row3col2), bg='white', fg='red', font='candara 22', width=3)
        self.row3col2.place(x=140, y=151)
        self.row3col3 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row3col3.place(x=198, y=151)
        self.row3col4 = Button(text='', command=lambda: self.change_numbers(
            self.row3col4), bg='white', fg='red', font='candara 22', width=3)
        self.row3col4.place(x=256, y=151)
        self.row3col5 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row3col5.place(x=314, y=151)
        self.row3col6 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row3col6.place(x=372, y=151)

        self.row4col1 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col1.place(x=82, y=214)
        self.row4col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col2.place(x=140, y=214)
        self.row4col3 = Button(text='', command=lambda: self.change_numbers(
            self.row4col3), bg='white', fg='red', font='candara 22', width=3)
        self.row4col3.place(x=198, y=214)
        self.row4col4 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col4.place(x=256, y=214)
        self.row4col5 = Button(text='', command=lambda: self.change_numbers(
            self.row4col5), bg='white', fg='red', font='candara 22', width=3)
        self.row4col5.place(x=314, y=214)
        self.row4col6 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row4col6.place(x=372, y=214)

        self.row5col1 = Button(text='', command=lambda: self.change_numbers(
            self.row5col1), bg='white', fg='red', font='candara 22', width=3)
        self.row5col1.place(x=82, y=277)
        self.row5col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row5col2.place(x=140, y=277)
        self.row5col3 = Button(text='', command=lambda: self.change_numbers(
            self.row5col3), bg='white', fg='red', font='candara 22', width=3)
        self.row5col3.place(x=198, y=277)
        self.row5col4 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row5col4.place(x=256, y=277)
        self.row5col5 = Button(text='', command=lambda: self.change_numbers(
            self.row5col5), bg='white', fg='red', font='candara 22', width=3)
        self.row5col5.place(x=314, y=277)
        self.row5col6 = Button(text='', command=lambda: self.change_numbers(
            self.row5col6), bg='white', fg='red', font='candara 22', width=3)
        self.row5col6.place(x=372, y=277)

        self.row6col1 = Button(text='', command=lambda: self.change_numbers(
            self.row6col1), bg='white', fg='red', font='candara 22', width=3)
        self.row6col1.place(x=82, y=340)
        self.row6col2 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row6col2.place(x=140, y=340)
        self.row6col3 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row6col3.place(x=198, y=340)
        self.row6col4 = Button(text='', command=lambda: self.change_numbers(
            self.row6col4), bg='white', fg='red', font='candara 22', width=3)
        self.row6col4.place(x=256, y=340)
        self.row6col5 = Button(text='', command=lambda: self.change_numbers(
            self.row6col5), bg='white', fg='red', font='candara 22', width=3)
        self.row6col5.place(x=314, y=340)
        self.row6col6 = Button(text='', bg='white',
                               fg='#101820', font='candara 22', width=3)
        self.row6col6.place(x=372, y=340)

        Button(text='Submit', command=self.check_if_solved, fg='#101820', bg='#f2aa4c', width=15,
               font='montserrat 14').place(anchor=CENTER, relx=0.5, rely=0.805)
        Button(text='Easy Mode', command=lambda: self.master.switch_frame(EasyPage),
               width=14, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=70, y=468)
        Button(text='Hard Mode', command=lambda: self.master.switch_frame(ExtremePage),
               width=14, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=260, y=468)
        # ======== Variables ==========
        self.grid = [[0 for i in range(6)] for j in range(6)]
        self.playing_board = []
        self.reach_end = False
        self.num = 0
        self.display_board()

    def display_board(self):
        self.playing_board = []
        self.grid = [[0 for i in range(6)] for j in range(6)]
        self.generate_sudoku(self.grid)
        self.playing_board += self.grid

        self.row1col4['text'] = ''
        self.row1col6['text'] = ''

        self.row2col1['text'] = ''
        self.row2col3['text'] = ''
        self.row2col5['text'] = ''
        self.row2col6['text'] = ''

        self.row3col1['text'] = ''
        self.row3col2['text'] = ''
        self.row3col4['text'] = ''

        self.row4col3['text'] = ''
        self.row4col5['text'] = ''

        self.row5col1['text'] = ''
        self.row5col3['text'] = ''
        self.row5col5['text'] = ''
        self.row5col6['text'] = ''

        self.row6col1['text'] = ''
        self.row6col4['text'] = ''
        self.row6col5['text'] = ''

        self.row1col1.config(text=self.playing_board[0][0])
        self.row1col2.config(text=self.playing_board[0][1])
        self.row1col3.config(text=self.playing_board[0][2])
        self.row1col5.config(text=self.playing_board[0][4])

        self.row2col2.config(text=self.playing_board[1][1])
        self.row2col4.config(text=self.playing_board[1][3])

        self.row3col3.config(text=self.playing_board[2][2])
        self.row3col5.config(text=self.playing_board[2][4])
        self.row3col6.config(text=self.playing_board[2][5])

        self.row4col1.config(text=self.playing_board[3][0])
        self.row4col2.config(text=self.playing_board[3][1])
        self.row4col4.config(text=self.playing_board[3][3])
        self.row4col6.config(text=self.playing_board[3][5])

        self.row5col2.config(text=self.playing_board[4][1])
        self.row5col4.config(text=self.playing_board[4][3])

        self.row6col2.config(text=self.playing_board[5][1])
        self.row6col3.config(text=self.playing_board[5][2])
        self.row6col6.config(text=self.playing_board[5][5])

    def change_numbers(self, button):
        if self.num == 6:
            self.reach_end = True
        if self.num == 1:
            self.reach_end = False
        if not self.reach_end:
            self.num += 1
            button.config(text=self.num)
        if self.reach_end:
            self.num -= 1
            button.config(text=self.num)

    def generate_sudoku(self, grid):
        number_list = [*range(1, 7)]
        for i in range(0, 36):
            row = i//6
            col = i % 6
            if grid[row][col] == 0:
                sf(number_list)
                for number in number_list:
                    if self.valid_location(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_sudoku(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def valid_location(self, grid, row, col, number):
        if self.num_used_in_row(grid, row, number):
            return False
        elif self.num_used_in_column(grid, col, number):
            return False
        return True

    def find_empty_square(self, grid):
        for i in range(6):
            for j in range(6):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def num_used_in_row(self, grid, row, number):
        if number in grid[row]:
            return True
        return False

    def num_used_in_column(self, grid, col, number):
        for i in range(6):
            if grid[i][col] == number:
                return True
        return False

    def check_if_solved(self):
        # known
        k1 = self.row1col1['text']
        k2 = self.row1col2['text']
        k3 = self.row1col3['text']
        k4 = self.row1col5['text']
        k5 = self.row2col2['text']
        k6 = self.row2col4['text']
        k7 = self.row3col3['text']
        k8 = self.row3col5['text']
        k9 = self.row3col6['text']
        k11 = self.row4col1['text']
        k12 = self.row4col2['text']
        k13 = self.row4col4['text']
        k14 = self.row4col6['text']
        k15 = self.row5col2['text']
        k16 = self.row5col4['text']
        k17 = self.row6col2['text']
        k18 = self.row6col3['text']
        k19 = self.row6col6['text']
        # player input
        u1 = self.row1col4['text']
        u2 = self.row1col6['text']
        u3 = self.row2col1['text']
        u4 = self.row2col3['text']
        u5 = self.row2col5['text']
        u6 = self.row2col6['text']
        u7 = self.row3col1['text']
        u8 = self.row3col2['text']
        u9 = self.row3col4['text']
        u10 = self.row4col3['text']
        u11 = self.row4col5['text']
        u12 = self.row5col1['text']
        u13 = self.row5col3['text']
        u14 = self.row5col5['text']
        u15 = self.row5col6['text']
        u16 = self.row6col1['text']
        u17 = self.row6col4['text']
        u18 = self.row6col5['text']

        player_board = [
            [k1, k2, k3, u1, k4, u2],
            [u3, k5, u4, k6, u5, u6],
            [u7, u8, k7, u9, k8, k9],
            [k11, k12, u10, k13, u11, k14],
            [u12, k15, u13, k16, u14, u15],
            [u16, k17, k18, u17, u18, k19]
        ]

        if player_board == self.playing_board:
            messagebox.showinfo('Solved', 'Congratulations! You solved it.')
            self.display_board()
        else:
            messagebox.showinfo('Unsolved', 'Not quite there yet.')


class ExtremePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Frame.configure(self, bg='#101820')
        self.master = master
        self.master.title('Sudoku | Really Hard')
        self.master.geometry('698x710+334+29')
        self.master.resizable(0, 0)

        # ======== Variables ==========
        self.playing_board = []
        self.reach_end = False
        self.num = 0
        self.display_ui()
        self.generate_sudoku()

    def display_ui(self):
        # ========= UI and stuff ===========
        self.row1col1 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row1col1.place(x=82, y=25)
        self.row1col2 = Button(text='8', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row1col2.place(x=140, y=25)
        self.row1col3 = Button(text='', command=lambda: self.change_numbers(
            self.row1col3), bg='white', fg='red', font='candara 22', width=3)
        self.row1col3.place(x=198, y=25)
        self.row1col4 = Button(text='4', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row1col4.place(x=256, y=25)
        self.row1col5 = Button(text='', command=lambda: self.change_numbers(
            self.row1col5), bg='white', fg='red', font='candara 22', width=3)
        self.row1col5.place(x=314, y=25)
        self.row1col6 = Button(text='', command=lambda: self.change_numbers(
            self.row1col6), bg='white', fg='red', font='candara 22', width=3)
        self.row1col6.place(x=372, y=25)
        self.row1col7 = Button(text='1', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row1col7.place(x=430, y=25)
        self.row1col8 = Button(text='2', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row1col8.place(x=488, y=25)
        self.row1col9 = Button(text='', command=lambda: self.change_numbers(
            self.row1col9), bg='white', fg='red', font='candara 22', width=3)
        self.row1col9.place(x=546, y=25)

        self.row2col1 = Button(text='6', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row2col1.place(x=82, y=88)
        self.row2col2 = Button(text='', command=lambda: self.change_numbers(
            self.row2col2), bg='white', fg='red', font='candara 22', width=3)
        self.row2col2.place(x=140, y=88)
        self.row2col3 = Button(text='', command=lambda: self.change_numbers(
            self.row2col3), bg='white', fg='red', font='candara 22', width=3)
        self.row2col3.place(x=198, y=88)
        self.row2col4 = Button(text='', command=lambda: self.change_numbers(
            self.row2col4), bg='white', fg='red', font='candara 22', width=3)
        self.row2col4.place(x=256, y=88)
        self.row2col5 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row2col5.place(x=314, y=88)
        self.row2col6 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row2col6.place(x=372, y=88)
        self.row2col7 = Button(text='', command=lambda: self.change_numbers(
            self.row2col7), bg='white', fg='red', font='candara 22', width=3)
        self.row2col7.place(x=430, y=88)
        self.row2col8 = Button(text='', command=lambda: self.change_numbers(
            self.row2col8), bg='white', fg='red', font='candara 22', width=3)
        self.row2col8.place(x=488, y=88)
        self.row2col9 = Button(text='9', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row2col9.place(x=546, y=88)

        self.row3col1 = Button(text='', command=lambda: self.change_numbers(
            self.row3col1), bg='white', fg='red', font='candara 22', width=3)
        self.row3col1.place(x=82, y=151)
        self.row3col2 = Button(text='', command=lambda: self.change_numbers(
            self.row3col2), bg='white', fg='red', font='candara 22', width=3)
        self.row3col2.place(x=140, y=151)
        self.row3col3 = Button(text='', command=lambda: self.change_numbers(
            self.row3col3), bg='white', fg='red', font='candara 22', width=3)
        self.row3col3.place(x=198, y=151)
        self.row3col4 = Button(text='6', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row3col4.place(x=256, y=151)
        self.row3col5 = Button(text='', command=lambda: self.change_numbers(
            self.row3col5), bg='white', fg='red', font='candara 22', width=3)
        self.row3col5.place(x=314, y=151)
        self.row3col6 = Button(text='1', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row3col6.place(x=372, y=151)
        self.row3col7 = Button(text='', command=lambda: self.change_numbers(
            self.row3col7), bg='white', fg='red', font='candara 22', width=3)
        self.row3col7.place(x=430, y=151)
        self.row3col8 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row3col8.place(x=488, y=151)
        self.row3col9 = Button(text='8', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row3col9.place(x=546, y=151)

        self.row4col1 = Button(text='', command=lambda: self.change_numbers(
            self.row4col1), bg='white', fg='red', font='candara 22', width=3)
        self.row4col1.place(x=82, y=214)
        self.row4col2 = Button(text='', command=lambda: self.change_numbers(
            self.row4col2), bg='white', fg='red', font='candara 22', width=3)
        self.row4col2.place(x=140, y=214)
        self.row4col3 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row4col3.place(x=198, y=214)
        self.row4col4 = Button(text='', command=lambda: self.change_numbers(
            self.row4col4), bg='white', fg='red', font='candara 22', width=3)
        self.row4col4.place(x=256, y=214)
        self.row4col5 = Button(text='4', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row4col5.place(x=314, y=214)
        self.row4col6 = Button(text='', command=lambda: self.change_numbers(
            self.row4col6), bg='white', fg='red', font='candara 22', width=3)
        self.row4col6.place(x=372, y=214)
        self.row4col7 = Button(text='2', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row4col7.place(x=430, y=214)
        self.row4col8 = Button(text='6', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row4col8.place(x=488, y=214)
        self.row4col9 = Button(text='', command=lambda: self.change_numbers(
            self.row4col9), bg='white', fg='red', font='candara 22', width=3)
        self.row4col9.place(x=546, y=214)

        self.row5col1 = Button(text='', command=lambda: self.change_numbers(
            self.row5col1), bg='white', fg='red', font='candara 22', width=3)
        self.row5col1.place(x=82, y=277)
        self.row5col2 = Button(text='', command=lambda: self.change_numbers(
            self.row5col2), bg='white', fg='red', font='candara 22', width=3)
        self.row5col2.place(x=140, y=277)
        self.row5col3 = Button(text='1', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row5col3.place(x=198, y=277)
        self.row5col4 = Button(text='', command=lambda: self.change_numbers(
            self.row5col4), bg='white', fg='red', font='candara 22', width=3)
        self.row5col4.place(x=256, y=277)
        self.row5col5 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row5col5.place(x=314, y=277)
        self.row5col6 = Button(text='', command=lambda: self.change_numbers(
            self.row5col6), bg='white', fg='red', font='candara 22', width=3)
        self.row5col6.place(x=372, y=277)
        self.row5col7 = Button(text='9', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row5col7.place(x=430, y=277)
        self.row5col8 = Button(text='3', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row5col8.place(x=488, y=277)
        self.row5col9 = Button(text='', command=lambda: self.change_numbers(
            self.row5col9), bg='white', fg='red', font='candara 22', width=3)
        self.row5col9.place(x=546, y=277)

        self.row6col1 = Button(text='9', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row6col1.place(x=82, y=340)
        self.row6col2 = Button(text='', command=lambda: self.change_numbers(
            self.row6col2), bg='white', fg='red', font='candara 22', width=3)
        self.row6col2.place(x=140, y=340)
        self.row6col3 = Button(text='4', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row6col3.place(x=198, y=340)
        self.row6col4 = Button(text='', command=lambda: self.change_numbers(
            self.row6col4), bg='white', fg='red', font='candara 22', width=3)
        self.row6col4.place(x=256, y=340)
        self.row6col5 = Button(text='6', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row6col5.place(x=314, y=340)
        self.row6col6 = Button(text='', command=lambda: self.change_numbers(
            self.row6col6), bg='white', fg='red', font='candara 22', width=3)
        self.row6col6.place(x=372, y=340)
        self.row6col7 = Button(text='', command=lambda: self.change_numbers(
            self.row6col7), bg='white', fg='red', font='candara 22', width=3)
        self.row6col7.place(x=430, y=340)
        self.row6col8 = Button(text='', command=lambda: self.change_numbers(
            self.row6col8), bg='white', fg='red', font='candara 22', width=3)
        self.row6col8.place(x=488, y=340)
        self.row6col9 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row6col9.place(x=546, y=340)

        self.row7col1 = Button(text='', command=lambda: self.change_numbers(
            self.row7col1), bg='white', fg='red', font='candara 22', width=3)
        self.row7col1.place(x=82, y=403)
        self.row7col2 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row7col2.place(x=140, y=403)
        self.row7col3 = Button(text='', command=lambda: self.change_numbers(
            self.row7col3), bg='white', fg='red', font='candara 22', width=3)
        self.row7col3.place(x=198, y=403)
        self.row7col4 = Button(text='3', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row7col4.place(x=256, y=403)
        self.row7col5 = Button(text='', command=lambda: self.change_numbers(
            self.row7col5), bg='white', fg='red', font='candara 22', width=3)
        self.row7col5.place(x=314, y=403)
        self.row7col6 = Button(text='', command=lambda: self.change_numbers(
            self.row7col6), bg='white', fg='red', font='candara 22', width=3)
        self.row7col6.place(x=372, y=403)
        self.row7col7 = Button(text='', command=lambda: self.change_numbers(
            self.row7col7), bg='white', fg='red', font='candara 22', width=3)
        self.row7col7.place(x=430, y=403)
        self.row7col8 = Button(text='1', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row7col8.place(x=488, y=403)
        self.row7col9 = Button(text='2', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row7col9.place(x=546, y=403)

        self.row8col1 = Button(text='1', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row8col1.place(x=82, y=466)
        self.row8col2 = Button(text='2', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row8col2.place(x=140, y=466)
        self.row8col3 = Button(text='', command=lambda: self.change_numbers(
            self.row8col3), bg='white', fg='red', font='candara 22', width=3)
        self.row8col3.place(x=198, y=466)
        self.row8col4 = Button(text='', command=lambda: self.change_numbers(
            self.row8col4), bg='white', fg='red', font='candara 22', width=3)
        self.row8col4.place(x=256, y=466)
        self.row8col5 = Button(text='', command=lambda: self.change_numbers(
            self.row8col5), bg='white', fg='red', font='candara 22', width=3)
        self.row8col5.place(x=314, y=466)
        self.row8col6 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row8col6.place(x=372, y=466)
        self.row8col7 = Button(text='4', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row8col7.place(x=430, y=466)
        self.row8col8 = Button(text='', command=lambda: self.change_numbers(
            self.row8col8), bg='white', fg='red', font='candara 22', width=3)
        self.row8col8.place(x=488, y=466)
        self.row8col9 = Button(text='', command=lambda: self.change_numbers(
            self.row8col9), bg='white', fg='red', font='candara 22', width=3)
        self.row8col9.place(x=546, y=466)

        self.row9col1 = Button(text='', command=lambda: self.change_numbers(
            self.row9col1), bg='white', fg='red', font='candara 22', width=3)
        self.row9col1.place(x=82, y=529)
        self.row9col2 = Button(text='4', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row9col2.place(x=140, y=529)
        self.row9col3 = Button(text='9', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row9col3.place(x=198, y=529)
        self.row9col4 = Button(text='2', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row9col4.place(x=256, y=529)
        self.row9col5 = Button(text='', command=lambda: self.change_numbers(
            self.row9col5), bg='white', fg='red', font='candara 22', width=3)
        self.row9col5.place(x=314, y=529)
        self.row9col6 = Button(text='6', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row9col6.place(x=372, y=529)
        self.row9col7 = Button(text='', command=lambda: self.change_numbers(
            self.row9col7), bg='white', fg='red', font='candara 22', width=3)
        self.row9col7.place(x=430, y=529)
        self.row9col8 = Button(text='', command=lambda: self.change_numbers(
            self.row9col8), bg='white', fg='red', font='candara 22', width=3)
        self.row9col8.place(x=488, y=529)
        self.row9col9 = Button(text='', bg='white',
                               fg='teal', font='candara 22', width=3)
        self.row9col9.place(x=546, y=529)

        Button(text='Submit', command=self.check_if_solved, fg='#101820', bg='#f2aa4c', width=30,
               font='montserrat 14').place(anchor=CENTER, relx=0.5, rely=0.877)
        Button(text='Easy Mode', command=lambda: self.master.switch_frame(EasyPage),
               width=22, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=65, y=653)
        Button(text='My Wierd Mode', command=lambda: self.master.switch_frame(MyWierdVersion),
               width=22, fg='#101820', bg='#f2aa4c', font='montserrat 14').place(x=350, y=653)

    def change_numbers(self, button):
        if self.num == 9:
            self.reach_end = True
        if self.num == 1:
            self.reach_end = False
        if not self.reach_end:
            self.num += 1
            button.config(text=self.num)
        if self.reach_end:
            self.num -= 1
            button.config(text=self.num)

    def generate_sudoku(self):
        self.playing_board = []
        self.row1col3['text'] = ''
        self.row1col5['text'] = ''
        self.row1col6['text'] = ''
        self.row1col9['text'] = ''
        self.row2col2['text'] = ''
        self.row2col3['text'] = ''
        self.row2col4['text'] = ''
        self.row2col7['text'] = ''
        self.row2col8['text'] = ''
        self.row3col1['text'] = ''
        self.row3col2['text'] = ''
        self.row3col3['text'] = ''
        self.row3col5['text'] = ''
        self.row3col7['text'] = ''
        self.row4col1['text'] = ''
        self.row4col2['text'] = ''
        self.row4col4['text'] = ''
        self.row4col6['text'] = ''
        self.row4col9['text'] = ''
        self.row5col1['text'] = ''
        self.row5col2['text'] = ''
        self.row5col4['text'] = ''
        self.row5col6['text'] = ''
        self.row5col9['text'] = ''
        self.row6col2['text'] = ''
        self.row6col4['text'] = ''
        self.row6col6['text'] = ''
        self.row6col7['text'] = ''
        self.row6col8['text'] = ''
        self.row7col1['text'] = ''
        self.row7col3['text'] = ''
        self.row7col4['text'] = ''
        self.row7col5['text'] = ''
        self.row7col6['text'] = ''
        self.row7col7['text'] = ''
        self.row8col3['text'] = ''
        self.row8col4['text'] = ''
        self.row8col5['text'] = ''
        self.row8col8['text'] = ''
        self.row8col9['text'] = ''
        self.row9col1['text'] = ''
        self.row9col5['text'] = ''
        self.row9col7['text'] = ''
        self.row9col8['text'] = ''

        base = 3
        side = base*base

        def pattern(r, c):
            return (base*(r % base) + r//base+c) % side

        def shuffle(s):
            return sample(s, len(s))
        rbase = range(base)
        rows = [g*base + r for g in shuffle(rbase) for r in shuffle(rbase)]
        cols = [g*base + c for g in shuffle(rbase) for c in shuffle(rbase)]
        nums = shuffle(range(1, base*base+1))

        board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        self.playing_board += board
        self.row1col1.config(text=self.playing_board[0][0])
        self.row1col2.config(text=self.playing_board[0][1])
        self.row1col4.config(text=self.playing_board[0][3])
        self.row1col7.config(text=self.playing_board[0][6])
        self.row1col8.config(text=self.playing_board[0][7])
        self.row2col1.config(text=self.playing_board[1][0])
        self.row2col5.config(text=self.playing_board[1][4])
        self.row2col6.config(text=self.playing_board[1][5])
        self.row2col9.config(text=self.playing_board[1][8])
        self.row3col4.config(text=self.playing_board[2][3])
        self.row3col6.config(text=self.playing_board[2][5])
        self.row3col8.config(text=self.playing_board[2][7])
        self.row3col9.config(text=self.playing_board[2][8])
        self.row4col3.config(text=self.playing_board[3][2])
        self.row4col5.config(text=self.playing_board[3][4])
        self.row4col7.config(text=self.playing_board[3][6])
        self.row4col8.config(text=self.playing_board[3][7])
        self.row5col3.config(text=self.playing_board[4][2])
        self.row5col5.config(text=self.playing_board[4][4])
        self.row5col7.config(text=self.playing_board[4][6])
        self.row5col8.config(text=self.playing_board[4][7])
        self.row6col1.config(text=self.playing_board[5][0])
        self.row6col3.config(text=self.playing_board[5][2])
        self.row6col5.config(text=self.playing_board[5][4])
        self.row6col9.config(text=self.playing_board[5][8])
        self.row7col2.config(text=self.playing_board[6][1])
        self.row7col4.config(text=self.playing_board[6][3])
        self.row7col8.config(text=self.playing_board[6][7])
        self.row7col9.config(text=self.playing_board[6][8])
        self.row8col1.config(text=self.playing_board[7][0])
        self.row8col2.config(text=self.playing_board[7][1])
        self.row8col6.config(text=self.playing_board[7][5])
        self.row8col7.config(text=self.playing_board[7][6])
        self.row9col2.config(text=self.playing_board[8][1])
        self.row9col3.config(text=self.playing_board[8][2])
        self.row9col4.config(text=self.playing_board[8][3])
        self.row9col6.config(text=self.playing_board[8][5])
        self.row9col9.config(text=self.playing_board[8][8])

    def check_if_solved(self):
        # known
        k1 = self.row1col1['text']
        k2 = self.row1col2['text']
        k3 = self.row1col4['text']
        k4 = self.row1col7['text']
        k5 = self.row1col8['text']
        k6 = self.row2col1['text']
        k7 = self.row2col5['text']
        k8 = self.row2col6['text']
        k9 = self.row2col9['text']
        k10 = self.row3col4['text']
        k11 = self.row3col6['text']
        k12 = self.row3col8['text']
        k13 = self.row3col9['text']
        k14 = self.row4col3['text']
        k15 = self.row4col5['text']
        k16 = self.row4col7['text']
        k17 = self.row4col8['text']
        k20 = self.row5col3['text']
        k21 = self.row5col5['text']
        k22 = self.row5col7['text']
        k23 = self.row5col8['text']
        k25 = self.row6col1['text']
        k26 = self.row6col3['text']
        k27 = self.row6col5['text']
        k28 = self.row6col9['text']
        k30 = self.row7col2['text']
        k31 = self.row7col4['text']
        k32 = self.row7col8['text']
        k33 = self.row7col9['text']
        k35 = self.row8col1['text']
        k36 = self.row8col2['text']
        k37 = self.row8col6['text']
        k38 = self.row8col7['text']
        k40 = self.row9col2['text']
        k41 = self.row9col3['text']
        k42 = self.row9col4['text']
        k43 = self.row9col6['text']
        k44 = self.row9col9['text']
        # player input
        u1 = self.row1col3['text']
        u2 = self.row1col5['text']
        u3 = self.row1col6['text']
        u4 = self.row1col9['text']
        u5 = self.row2col2['text']
        u6 = self.row2col3['text']
        u7 = self.row2col4['text']
        u8 = self.row2col7['text']
        u9 = self.row2col8['text']
        u10 = self.row3col1['text']
        u11 = self.row3col2['text']
        u12 = self.row3col3['text']
        u13 = self.row3col5['text']
        u14 = self.row3col7['text']
        u15 = self.row4col1['text']
        u16 = self.row4col2['text']
        u17 = self.row4col4['text']
        u18 = self.row4col6['text']
        u19 = self.row4col9['text']
        u20 = self.row5col1['text']
        u21 = self.row5col2['text']
        u22 = self.row5col4['text']
        u23 = self.row5col6['text']
        u24 = self.row5col9['text']
        u25 = self.row6col2['text']
        u26 = self.row6col4['text']
        u27 = self.row6col6['text']
        u28 = self.row6col7['text']
        u29 = self.row6col8['text']
        u30 = self.row7col1['text']
        u31 = self.row7col3['text']
        u33 = self.row7col5['text']
        u34 = self.row7col6['text']
        u44 = self.row7col7['text']
        u35 = self.row8col3['text']
        u36 = self.row8col4['text']
        u37 = self.row8col5['text']
        u38 = self.row8col8['text']
        u39 = self.row8col9['text']
        u40 = self.row9col1['text']
        u41 = self.row9col5['text']
        u42 = self.row9col7['text']
        u43 = self.row9col8['text']

        player_board = [
            [k1, k2, u1, k3, u2, u3, k4, k5, u4],
            [k6, u5, u6, u7, k7, k8, u8, u9, k9],
            [u10, u11, u12, k10, u13, k11, u14, k12, k13],
            [u15, u16, k14, u17, k15, u18, k16, k17, u19],
            [u20, u21, k20, u22, k21, u23, k22, k23, u24],
            [k25, u25, k26, u26, k27, u27, u28, u29, k28],
            [u30, k30, u31, k31, u33, u34, u44, k32, k33],
            [k35, k36, u35, u36, u37, k37, k38, u38, u39],
            [u40, k40, k41, k42, u41, k43, u42, u43, k44]
        ]

        if player_board == self.playing_board:
            messagebox.showinfo('Solved', 'Congratulations! You solved it.')
            self.generate_sudoku()
        else:
            messagebox.showinfo('Unsolved', 'Not quite there yet.')


if __name__ == "__main__":
    app = Switch()
    app.mainloop()
