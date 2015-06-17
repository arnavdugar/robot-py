import ctypes
import math

lib = ctypes.CDLL('./lib/position.so')

lib.vec3d_dot.restype = ctypes.c_double
lib.vec3d_magnitude.restype = ctypes.c_double
lib.vec3d_distance.restype = ctypes.c_double
lib.vec3d_interior_angle.restype = ctypes.c_double
lib.vec3d_angle.restype = ctypes.c_double


class Position(ctypes.Structure):

    _fields_ = [('x', ctypes.c_double),
                ('y', ctypes.c_double),
                ('z', ctypes.c_double)]

    properties = ('x', 'y', 'z')

    @property
    def pointer(self):
        return ctypes.byref(self)

    def __repr__(self):
        return '(%g, %g, %g)' % (self.x, self.y, self.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

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
        if type(other) == Position:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
            return Position(x, y, z)

    def __imul__(self, other):
        x = self.x * other
        y = self.y * other
        z = self.z * other
        return Position(x, y, z)

    def __neg__(self):
        x = self.x * -1
        y = self.y * -1
        z = self.z * -1
        return Position(x, y, z)

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

    def interior_angle(self, other):
        return math.acos((self * other) / math.sqrt((self * self) * (other * other)))

    def angle(self, other, normal):
        angle = self.interior_angle(other)
        if (self.cross(other)) * normal < 0:
            angle *= -1
        return angle

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

    def rotated(self, axis, angle):
        p = Position()
        lib.vec3d_rotate(p.pointer, self.pointer, axis.pointer, ctypes.c_double(angle))
        return p