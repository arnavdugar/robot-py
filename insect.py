import robot
import serialize


class Leg(robot.Leg):

    properties = ("model", "name_base", "start_position", "leg_direction", "lengths", "write_indexes")
    segment_types = ('Base', 'Middle', 'Tip')

    def init(self):
        self.name = self.name_base + ' Leg'
        self.segments = serialize.load(self.model)
        for i in range(len(self.segments)):
            segment = self.segments[i]
            segment.name = Leg.segment_types[i] + ' ' + self.name_base + ' Segment'
            segment.length = self.lengths[i]
            segment.write_index = self.write_indexes[i]
        self.segments[0].parent = self