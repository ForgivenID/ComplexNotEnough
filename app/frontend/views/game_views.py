import arcade as arc
import arcade.gui as ui

from app.frontend.VFX_elements.Shapes import Sweeper

from technical.ui_style import button_style


class MainMenu(arc.View):
    def __init__(self, processor):
        super().__init__()
        self.ui = ui.ui_manager.UIManager()
        self.sweeper = Sweeper(self.window)
        self.window.set_mouse_visible(False)
        self.ui_setup_main()
        self.processor = processor

    def ui_setup_main(self):
        self.ui.enable()
        self.ui.clear()

        main_box = ui.UIBoxLayout(width=self.window.width // 2, height=self.window.height // 3, space_between=25)

        title = ui.UILabel(
            text_color=(255, 255, 255, 255),
            align='center',
            text='Complex Not Enough',
            font_name=('Good Times', 'Arial'),
            font_size=50,
            size_hint=(1, .25)
        )

        new_world_button = ui.UIFlatButton(text='NEW_WORLD', size_hint=(.2, .16), style=button_style)
        load_world_button = ui.UIFlatButton(text='LOAD_WORLD', size_hint=(.2, .16), style=button_style)
        settings_button = ui.UIFlatButton(text='SETTINGS', size_hint=(.2, .16), style=button_style)

        @new_world_button.event("on_click")
        def new_world(e):
            self.processor.send_to_back(('cmd', 'new_world'))

        main_box.add(title)
        main_box.add(new_world_button)
        main_box.add(load_world_button)
        main_box.add(settings_button)

        main_box.center_on_screen()
        self.ui.add(main_box)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        ...

    def on_draw(self):
        self.window.use()
        self.clear()
        self.ui.draw()
        self.sweeper.draw()
        arc.draw_ellipse_outline(self.window.mouse['x'] + 9,
                                 self.window.mouse['y'] - 15,
                                 20, 35, (100, 100, 100, 255), 5, -30, 3)
        arc.draw_ellipse_filled(self.window.mouse['x'] + 9,
                                self.window.mouse['y'] - 15,
                                10, 25, (255, 255, 255, 150), -30, 3)


    def on_update(self, delta_time: float):
        self.sweeper.move(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol, modifiers:
            case arc.key.ESCAPE, _:
                arc.pause(0.2)
                arc.exit()


class SimulationSection(arc.Section):
    def __init__(self, l, b, w, h):
        super().__init__(l, b, w, h, name='simulation', local_mouse_coordinates=True)



class SimulationView(arc.View):
    def __init__(self, processor):
        super().__init__()
        self.sim_section = arc.Section()

