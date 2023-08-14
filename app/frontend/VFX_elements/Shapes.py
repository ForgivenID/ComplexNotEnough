import arcade as arc


class Sweeper:
    def __init__(self, window):
        self.window = window
        self.width = self.window.width
        self.height = self.window.height * .2
        self.res: int = 40
        self.list = arc.shape_list.ShapeElementList()
        self.list.position = (0, self.window.height)
        for i in range(self.res):
            self.list.append(
                arc.shape_list.create_rectangle_filled(self.width / 2, i * self.height / self.res,
                                                       self.width,
                                                       self.height / self.res,
                                                       color=(255, 255, 255, round(60 * (1 - i / self.res)))))

    def draw(self):
        self.list.draw()

    def move(self, dt):
        self.list.position = (
            0, (self.list.position[1] - 80 * dt + 2 * self.height) % (
                        self.window.height + 2.2 * self.height) - 2 * self.height
        )
