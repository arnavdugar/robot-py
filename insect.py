import robot
import serialize
import math


class Leg(robot.Leg):

    properties = ("model", "orientation", "name_base", "start_position", "leg_direction", "lengths", "write_indexes")
    segment_types = ('Base', 'Middle', 'Tip')

    def init(self):
        self.name = self.name_base + ' Leg'
        self.segments = serialize.load(self.model)
        assert len(self.segments) == 3
        initial_direction = self.segments[0].direction_center
        if self.orientation == 'counterclockwise':
            self.segments[0].axis *= -1
            self.segments[1].axis *= -1
            self.segments[1].default_rotation *= -1
            self.segments[2].axis *= -1
            self.segments[2].default_rotation *= -1
        axis = initial_direction.cross(self.leg_direction)
        angle = initial_direction.interior_angle(self.leg_direction)
        for i in range(len(self.segments)):
            segment = self.segments[i]
            self.init_segment(segment, i, axis, angle)
        self.segments[0].parent = self

    def init_segment(self, segment, i, axis, angle):
        segment.index = i
        segment.parent = self
        segment.name = Leg.segment_types[i] + ' ' + self.name_base + ' Segment'
        segment.length = self.lengths[i]
        segment.write_index = self.write_indexes[i]
        segment.axis = segment.axis.rotated(axis, angle)
        segment.direction_center = segment.direction_center.rotated(axis, angle)
        segment.init()

    def compute_base(self, position, start):
        segment = self.segments[0]
        axis = segment.global_axis
        d1, d2, d3 = position * axis, segment.direction_center_normalized * axis, start * axis
        v1 = position - (axis * d1)
        v1 -= start - (axis * d3)
        v2 = segment.direction_center_normalized - (axis * d2)
        if v1.interior_angle(v2) > math.pi/2:
            v1 *= -1
        a1 = math.asin(v2.cross(v1) * axis / (v1.magnitude * v2.magnitude))
        p1 = (segment.direction_center_normalized * segment.length).rotated(axis, a1) + start
        return a1, p1

    def compute_mid(self, position, start, a1):
        s1, segment, s2 = self.segments
        remaining = position - start
        global_direction_center = segment.direction_center_normalized.rotated(s1.axis_normalized, a1)
        centered_angle = global_direction_center.angle(remaining, segment.axis_normalized)
        interior_angle = triangle(segment.length, remaining.magnitude, s2.length)
        a2 = centered_angle + interior_angle
        p2 = (global_direction_center * segment.length).rotated(segment.global_axis, a2) + start
        return a2, p2

    def compute_tip(self, position, start, a1, a2):
        s1, s2, segment = self.segments
        remaining = position - start
        global_direction_center = segment.direction_center_normalized.rotated(s2.axis_normalized, a2)
        global_direction_center = global_direction_center.rotated(s1.axis_normalized, a1)
        centered_angle = global_direction_center.angle(remaining, segment.axis_normalized)
        return centered_angle

    def move_to(self, position):
        start = self.segments[0].global_start_position
        a0, p0 = self.compute_base(position, start)
        a1, p1 = self.compute_mid(position, p0, a0)
        a2 = self.compute_tip(position, p1, a0, a1)
        self.segments[0].angle = a0
        self.segments[1].angle = a1
        self.segments[2].angle = a2

def triangle(l1, l2, l3):
    return math.acos(((l1 ** 2) + (l2 ** 2) - (l3 ** 2)) / (2 * l1 * l2))