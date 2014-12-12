import robot
import serialize


class Leg(robot.Leg):

    properties = ("model", "name_base", "start_position", "leg_direction", "lengths", "write_indexes")
    segment_types = ('Base', 'Middle', 'Tip')

    def init(self):
        self.name = self.name_base + ' Leg'
        self.segments = serialize.load(self.model)
        initial_direction = self.segments[0].direction_center
        angle = initial_direction.angle(self.leg_direction)
        axis = initial_direction.cross(self.leg_direction)
        for i in range(len(self.segments)):
            segment = self.segments[i]
            segment.index = i
            segment.parent = self
            segment.name = Leg.segment_types[i] + ' ' + self.name_base + ' Segment'
            segment.length = self.lengths[i]
            segment.write_index = self.write_indexes[i]
            segment.axis = segment.axis.rotated(axis, angle)
            segment.direction_center = segment.direction_center.rotated(axis, angle)
            segment.init()
        self.segments[0].parent = self