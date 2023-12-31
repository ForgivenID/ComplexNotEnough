import numpy as np
import pymunk as pmk


class BaseEntity:
    def __init__(self):
        self.type = 'Base'
        self._mass = 200
        self._size = 100
        self.body = pmk.Body()
        self.shape = pmk.Circle(body=self.body, radius=self._size / 2)
        self.shape.mass = self._mass
        self.color = np.array([253, 100, 100, 253], dtype=np.ubyte)

    def update(self, dt):
        ...
        #self.body.apply_force_at_local_point((100 * dt, 0), (0, 1))

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, new_mass):
        self._mass = new_mass
        self.shape.mass = new_mass

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size
        self.shape.unsafe_set_radius(new_size / 2)

    @property
    def position(self) -> pmk.Vec2d | tuple[float, float]:
        return self.body.position

    @position.setter
    def position(self, pos: pmk.Vec2d | tuple[float, float]):
        self.body.position = pos

    @property
    def rotation(self):
        return self.body.angle

    @rotation.setter
    def rotation(self, float):
        self.body.angle = float


'''
def __init__(self):

        self._position = np.array([0, 0, 0], dtype='float32')
        self._velocity = np.array([0, 0, 0], dtype='float32')
        self.radius = 3

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos: tuple[float, float] | tuple[float, float, float]):
        match pos:
            case x, y:
                self._position[:2] = x, y

            case x, y, theta:
                self._position[:] = x, y, theta

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, new_x):
        self._position[0] = new_x

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, new_y):
        self._position[1] = new_y

    @property
    def theta(self):
        return self._position[2]

    @theta.setter
    def theta(self, new_theta):
        self._position[2] = new_theta
'''
