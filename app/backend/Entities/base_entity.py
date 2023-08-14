import numpy as np
import pymunk as pmk


class BaseEntity:
    def __init__(self):
        self._mass = 10
        self._size = 15
        self.body = pmk.Body()
        self.shape = pmk.Circle(body=self.body, radius=self._size / 2)
        self.shape.mass = self._mass
        self.color = (100, 100, 100, 255)

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
