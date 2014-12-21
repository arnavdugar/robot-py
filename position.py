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
            return lib.vec3d_dot(self.pointer, other.pointer)
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
        return lib.vec3d_interior_angle(self.pointer, other.pointer)

    def angle(self, other):
        return lib.vec3d_angle(self.pointer, other.pointer)

    def rotate_x(self, angle):
        return lib.vec3d_irotate_x(self.pointer, ctypes.c_double(angle))

    def rotate_y(self, angle):
        return lib.vec3d_irotate_y(self.pointer, ctypes.c_double(angle))

    def rotate_z(self, angle):
        return lib.vec3d_irotate_z(self.pointer, ctypes.c_double(angle))

    def rotated(self, axis, angle):
        p = Position()
        lib.vec3d_rotate(p.pointer, self.pointer, axis.pointer, ctypes.c_double(angle))
        return p