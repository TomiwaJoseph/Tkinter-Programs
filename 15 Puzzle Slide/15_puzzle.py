from tkinter import *
from tkinter import messagebox
from random import shuffle

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
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class StartPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#101820')
        self.root = root
        self.root.title('Start Page')
        self.root.geometry('600x600')
        self.root.resizable(0,0)
        #======= Title =====================
        Label(self.master,text="15 Puzzle",font='montserrat 40',fg='#f2aa4c',
              bg='#101820').place(relx=0.5,rely=0.43,anchor=CENTER)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Start',font='montserrat 16',bd=2,width=15,
            fg='#101820',bg='#f2aa4c',command=lambda:self.master.switch_frame(MainPage))
        self.human.place(relx=0.5,rely=0.54,anchor=CENTER)


class Board():
    def __init__(self, playable=True):
        while True:
            self.all_lot = [str(i) for i in range(1, 16)] + [""]
            if not playable:
                break
            shuffle(self.all_lot)
            if self.is_solvable():
                break
        
        self.new_game_board = []
        count = 0
        for row in range(4):
            row_list = []
            for column in range(4):
                row_list.append(Square(row, column, self.all_lot[count]))
                count += 1
            self.new_game_board.append(row_list)
            
    def is_solvable(self):
        inv = self.get_inversions()
        odd = self.is_odd_row()
        if inv % 2 == 0 and odd:
            return True
        if inv % 2 == 1 and not odd:
            return True
        return False
    
    def get_inversions(self):
        count = 0
        for i, x in enumerate(self.all_lot[:-1]):
            if x != '':
                for y in self.all_lot[i+1:]:
                    if y != '' and int(x) > int(y):
                        count += 1
        return count
 
    # returns True if open square is in odd row from bottom:
    def is_odd_row(self):
        idx = self.all_lot.index('')
        return idx in [4,5,6,7,12,13,14,15]           
 
    # returns name, text, and button object at row & col:
    def get_item(self, r, c):
        return self.new_game_board[r][c].get()
 
    def get_square(self, r, c):
        return self.new_game_board[r][c]
 
    def game_won(self):
        goal = [str(i) for i in range(1,16)] + ['']
        i = 0
        for r in range(4):
            for c in range(4):
                nm, txt, btn = self.get_item(r,c)
                if txt != goal[i]:
                    return False
                i += 1
        return True


class Square():
    def __init__(self, row, col, txt):
        self.row = row
        self.col = col
        self.name = 'btn' + str(row) + str(col)
        self.txt = txt
        self.btn = None
        
    def get(self):
            return [self.name, self.txt, self.btn]
 
    def set_btn(self, btn):
        self.btn = btn
 
    def set_txt(self, txt):
        self.txt = txt
        

class MainPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='#101820')
        self.root = root
        self.root.title('15 Puzzle')
        self.root.geometry('600x600')
        self.root.resizable(0,0)
        # ============= UI ===========
        self.display_board()
        self.play_game()
        
    def create_new_game(self):
        self.playable = True
        self.play_game()
        
    def play_game(self):
        # place square on board
        if self.playable:
            button_state = 'normal'
        else:
            button_state = 'disable'
        self.new_game_board = Board(self.playable)
        objh = 100  # button height
        objw = 100  # button width
        objx = 0    # x-coordinate position of widget in frame
        objy = 0    # y-coordinate position of widget in frame
        
        for row in range(4):
            for column in range(4):
                name, text, button = self.new_game_board.get_item(row, column)
                bg_color = '#f2aa4c'
                if text == '':
                    bg_color = '#fff'
                game_button = Button(self.game_frame,text=text,relief='groove',bg=bg_color,fg='#101820',
                    font='candara 24',state=button_state,command=lambda btn=name: self.button_clicked(btn))
                game_button.place(x=objx,y=objy,height=objh,width=objw)
                
                sq = self.new_game_board.get_square(row,column)
                sq.set_btn(game_button)
 
                objx = objx + objw
            objx = 0
            objy = objy + objh
                
    def display_board(self):
        self.playable = False
        self.new_game_board = None
        Button(text='New Game',font='candara 18',fg='#101820',command=self.create_new_game,
            bg='#f2aa4c',width=25,relief='groove').place(anchor=CENTER,relx=0.5,rely=0.135)
        self.game_frame = Frame(self.master,width=404,height=404,relief='ridge',bg='#fff',bd=2)
        self.game_frame.place(anchor=CENTER,relx=0.5,rely=0.555)
                
    def button_clicked(self, name):
        r, c = int(name[3]), int(name[4])
        name_from, txt_from, btn_from = self.new_game_board.get_item(r,c)
        
        if not txt_from:
            return
        
        adjs = [(r-1,c), (r, c-1), (r, c+1), (r+1, c)]
        for x, y in adjs:
            if 0 <= x <= 3 and 0 <= y <= 3:
                nm_to, txt_to, btn_to = self.new_game_board.get_item(x,y)
                if not txt_to:
                    sq = self.new_game_board.get_square(x,y)
                    sq.set_txt(txt_from)
                    sq = self.new_game_board.get_square(r,c)
                    sq.set_txt(txt_to)
                    btn_to.config(text=txt_from,
                                  bg='#f2aa4c')
                    btn_from.config(text=txt_to,
                                  bg='#fff')
                    # check if game is won:              
                    if self.new_game_board.game_won():
                        ans = messagebox.askquestion(
                            'You won!!!', 'Play again?')
                        if ans == 'no':
                            self.root.destroy()
                        else:
                            self.create_new_game()
                    return
        
        
if __name__ == '__main__':
    app = Switch()
    app.mainloop()