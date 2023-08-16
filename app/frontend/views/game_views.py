import arcade as arc
import arcade.gui as ui
import pyglet.math

from app.frontend.Entities.base_entity import BaseEntity
from app.frontend.VFX_elements.Shapes import Sweeper

from technical.ui_style import button_style


class MainMenu(arc.View):
    def __init__(self, processor):
        super().__init__()

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
            self.window.show_view(SimulationView(self.processor))

        main_box.add(title)
        main_box.add(new_world_button)
        main_box.add(load_world_button)
        main_box.add(settings_button)

        main_box.center_on_screen()
        self.ui.add(main_box)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse.position = x, y

    def on_draw(self):
        self.window.use()
        self.clear()
        self.ui.draw()
        self.mouse.draw()
        self.sweeper.draw()

    def on_update(self, delta_time: float):
        self.sweeper.move(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol, modifiers:
            case arc.key.ESCAPE, _:
                self.processor.quit()


class SmartCamera(arc.Camera):
    def __init__(self, viewport):
        super().__init__(viewport=viewport)


class SimulationSection(arc.Section):
    def __init__(self, entities_list, entities_alias):
        super().__init__(100 / 1920 * self.window.width,
                         100 / 1200 * self.window.height,
                         1720 / 1920 * self.window.width,
                         1000 / 1200 * self.window.height,
                         local_mouse_coordinates=True)
        self.entities_list = entities_list
        self.entities_alias: dict[int, BaseEntity] = entities_alias
        self.camera = arc.Camera(viewport=(
                100 / 1920 * self.window.width,
                100 / 1200 * self.window.height,
                1720 / 1920 * self.window.width,
                1000 / 1200 * self.window.height,
            ))
        self.camera.center((0, 0))

    def on_update(self, delta_time: float):
        if self.camera.zoom <= 1:
            [e.set_quality(3) for e in self.entities_alias.values()]
        elif 1 < self.camera.zoom <= 1.5:
            [e.set_quality(2) for e in self.entities_alias.values()]
        elif 1.5 < self.camera.zoom <= 3:
            [e.set_quality(1) for e in self.entities_alias.values()]
        else:
            [e.set_quality(0) for e in self.entities_alias.values()]

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.camera.zoom = max(0.5, min(5.0, self.camera.zoom - scroll_y / 3))

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int):
        self.camera.move_to(self.camera.position + pyglet.math.Vec2(-dx, -dy) * self.camera.zoom**2 * 2)

    def on_draw(self):
        self.camera.use()
        self.entities_list.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol, modifiers:
            case arc.key.ESCAPE, _:
                self.view.processor.quit()


class SimulationView(arc.View):
    def __init__(self, processor):
        super().__init__()
        self.window.set_mouse_visible(True)

        # self.simulation_camera.anchor = (0, 0)

        self.gui_camera = arc.Camera
        self.processor = processor
        self.entities_list = arc.SpriteList()
        self.entities_alias: dict[int, BaseEntity] = {}
        self.world_age = 0

        self.add_section(SimulationSection(self.entities_list, self.entities_alias))

    def on_update(self, delta_time: float):
        if self.world_age != self.processor.world_age:

            buff = self.processor.entities.copy()

            for uid, e in buff.items():
                x, y, angle, diam, color, uid = e
                if uid not in self.entities_alias:
                    self.entities_alias[uid] = BaseEntity(x, y, diam, angle, color,
                                                          self.entities_list)
                self.entities_alias[uid].update(x, y, diam, angle, color)
            disappeared = []
            for uid, e in self.entities_alias.items():
                if uid not in self.processor.entities:
                    e.disappear()
                    disappeared.append(uid)
            for uid in disappeared:
                self.entities_alias.pop(uid)

            self.entities_list.update()
            self.world_age = self.processor.world_age

    def on_draw(self):
        self.clear(arc.color.DARK_BLUE_GRAY)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol, modifiers:
            case arc.key.ESCAPE, _:
                self.processor.quit()
