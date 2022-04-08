from tkinter import *
from tkinter import messagebox
from random import choice, shuffle

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
        Frame.configure(self,bg='cadetblue')
        self.root = root
        self.root.title('Intro Page')
        self.root.geometry('400x300')
        self.root.resizable(0,0)
        #======= Title =====================
        Label(self.master,text="Don't Han",font='candara 40',fg='#505050',bg='#fff').place(x=65,y=83)
        Label(self.master,text="Don't Hang",font='candara 40',fg='white',bg='cadetblue').place(x=65,y=80)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Start',font='candara 18',bd=0,fg='cornsilk',bg='cadetblue',command=lambda:self.master.switch_frame(MainPage))
        self.human.place(x=160,y=140)



class MainPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='cadet blue')
        self.root = root
        self.root.title("Don't Hang")
        self.root.geometry('710x540')
        self.root.resizable(0,0)
        
        
if __name__ == '__main__':
    app = Switch()
    app.mainloop()