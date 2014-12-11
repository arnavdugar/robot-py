import math


class Position:

    properties = ("x", "y", "z")

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "(%g, %g, %g)" % (self.x, self.y, self.z)

    @property
    def copy(self):
        return Position(self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Position(x, y, z)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Position(x, y, z)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Position(x, y, z)

    @property
    def magnitude(self):
        return math.sqrt(self * self)

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    def normalize(self):
        magnitude = self.magnitude
        self.x /= magnitude
        self.y /= magnitude
        self.z /= magnitude

    @property
    def normalized(self):
        magnitude = self.magnitude
        x = self.x / magnitude
        y = self.y / magnitude
        z = self.z / magnitude
        return Position(x, y, z)

    def scaled(self, scalor):
        x = self.x * scalor
        y = self.y * scalor
        z = self.z * scalor
        return Position(x, y, z)

    def angle(self, other):
        return math.acos((self * other) / math.sqrt((self * self) * (other * other)))

    def rotate_x(self, angle):
        y = self.y * math.cos(angle) - self.z * math.sin(angle)
        z = self.y * math.sin(angle) + self.z * math.cos(angle)
        self.y, self.z = y, z

    def rotate_y(self, angle):
        z = self.z * math.cos(angle) - self.x * math.sin(angle)
        x = self.z * math.sin(angle) + self.x * math.cos(angle)
        self.z, self.x = z, x

    def rotate_z(self, angle):
        x = self.x * math.cos(angle) - self.y * math.sin(angle)
        y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x, self.y = x, y

    def rotated(self, axis, theta):
        if theta == 0:
            return self.copy
        c, s = math.cos(theta / 2), math.sin(theta / 2)
        l = c, axis.x * s, axis.y * s, axis.z * s
        v = 0, self.x, self.y, self.z
        r = c, -axis.x * s, -axis.y * s, -axis.z * s
        t, x, y, z = quaternion_multiply(quaternion_multiply(l, v), r)
        return Position(x, y, z)


def quaternion_multiply(q1, q2):
    return ((q1[0] * q2[0]) - (q1[1] * q2[1]) - (q1[2] * q2[2]) - (q1[3] * q2[3]),
            (q1[0] * q2[1]) + (q1[1] * q2[0]) + (q1[2] * q2[3]) - (q1[3] * q2[2]),
            (q1[0] * q2[2]) - (q1[1] * q2[3]) + (q1[2] * q2[0]) + (q1[3] * q2[1]),
            (q1[0] * q2[3]) + (q1[1] * q2[2]) - (q1[2] * q2[1]) + (q1[3] * q2[0]))