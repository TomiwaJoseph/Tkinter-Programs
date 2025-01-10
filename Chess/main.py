from tkinter import Label, Frame, Tk, Button
from game_ui import MultiPlayer

root = Tk


class Switch(root):
    def __init__(self):
        root.__init__(self)
        self._frame = None
        self.switch_frame(MultiPlayer)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.place(x=0, y=0, relheight=1, relwidth=1)


if __name__ == '__main__':
    app = Switch()
    app.mainloop()
