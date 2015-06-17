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

    def compute_base(self, position):
        segment = self.segments[0]
        axis = segment.global_axis
        center = segment.global_direction_center
        start = segment.global_start_position
        d1, d2, d3 = position * axis, center * axis, start * axis
        v1 = position - (axis * d1)
        v1 -= start - (axis * d3)
        v2 = center - (axis * d2)
        if v1.interior_angle(v2) > math.pi/2:
            v1 *= -1
        a = math.asin(v2.cross(v1) * axis / (v1.magnitude * v2.magnitude))
        p = (center * segment.length).rotated(axis, a) + segment.global_start_position
        return a, p

    def compute_remaining(self, position, start):
        s1, s2 = self.segments[1:3]
        remaining = position - start
        centered_angle = s1.position.angle(s2.global_direction_center, s2.axis_normalized)
        interior_angle = triangle(s1.length, s2.length, remaining.magnitude)
        import pdb; pdb.set_trace()
        return 0.0, -centered_angle

    def move_to(self, position):
        a0, p0 = self.compute_base(position)
        a1, a2 = self.compute_remaining(position, p0)
        self.segments[0].angle = a0
        self.segments[1].angle = a1
        self.segments[2].angle = a2

def triangle(l1, l2, l3):
    return math.acos(((l1 ** 2) + (l2 ** 2) - (l3 ** 2)) / (2 * l1 * l2))