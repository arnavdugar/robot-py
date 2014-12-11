import tkinter


class Display(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Robot")
        self.resizable(0, 0)
        self.canvas = [Canvas(self, i) for i in range(4)]


class Canvas(tkinter.Canvas):

    def __init__(self, master, index):
        tkinter.Canvas.__init__(self, master, width=400, height=400)
        self.grid(column=(index % 2), row=(index // 2))