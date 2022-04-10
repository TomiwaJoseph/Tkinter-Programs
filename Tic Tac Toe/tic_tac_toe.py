from tkinter import *
root = Tk

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
        self._frame.place(x=0,y=0,relheight=1,relwidth=1)


class StartPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#101820')
        self.master = master
        self.master.title('Intro Page')
        self.master.geometry('400x515')
        self.master.resizable(False,False)
        #======= Title ===================== 101820 f2aa4c
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
        Label(text="You vs AI!",font='candara 24',bg='#222',fg='white').place(x=130,y=10)
        self.board = Frame(width=301,height=360,bg='light gray').place(x=50,y=75)
        self.restart = Button(text='Reset',font='candara 14',command=self.reset_board)
        self.restart.place(x=100,y=448)
        self.know_if_computer_first = IntVar()
        self.switch_opponent = Button(text='Play Human',font='candara 14',command=lambda:self.master.switch_frame(HumanPage))
        self.switch_opponent.place(x=200,y=448)
        self.AIfirst = Checkbutton(text='Allow AI to play first',font='candara 12',
            fg='cadetblue',bg='#222',var=self.know_if_computer_first,command=self.AIPlayFirst)
        self.AIfirst.place(x=110,y=45)
        self.stop_game = False
    
    def AIPlayFirst(self):
        pass
    
    def reset_board(self):
        pass


class HumanPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#101820')
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('400x515')
        Label(text="Game on!",font='montserrat 24',bg='#101820',
              fg='#f2aa4c').place(anchor=CENTER,relx=0.5,rely=0.075)
        # self.board = Frame(width=301,height=360,bg='light gray').place(anchor=CENTER,relx=0.5,rely=0.495)
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
        self.but7 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but7))
        self.but7.place(x=50,y=77)
        self.but8 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but8))
        self.but8.place(x=150,y=77)
        self.but9 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but9))
        self.but9.place(x=250,y=77)
        self.but4 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but4))
        self.but4.place(x=50,y=195)
        self.but5 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but5))
        self.but5.place(x=150,y=195)
        self.but6 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but6))
        self.but6.place(x=250,y=195)
        self.but1 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but1))
        self.but1.place(x=50,y=313)
        self.but2 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but2))
        self.but2.place(x=150,y=313)
        self.but3 = Button(text='',bd=0,bg='white',font='candara 42',width=3,command=lambda:self.switch_turns(self.but3))
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
        
        self.but1.config(bg = 'white')
        self.but2.config(bg = 'white')
        self.but3.config(bg = 'white')
        self.but4.config(bg = 'white')
        self.but5.config(bg = 'white')
        self.but6.config(bg = 'white')
        self.but7.config(bg = 'white')
        self.but8.config(bg = 'white')
        self.but9.config(bg = 'white')



if __name__=='__main__':
    app = Switch()
    app.mainloop()