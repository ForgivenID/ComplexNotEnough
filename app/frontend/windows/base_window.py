import arcade as arc

from technical.settings import FULLSCREEN


class BaseWindow(arc.Window):
    def __init__(self):
        super().__init__(
            title=f'ComplexNotEnough - [???]',
            update_rate=1 / 60,
            style=arc.pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
            fullscreen=FULLSCREEN,
            samples=7,
        )
        self.switch_to()
        self.center_window()
        self.activate()

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arc.key.ESCAPE:
                arc.pause(0.5)
                arc.exit()
