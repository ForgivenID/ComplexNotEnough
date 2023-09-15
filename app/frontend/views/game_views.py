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
    def __init__(self, viewport=None):
        super().__init__(viewport=viewport)

    def _set_projection_matrix(self, *, update_combined_matrix: bool = True) -> None:
        """
        Helper method. This will just pre-compute the projection and combined matrix

        :param bool update_combined_matrix: if True will also update the combined matrix (projection @ view)
        """
        # apply zoom
        left, right, bottom, top = self._projection
        if self._scale != (1.0, 1.0):
            _right = self._scale[0] * right
            _top = self._scale[1] * top
            left = left + (right - _right)
            bottom = bottom + (top - _top)
            right = _right  # x axis scale
            top = _top  # y axis scale

        self._projection_matrix = pyglet.math.Mat4.orthogonal_projection(left, right, bottom, top, self._near,
                                                                         self._far)
        if update_combined_matrix:
            self._set_combined_matrix()


class SimulationSection(arc.Section):
    def __init__(self, entities_list, entities_alias):

        super().__init__(100 / 1920 * self.window.width,
                         100 / 1200 * self.window.height,
                         1720 / 1920 * self.window.width,
                         1000 / 1200 * self.window.height,
                         local_mouse_coordinates=False,
                         prevent_dispatch_view=['on_key_press'])

        self.entities_list: arc.SpriteList = entities_list
        self.entities_alias: dict[int, BaseEntity] = entities_alias

        self.camera = SmartCamera()
        self.camera_movement_vec = pyglet.math.Vec2(0, 0)
        self.camera_speed = 500
        self.camera_accel = 1
        self.keys_pressed = {'x': [], 'y': []}

        self.quality = 3
        '''self.camera = SmartCamera(viewport=(
            50 / 1920 * self.window.width,
            50 / 1200 * self.window.height,
            1720 / 1920 * self.window.width,
            1100 / 1200 * self.window.height,
        ))'''
        # self.camera.center((0, 0))
        self.camera.zoom = 2

    def set_quality(self):
        zoom = self.camera.zoom ** 2
        q = self.quality
        if zoom <= 5:
            self.quality = 3
        elif 5 < zoom <= 10:
            self.quality = 2
        elif 10 < zoom <= 22:
            self.quality = 1
        else:
            self.quality = 0
        [e.set_quality(self.quality) for e in self.entities_alias.values()]

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.camera.zoom = max(1.5, min(5.0, self.camera.zoom - (scroll_y*self.camera.zoom) / 100))
        self.set_quality()

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int):
        self.camera.move_to((self.camera.position + pyglet.math.Vec2(-dx, -dy) * self.camera.zoom ** 2), 1)

    def on_draw(self):
        self.camera.use()
        self.entities_list.draw()

    def on_update(self, delta_time: float):
        self._handle_keyboard_movement(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol, modifiers:
            case arc.key.ESCAPE, _:
                self.view.processor.quit()
            case key, _:
                if (key == arc.key.W or key == arc.key.S) and key not in self.keys_pressed['y']:
                    self.keys_pressed['y'].append(key)
                elif (key == arc.key.A or key == arc.key.D) and key not in self.keys_pressed['x']:
                    self.keys_pressed['x'].append(key)

    def on_key_release(self, symbol: int, modifiers: int):

        match symbol, modifiers:
            case key, _:
                if (key == arc.key.W or key == arc.key.S) and key in self.keys_pressed['y']:
                    self.keys_pressed['y'].remove(key)
                elif (key == arc.key.A or key == arc.key.D) and key in self.keys_pressed['x']:
                    self.keys_pressed['x'].remove(key)

    def _handle_keyboard_movement(self, delta_time: float):
        if self.keys_pressed['y']:
            match self.keys_pressed['y'][0]:
                case arc.key.W:
                    self.camera_movement_vec += pyglet.math.Vec2(0, 1)
                case arc.key.S:
                    self.camera_movement_vec += pyglet.math.Vec2(0, -1)
        if self.keys_pressed['x']:
            match self.keys_pressed['x'][0]:
                case arc.key.D:
                    self.camera_movement_vec += pyglet.math.Vec2(1, 0)
                case arc.key.A:
                    self.camera_movement_vec += pyglet.math.Vec2(-1, 0)
        self.camera_movement_vec = self.camera_movement_vec.limit(1)
        self.camera.move(
            self.camera.position + self.camera_movement_vec * self.camera_speed * delta_time * self.camera_accel
        )
        self.camera_accel = min(self.camera_accel + 1 * delta_time, 5)
        self.camera_movement_vec *= 0


class SimulationView(arc.View):
    def __init__(self, processor):
        super().__init__()
        self.window.set_mouse_visible(True)

        # self.simulation_camera.anchor = (0, 0)

        self.gui_camera = arc.Camera

        self.processor = processor
        self.entities_list: arc.SpriteList = arc.SpriteList()
        self.entities_alias: dict[int, BaseEntity] = {}
        self.world_age = 0
        self.sim_section = SimulationSection(self.entities_list, self.entities_alias)
        self.add_section(self.sim_section)

        self.tickrate_text = arc.Text(str(self.processor.backend_tickrate), 0, 0, color=arc.color.RED, font_size=20)

    def on_update(self, delta_time: float):
        self.tickrate_text.text = str(self.processor.backend_tickrate)
        self._receive_entities()

    def _receive_entities(self):
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
                e.quality = self.sim_section.quality
            for uid in disappeared:
                self.entities_alias.pop(uid)

            self.entities_list.update()
            self.world_age = self.processor.world_age

    def on_draw(self):
        self.clear(arc.color.DARK_BLUE_GRAY)
        self.window.use()
        self.tickrate_text.draw()
