import robot
import serialize
import position
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
            self.segments[1].axis.scale(-1)
            self.segments[1].default_rotation *= -1
            self.segments[2].axis.scale(-1)
            self.segments[2].default_rotation *= -1
        axis = initial_direction.cross(self.leg_direction)
        angle = initial_direction.angle(self.leg_direction)
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

    def compute_base(self, position, segment):
        axis = segment.global_axis
        center = segment.global_direction_center
        start = segment.global_start_position
        d1, d2, d3 = position * axis, center * axis, start * axis
        v1 = position - axis.scaled(d1)
        v1 -= start - axis.scaled(d3)
        v2 = center - axis.scaled(d2)
        if v1.angle(v2) > math.pi/2:
            v1 = v1.scaled(-1)
        a = math.asin(v2.cross(v1) * axis / (v1.magnitude * v2.magnitude))
        p = center.scaled(segment.length).rotated(axis, a)
        return a, p

    def compute_remaining(self, position, p1, s1, s2):
        local = position - p1
        center, base = s1.direction_center_normalized, s1.previous
        center = center.rotated(base.axis_normalized, base.angle)
        center_angle = center.angle(local)

        distance = local.magnitude
        angle = s1.length * s1.length + s2.length * s2.length - distance * distance
        angle /= 2 * s1.length * s2.length
        if angle < -1 or angle > 1:
            print("Error: Cannot Reach Location!")
            return

        pass

    def move_to(self, position):
        a1, p1 = self.compute_base(position, self.segments[0])
        self.compute_remaining(position, p1, self.segments[1], self.segments[2])
        return a1