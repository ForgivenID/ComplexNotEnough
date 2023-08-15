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


class CustomMouse:
    def __init__(self, window: arc.Window):
        super().__init__([], [(0, 0, 0, 0)])
        self.window = window
        self.mouse = arc.shape_list.ShapeElementList()
        self.mouse.append(
            arc.shape_list.create_ellipse_outline(self.window.mouse['x'] + 9,
                                                  self.window.mouse['y'] - 15,
                                                  20, 35, (100, 100, 100, 255), 5, -30, 3)
        )
        self.mouse.append(
            arc.shape_list.create_ellipse_filled(self.window.mouse['x'] + 9,
                                                 self.window.mouse['y'] - 15,
                                                 10, 25, (255, 255, 255, 150), -30, 3)
        )
        arc.schedule(self.draw, 0.01)

    def draw(self):
        self.mouse.draw()

    def on_update(self):
        if 'x' in self.window.mouse.data and 'y' in self.window.mouse.data:
            self.mouse.position = self.window.mouse['x'], self.window.mouse['y']
