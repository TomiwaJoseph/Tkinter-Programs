from tkinter import *

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
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#101820')
        self.master = master
        self.master.title('Intro Page')
        self.master.geometry('400x515')
        self.master.resizable(0,0)
        #======= Title =====================
        Label(self.master,text='Tic Tac Toe',font='montserrat 42',fg='#505050',bg='#f2aa4c').place(x=45,y=153)
        Label(self.master,text='Tic Tac Toe',font='montserrat 42',fg='#f2aa4c',bg='#101820').place(x=45,y=150)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Human',width=12,font='montserrat 14',bd=0,fg='#101820',bg='#f2aa4c',command=lambda:self.master.switch_frame(HumanPage))
        self.human.place(x=212,y=255)
        self.AI = Button(self.master,text='Computer',width=12,font='montserrat 14',bd=0,fg='#101820',bg='#f2aa4c',command=lambda:self.master.switch_frame(AIPage))
        self.AI.place(x=40,y=255)


class AIPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#101820')
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('400x515')
        self.master.resizable(0,0)
        self.restart = Button(text='Reset',width=12,font='montserrat 14',command=self.reset_board,
                              fg='#101820',bg='#f2aa4c')
        self.restart.place(x=40,y=450)
        self.switch_opponent = Button(text='Play Human',font='montserrat 14',command=lambda:self.master.switch_frame(HumanPage),
                            width=12,fg='#101820',bg='#f2aa4c')
        self.switch_opponent.place(x=210,y=450)
        self.know_if_computer_first = IntVar()
        self.AIfirst = Checkbutton(text='Allow AI to play first',font='montserrat 14',
            fg='#f2aa4c',bg='#101820',var=self.know_if_computer_first,command=self.AI_play_first)
        self.AIfirst.place(anchor=CENTER,relx=0.5,rely=0.075)
        self.stop_game = False
        self.display_buttons()
        #=========== Variables =============
        self.player = 'X'
        self.bot = 'O'
        self.board = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '
        }
        
    def display_buttons(self):
        #========== Buttons =================
        self.but1 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but1, 1))
        self.but1.place(x=50,y=77)
        self.but2 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but2, 2))
        self.but2.place(x=150,y=77)
        self.but3 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but3, 3))
        self.but3.place(x=250,y=77)
        self.but4 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but4, 4))
        self.but4.place(x=50,y=195)
        self.but5 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but5, 5))
        self.but5.place(x=150,y=195)
        self.but6 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but6, 6))
        self.but6.place(x=250,y=195)
        self.but7 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but7, 7))
        self.but7.place(x=50,y=315)
        self.but8 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but8, 8))
        self.but8.place(x=150,y=315)
        self.but9 = Button(text='',bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but9, 9))
        self.but9.place(x=250,y=315)
    
    def reset_board(self):
        self.player = 'X'
        self.bot = 'O'
        self.board = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '
        }
        self.stop_game = False
        self.know_if_computer_first.set(0)
        self.but1["text"] = ""
        self.but2["text"] = ""
        self.but3["text"] = ""
        self.but4["text"] = ""
        self.but5["text"] = ""
        self.but6["text"] = ""
        self.but7["text"] = ""
        self.but8["text"] = ""
        self.but9["text"] = ""
        
        self.but1.configure(bg='#222')
        self.but2.configure(bg='#222')
        self.but3.configure(bg='#222')
        self.but4.configure(bg='#222')
        self.but5.configure(bg='#222')
        self.but6.configure(bg='#222')
        self.but7.configure(bg='#222')
        self.but8.configure(bg='#222')
        self.but9.configure(bg='#222')
        self.AIfirst.config(state=NORMAL)

    def insert_letter(self, letter, position):
        self.board[position] = letter
        return
        
    def AI_play_first(self):
        check = self.know_if_computer_first.get()
        if check:
            self.player = "O"
            self.bot = "X"
            self.get_AI_move()
            self.AIfirst.config(state=DISABLED)
    
    def switch_turns(self, button, position):
        if button['text'] == '' and self.stop_game == False:
            button.configure(text=self.player, fg='#fff')
            self.insert_letter(self.player, position)
            self.check_for_win()
            self.get_AI_move()
    
    def clean_board(self, button_list):
        all_tiles = [self.but1, self.but2, self.but3, self.but4, self.but5, self.but6,
                     self.but7, self.but8, self.but9]
        for button in all_tiles:
            if button in button_list:
                button.configure(fg='#101820', bg='#f2aa4c')
    
    def check_for_win(self):
        if (self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] != ' '):
            self.clean_board([self.but1, self.but2, self.but3])
            self.stop_game = True
            return True
        elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] != ' '):
            self.clean_board([self.but4, self.but5, self.but6])
            self.stop_game = True
            return True
        elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] != ' '):
            self.clean_board([self.but7, self.but8, self.but9])
            self.stop_game = True
            return True
        elif (self.board[1] == self.board[4] and self.board[1] == self.board[7] and self.board[1] != ' '):
            self.clean_board([self.but1, self.but4, self.but7])
            self.stop_game = True
            return True
        elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] != ' '):
            self.clean_board([self.but2, self.but5, self.but8])
            self.stop_game = True
            return True
        elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] != ' '):
            self.clean_board([self.but3, self.but6, self.but9])
            self.stop_game = True
            return True
        elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] != ' '):
            self.clean_board([self.but1, self.but5, self.but9])
            self.stop_game = True
            return True
        elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] != ' '):
            self.clean_board([self.but7, self.but5, self.but3])
            self.stop_game = True
            return True
        else:
            return False
    
    def check_for_draw(self):
        for key in self.board.keys():
            if (self.board[key] == ' '):
                return False
        return True
    
    def check_which_mark_won(self, mark):
        if self.board[1] == self.board[2] and self.board[1] == self.board[3] and self.board[1] == mark:
            return True
        elif (self.board[4] == self.board[5] and self.board[4] == self.board[6] and self.board[4] == mark):
            return True
        elif (self.board[7] == self.board[8] and self.board[7] == self.board[9] and self.board[7] == mark):
            return True
        elif (self.board[1] == self.board[4] and self.board[1] == self.board[7] and self.board[1] == mark):
            return True
        elif (self.board[2] == self.board[5] and self.board[2] == self.board[8] and self.board[2] == mark):
            return True
        elif (self.board[3] == self.board[6] and self.board[3] == self.board[9] and self.board[3] == mark):
            return True
        elif (self.board[1] == self.board[5] and self.board[1] == self.board[9] and self.board[1] == mark):
            return True
        elif (self.board[7] == self.board[5] and self.board[7] == self.board[3] and self.board[7] == mark):
            return True
        else:
            return False
          
    def get_AI_move(self):
        self.AIfirst.config(state=DISABLED)
        a = -1000
        b = 1000
        bestScore = -800
        bestMove = 0
        all_buttons = {
            1: self.but1, 2: self.but2, 3: self.but3,
            4: self.but4, 5: self.but5, 6: self.but6,
            7: self.but7, 8: self.but8, 9: self.but9,
        }
        
        for key in self.board.keys():
            if (self.board[key] == ' '):
                self.board[key] = self.bot
                score = self.minimax(self.board, 0, a, b, False)
                self.board[key] = ' '
                if (score > bestScore):
                    bestScore = score
                    bestMove = key

        self.insert_letter(self.bot, bestMove)
        try:
            all_buttons[bestMove].configure(text=self.bot, fg='#f2aa4c', bg='#fff')
        except KeyError:
            pass
        self.check_for_win()
        return

    def minimax(self, board, depth, alpha, beta, isMaximizing):
        if (self.check_which_mark_won(self.bot)):
            return 1
        elif (self.check_which_mark_won(self.player)):
            return -1
        elif (self.check_for_draw()):
            return 0
        
        if (isMaximizing):
            bestScore = -800
            for key in self.board.keys():
                if (self.board[key] == ' '):
                    self.board[key] = self.bot
                    score = self.minimax(self.board, depth + 1, alpha, beta, False)
                    bestScore = max(bestScore, score)
                    alpha = max(alpha, score)
                    self.board[key] = ' '
                    if beta <= alpha:
                        break
            return bestScore

        else:
            bestScore = 800
            for key in self.board.keys():
                if (self.board[key] == ' '):
                    self.board[key] = self.player
                    score = self.minimax(self.board, depth + 1, alpha, beta, True)
                    bestScore = min(bestScore, score)
                    beta = min(beta, score)
                    self.board[key] = ' '
                    if beta <= alpha:
                        break
            return bestScore


class HumanPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#101820')
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('400x515')
        self.master.resizable(0,0)
        #======== Some UI ============
        Label(text="Game on!",font='montserrat 24',bg='#101820',
              fg='#f2aa4c').place(anchor=CENTER,relx=0.5,rely=0.075)
        self.restart = Button(text='Reset',width=12,font='montserrat 14',command=self.reset_board,
                              fg='#101820',bg='#f2aa4c')
        self.restart.place(x=40,y=450)
        self.switch_opponent = Button(text='Play AI',font='montserrat 14',command=lambda:self.master.switch_frame(AIPage),
                            width=12,fg='#101820',bg='#f2aa4c')
        self.switch_opponent.place(x=210,y=450)
        self.player = 'X'
        self.stop_game = False
        self.display_buttons()
        
    def display_buttons(self):
        #========== Buttons =================
        self.but7 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but7))
        self.but7.place(x=50,y=77)
        self.but8 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but8))
        self.but8.place(x=150,y=77)
        self.but9 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but9))
        self.but9.place(x=250,y=77)
        self.but4 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but4))
        self.but4.place(x=50,y=195)
        self.but5 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but5))
        self.but5.place(x=150,y=195)
        self.but6 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but6))
        self.but6.place(x=250,y=195)
        self.but1 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but1))
        self.but1.place(x=50,y=313)
        self.but2 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but2))
        self.but2.place(x=150,y=313)
        self.but3 = Button(text='',bd=0,bg='#222',font='candara 42',width=3,command=lambda:self.switch_turns(self.but3))
        self.but3.place(x=250,y=313)
    
    def switch_turns(self, button):
        if button['text'] == '' and self.stop_game == False and self.player == 'X':
            button.configure(text='X',fg='#101820',bg='white')
            self.player = 'O'
            self.check_for_win()
        elif button['text'] == '' and self.stop_game == False and self.player == 'O':
            button.configure(text='O',fg='#f2aa4c',bg='white')
            self.player = 'X'
            self.check_for_win()
            
    def clean_board(self, button_list):
        all_tiles = [self.but1, self.but2, self.but3, self.but4, self.but5, self.but6,
                     self.but7, self.but8, self.but9]
        for button in all_tiles:
            if button in button_list:
                button.configure(fg='#101820', bg='#f2aa4c')
                
    def check_for_win(self):
        if self.but1['text'] == self.but2['text'] and self.but1['text'] == self.but3['text'] and self.but1['text'] != "":
            self.clean_board([self.but1, self.but2, self.but3, self.but1['text']])
            self.stop_game = True
        elif self.but4['text'] == self.but5['text'] and self.but4['text'] == self.but6['text'] and self.but4['text'] != "":
            self.clean_board([self.but4, self.but5, self.but6, self.but4['text']])
            self.stop_game = True
        elif self.but7['text'] == self.but8['text'] and self.but7['text'] == self.but9['text'] and self.but7['text'] != "":
            self.clean_board([self.but7, self.but8, self.but9, self.but7['text']])
            self.stop_game = True
        elif self.but1['text'] == self.but4['text'] and self.but1['text'] == self.but7['text'] and self.but1['text'] != "":
            self.clean_board([self.but1, self.but4, self.but7, self.but1['text']])
            self.stop_game = True
        elif self.but2['text'] == self.but5['text'] and self.but2['text'] == self.but8['text'] and self.but2['text'] != "":
            self.clean_board([self.but2, self.but5, self.but8, self.but2['text']])
            self.stop_game = True
        elif self.but3['text'] == self.but6['text'] and self.but3['text'] == self.but9['text'] and self.but3['text'] != "":
            self.clean_board([self.but3, self.but6, self.but9, self.but3['text']])
            self.stop_game = True
        elif self.but1['text'] == self.but5['text'] and self.but1['text'] == self.but9['text'] and self.but1['text'] != "":
            self.clean_board([self.but1, self.but5, self.but9, self.but1['text']])
            self.stop_game = True
        elif self.but7['text'] == self.but5['text'] and self.but7['text'] == self.but3['text'] and self.but7['text'] != "":
            self.clean_board([self.but7, self.but5, self.but3, self.but7['text']])
            self.stop_game = True
    
    def reset_board(self):
        self.player = 'X'
        self.stop_game = False
        self.but1["text"] = ""
        self.but2["text"] = ""
        self.but3["text"] = ""
        self.but4["text"] = ""
        self.but5["text"] = ""
        self.but6["text"] = ""
        self.but7["text"] = ""
        self.but8["text"] = ""
        self.but9["text"] = ""
        
        self.but1.config(bg='#222')
        self.but2.config(bg='#222')
        self.but3.config(bg='#222')
        self.but4.config(bg='#222')
        self.but5.config(bg='#222')
        self.but6.config(bg='#222')
        self.but7.config(bg='#222')
        self.but8.config(bg='#222')
        self.but9.config(bg='#222')


if __name__=='__main__':
    app = Switch()
    app.mainloop()