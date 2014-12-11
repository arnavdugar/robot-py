import tkinter
import position


class Display(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Robot")
        self.resizable(0, 0)
        self.canvas = [Canvas(self, i) for i in range(4)]

    def clear_all(self):
        for c in self.canvas:
            c.delete("all")

    def draw_line(self, name, start, end, **kwargs):
        for c in self.canvas:
            c.draw_line(name, start, end, **kwargs)

    def draw_polygon(self, name, *vertexes, **kwargs):
        for c in self.canvas:
            c.draw_polygon(name, *vertexes, **kwargs)

    def update_item(self, name, *vertexes):
        for c in self.canvas:
            c.update_item(name, *vertexes)


class Canvas(tkinter.Canvas):

    default_rotation = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 3, 2))
    final_view = position.Position(0, 0, 1)

    def __init__(self, master, index):
        tkinter.Canvas.__init__(self, master, width=400, height=400)
        self.grid(column=(index % 2), row=(index // 2))
        self.rotation = position.Position(*Canvas.default_rotation[index])

    @property
    def rotation(self):
        return self._rotation
        
    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        self.angle = Canvas.final_view.angle(self.rotation)
        self.axis = Canvas.final_view.cross(self.rotation)
        magnitude = self.axis.magnitude
        if magnitude == 0:
            self.axis = position.Position(0, 1, 0)
        else:
            self.axis.normalize()

    def compute_points(self, *points):
        values = []
        for point in points:
            rotated = point.rotated(self.axis, self.angle)
            values.append(200 + rotated.x)
            values.append(200 + rotated.y)
        return values

    def draw_line(self, name, start, end, **kwargs):
        points = self.compute_points(start, end)
        self.create_line(*points, tags=name, width=2, **kwargs)

    def draw_polygon(self, name, *vertexes, **kwargs):
        points = self.compute_points(*vertexes)
        self.create_polygon(*points, tags=name, outline='black', fill='#ccc', width=2, activefill='#aaa', **kwargs)

    def update_item(self, name, *vertexes):
        points = self.compute_points(*vertexes)
        self.coords(name, tuple(points))
