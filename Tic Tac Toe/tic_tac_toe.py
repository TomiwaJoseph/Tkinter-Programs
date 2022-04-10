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
        self.master.geometry('400x500')
        self.master.resizable(False,False)
        #======= Title ===================== 101820 0063b2
        Label(self.master,text='Tic Tac Toe',font='candara 50',fg='#505050',bg='#f2aa4c').place(x=45,y=153)
        Label(self.master,text='Tic Tac Toe',font='candara 50',fg='#f2aa4c',bg='#101820').place(x=45,y=150)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Human',font='candara 14',bd=0,fg='white',bg='#222',command=lambda:self.master.switch_frame(HumanPage))
        self.human.place(x=250,y=270)
        self.AI = Button(self.master,text='AI',width=8,font='candara 14',bd=0,fg='white',bg='#222',command=lambda:self.master.switch_frame(AIPage))
        self.AI.place(x=60,y=270)


class AIPage(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        Frame.configure(self,bg='#222')
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('400x500')
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
        Frame.configure(self,bg='#222')
        self.master = master
        self.master.title('Tic Tac Toe')
        self.master.geometry('400x500')
        Label(text="Let's Play!",font='candara 24',bg='#222',fg='white').place(x=130,y=15)
        self.board = Frame(width=301,height=360,bg='light gray').place(x=50,y=75)
        self.restart = Button(text='Reset',font='candara 14',command=self.reset_board)
        self.restart.place(x=100,y=448)
        self.switch_opponent = Button(text='Play AI',font='candara 14',command=lambda:self.master.switch_frame(AIPage))
        self.switch_opponent.place(x=230,y=448)
        self.player = 'X'
        self.stop_game = False
        
    def reset_board(self):
        pass



if __name__=='__main__':
    app = Switch()
    app.mainloop()