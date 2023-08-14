import arcade as arc

from technical.autoloader import shared


class Background:
    def __init__(self, window):
        self.window = window
        self.width = self.window.width
        self.height = self.window.height
        self.res: int = 100
        self.list = arc.shape_list.ShapeElementList()
        for i in range(self.res):
            self.list.append(
                arc.shape_list.create_rectangle_outline(self.width // 2, self.height // 2,
                                                        self.width * (1 - i / self.res),
                                                        self.height * (1 - i / self.res),
                                                        color=(0, 0, 0, round(255 * i / self.res)),
                                                        border_width=self.width // self.res))

    def draw(self):
        self.list.draw()


class StartupView(arc.View):
    def __init__(self):
        super().__init__()
        self.title_text = arc.text.Text('PROXIMORS', align='center',
                                        anchor_x='center',
                                        anchor_y='center',
                                        color=(200, 200, 200, 1),
                                        font_name=('Good Times', 'Arial'),
                                        start_x=self.window.width // 2,
                                        start_y=self.window.height // 2,
                                        font_size=56)
        self.title_text_left = arc.text.Text('PROXIMORS', align='center',
                                             anchor_x='center',
                                             anchor_y='center',
                                             color=(255, 100, 100, 0),
                                             font_name=('Good Times', 'Arial'),
                                             start_x=self.window.width // 2,
                                             start_y=self.window.height // 2,
                                             font_size=56)
        self.title_text_right = arc.text.Text('PROXIMORS', align='center',
                                              anchor_x='center',
                                              anchor_y='center',
                                              color=(100, 100, 255, 0),
                                              font_name=('Good Times', 'Arial'),
                                              start_x=self.window.width // 2,
                                              start_y=self.window.height // 2,
                                              font_size=56)
        self.bg = Background(self.window)
        self.timer = 0
        self.toggle_3d_effect = False
        self.sound_playing = False
        self.sfx = shared.SFX.startup
        self.window.set_mouse_visible(False)

    def on_update(self, delta_time: float):
        self.timer += delta_time
        if 2 <= self.timer <= 4:
            self.title_text.color = (self.title_text.color.r,
                                     self.title_text.color.g,
                                     self.title_text.color.b,
                                     min(self.title_text.color.a + round(250 * delta_time / 2), 255))
        if 3 <= self.timer <= 6:
            self.title_text.color = (min(self.title_text.color.r + round(56 * delta_time / 3), 255),
                                     min(self.title_text.color.g + round(56 * delta_time / 3), 255),
                                     min(self.title_text.color.b + round(56 * delta_time / 3), 255),
                                     self.title_text.color.a)
        if 5 <= self.timer <= 6.5:
            if not self.toggle_3d_effect:
                self.toggle_3d_effect = True

            self.title_text_left.color = (self.title_text_left.color.r,
                                          self.title_text_left.color.g,
                                          self.title_text_left.color.b,
                                          min(round(arc.math.lerp(self.title_text_left.color.a, 255, 3)), 255))
            self.title_text_left.x -= 5 * delta_time / 1.5

            self.title_text_right.color = (self.title_text_right.color.r,
                                           self.title_text_right.color.g,
                                           self.title_text_right.color.b,
                                           min(round(arc.math.lerp(self.title_text_right.color.a, 255, 3)), 255))
            self.title_text_right.x += 5 * delta_time / 1.5
            if not self.sound_playing and self.timer - 5 >= 0.9:
                self.sound_playing = True
                self.sfx.play()
        elif self.timer > 9:
            self.window.toggle_next_scene()

    def on_draw(self):
        self.clear()
        self.bg.draw()
        if self.toggle_3d_effect:
            self.title_text_right.draw()
            self.title_text_left.draw()
        self.title_text.draw()
