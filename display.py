

class Display:

    def __init__(self):
        self.body = None
        self.segments = set()

    def bind_body(self, body):
        self.body = body

    def bind_segment(self, segment):
        self.segments.add(segmentr)