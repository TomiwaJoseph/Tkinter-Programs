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
        # self.root.geometry('400x300')
        self.root.geometry('325x480')
        self.root.resizable(0,0)
        #======= Title =====================
        # Label(self.master,text="Simple",font='candara 20',fg='teal',bg='light gray').place(x=120,y=125)
        Label(self.master,text="Calculator",font='candara 40',fg='#505050',bg='cadetblue').place(x=45,y=153)
        Label(self.master,text="Calculator",font='candara 40',fg='teal',bg='light gray').place(x=45,y=150)
        #=========== Buttons ==================
        self.human = Button(self.master,text='Open',font='candara 18',bd=0,fg='teal',bg='light gray',command=lambda:self.master.switch_frame(MainPage))
        # self.human.place(x=130,y=230)
        self.human = Button(self.master,text='Open',font='candara 16',width=18,bd=0,fg='white',bg='teal',command=lambda:self.master.switch_frame(MainPage))
        self.human.place(x=60,y=233)


class MainPage(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        Frame.configure(self,bg='light gray')
        self.root = root
        self.root.title("Calculator")
        self.root.geometry('325x480')
        self.root.resizable(0,0)
        self.user_input = StringVar()
        self.calculation = ''
        #======== Display =============
        self.show_display()
    
    def show_display(self):
        self.display = Label(relief='ridge',fg='teal',bd=5,textvariable=self.user_input,width=9,font='candara 45',justify='right',bg='#fff')
        self.display.pack(pady=(20,0))
        #======= Buttons =================
        self.square = Button(text='x²',font='candara 24',fg='teal',width=4,command=lambda: self.do_the_calculation(self.square))
        self.square.place(x=4,y=400)
        self.one = Button(text='1',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.one))
        self.one.place(x=4,y=330)
        self.four = Button(text='4',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.four))
        self.four.place(x=4,y=260)
        self.seven = Button(text='7',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.seven))
        self.seven.place(x=4,y=190)
        self.squareroot = Button(text='√',font='candara 24',fg='teal',width=4,command=lambda: self.do_the_calculation(self.squareroot))
        self.squareroot.place(x=4,y=120)
    
        self.zero = Button(text='0',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.zero))
        self.zero.place(x=84,y=400)
        self.two = Button(text='2',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.two))
        self.two.place(x=84,y=330)
        self.five = Button(text='5',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.five))
        self.five.place(x=84,y=260)
        self.eight = Button(text='8',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.eight))
        self.eight.place(x=84,y=190)
        self.c = Button(text='C',font='candara 24',fg='teal',width=4,command=self.clear_display)
        self.c.place(x=84,y=120)

        self.point = Button(text='.',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.point))
        self.point.place(x=164,y=400)
        self.three = Button(text='3',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.three))
        self.three.place(x=164,y=330)
        self.six = Button(text='6',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.six))
        self.six.place(x=164,y=260)
        self.nine = Button(text='9',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.nine))
        self.nine.place(x=164,y=190)
        self.back = Button(text=u'\u2190',font='candara 24',fg='teal',width=4,command=lambda:self.remove_last_input(self.back))
        self.back.place(x=164,y=120)

        self.eval = Button(text='=',bd=0,font='candara 24',fg='teal',width=4,command=lambda: self.do_the_calculation(self.eval))
        self.eval.place(x=244,y=400)
        self.plus = Button(text='+',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.plus))
        self.plus.place(x=244,y=330)
        self.minus = Button(text='-',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.minus))
        self.minus.place(x=244,y=260)
        self.mult = Button(text='×',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.mult))
        self.mult.place(x=244,y=190)
        self.div = Button(text='÷',font='candara 24',fg='teal',width=4,command=lambda: self.button_click(self.div))
        self.div.place(x=244,y=120)

    def button_click(self, btn):
        self.calculation += btn['text']
        self.display.config(fg='teal')
        self.user_input.set(self.calculation)
    
    def clear_display(self):
        self.user_input.set('')
        self.calculation = ''
    
    def do_the_calculation(self, btn):
        if btn['text'] == '=' and self.calculation == '':
            return
        elif btn['text'] == '=' and self.calculation.startswith('÷'):
            splitted_input = list(self.calculation)
            splitted_input.insert(0, '0')
            put_together = ''.join(splitted_input)
            real_input = ''
            for elements in put_together:
                if elements == '÷': real_input += '/'
                elif elements == '×': real_input += '*'
                else: real_input += elements
            calculation_result = eval(real_input)
            self.user_input.set(calculation_result)
            self.display.config(fg='green')
            self.calculation = str(calculation_result)
        elif btn['text'] == '=' and self.calculation.startswith('×'):
            splitted_input = list(self.calculation)
            splitted_input.insert(0, '0')
            put_together = ''.join(splitted_input)
            real_input = ''
            for elements in put_together:
                if elements == '÷': real_input += '/'
                elif elements == '×': real_input += '*'
                else: real_input += elements
            calculation_result = eval(real_input)
            self.user_input.set(calculation_result)
            self.display.config(fg='green')
            self.calculation = str(calculation_result)
        elif btn['text'] == '=':
            try:
                self.display.config(fg='green')
                real_input = ''
                for elements in self.calculation:
                    if elements == '÷': real_input += '/'
                    elif elements == '×': real_input += '*'
                    else: real_input += elements
                calculation_result = eval(real_input)
                if len(str(calculation_result)) > 9:
                    self.user_input.set(str(calculation_result)[:9])
                else: self.user_input.set(calculation_result)
                self.calculation = str(calculation_result)
            except:
                self.display.config(fg='red')
                self.user_input.set('INVALID')
                self.calculation = ''
        elif btn['text'] == '√':
            try:
                self.display.config(fg='green')
                calculation_result = sqrt(float(self.calculation))
                if len(str(calculation_result)) > 9:
                    self.user_input.set(str(calculation_result)[:9])
                else: self.user_input.set(calculation_result)
                self.calculation = str(calculation_result)
            except:
                self.display.config(fg='red')
                self.user_input.set('INVALID')
                self.calculation = ''
        elif btn['text'] == 'x²':
            try:
                self.display.config(fg='green')
                calculation_result = eval(self.calculation + '**2')
                if len(str(calculation_result)) > 9:
                    self.user_input.set(str(calculation_result)[:9])
                else: self.user_input.set(calculation_result)
                self.calculation = str(calculation_result)
            except:
                self.display.config(fg='red')
                self.user_input.set('INVALID')
                self.calculation = ''
                       
    def remove_last_input(self, btn):
        cleaned = self.calculation[:-1]
        self.user_input.set(cleaned)
        self.calculation = cleaned


if __name__ == '__main__':
    app = Switch()
    app.mainloop()