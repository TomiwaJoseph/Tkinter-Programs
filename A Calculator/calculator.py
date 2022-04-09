from tkinter import *
from math import sqrt

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
        Frame.configure(self,bg='light gray')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('400x300')
        #self.root.iconbitmap(r'cal.ico')
        self.root.resizable(0,0)
        #======= Title =====================
        Label(self.master,text="Simple",font='candara 20',fg='teal',bg='light gray').place(x=160,y=45)
        Label(self.master,text="Calculator",font='candara 40',fg='#505050',bg='cadetblue').place(x=85,y=83)
        Label(self.master,text="Calculator",font='candara 40',fg='teal',bg='light gray').place(x=85,y=80)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Open',font='candara 18',bd=0,fg='teal',bg='light gray',command=lambda:self.master.switch_frame(MainPage))
        self.human.place(x=170,y=150)


class MainPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='light gray')
        self.root = root
        self.root.title("Calculator")
        self.root.geometry('325x480')
        self.root.resizable(0,0)
        self.result = StringVar()
        self.calculation = ''

if __name__ == '__main__':
    app = Switch()
    app.mainloop()