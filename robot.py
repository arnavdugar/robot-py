import position
import math


class Robot:

    properties = ("start_position", "legs")

    def init(self):
        pass

    def __repr__(self):
        return "[Robot]"

    @property
    def global_start_position(self):
        return self.start_position


class Leg:

    properties = ("name", "start_position", "segments")

    def init(self):
        pass

    def __repr__(self):
        return "[Leg %d]" % self.index

    @property
    def position(self):
        return self.global_end_position - self.global_start_position

    @property
    def global_start_position(self):
        return self.parent.global_start_position + self.start_position

    @property
    def global_end_position(self):
        return self.legs[len(self.legs) - 1].end_position


class Segment:

    properties = ("name", "length", "axis", "direction_center", "default_rotation", "write_index")

    def init(self):
        self._rotation = self.default_rotation
        self.axis_normalized = self.axis.normalized
        self.direction_center_normalized = self.direction_center.normalized
        self.display_listener = None

    def __repr__(self):
        return "[Segment %d, %d]" % (self.parent.index, self.index)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        if rotation < -1:
            rotation = -1
        elif rotation > 1:
            rotation = 1
        self._rotation = rotation
        if self.display_listener:
            self.display_listener()

    @property
    def angle(self):
        return self.rotation * math.pi / 2

    @angle.setter
    def angle(self, angle):
        self.rotation = angle * 2 / math.pi

    @property
    def value(self):
        return 1500 + round(self.rotation * 1000)

    @value.setter
    def value(self, value):
        self.rotation = (value - 1500) / 1000

    @property
    def global_axis(self):
        if self.previous:
            return self.axis_normalized.rotated(self.previous.global_axis, self.previous.angle)
        else:
            return self.axis_normalized

    @property
    def global_direction_center(self):
        if self.previous:
            return self.direction_center_normalized.rotated(self.previous.global_axis, self.previous.angle)
        else:
            return self.direction_center_normalized

    @property
    def position(self):
        return self.global_direction_center.scaled(self.length).rotated(self.global_axis, self.angle)

    @property
    def global_start_position(self):
        if self.previous:
            return self.previous.global_end_position
        else:
            return self.parent.global_start_position

    @property
    def global_end_position(self):
        return self.global_start_position + self.position