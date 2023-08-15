import arcade as arc

from technical.settings import ASSETS_FOLDER_PATH, Path


class BaseEntity:
    def __init__(self, x: float, y: float, diam: float,
                 angle: float, color: arc.color.Color, sprite_list: arc.SpriteList):
        self._position = (x, y)
        self._rotation = angle
        self._size = diam
        self._color = color
        body_texture = arc.sprite.sprite.load_texture(Path(ASSETS_FOLDER_PATH, 'sprites/entities/Base/100.png'))
        self.pixelation = 100
        self.body_sprite = arc.Sprite(body_texture, scale=self._size / (self.pixelation * 0.9), center_x=8, center_y=8)
        self.body_sprite.color = color

        sprite_list.append(self.body_sprite)

    def update(self, x, y, diam, angle, color):
        self._position = (x, y)
        self._rotation = angle
        self._size = diam
        self._color = color
        self._update()

    def _update(self):
        self.body_sprite.position = self._position
        self.body_sprite.angle = self._rotation
        self.body_sprite.color = self._color
        self.body_sprite.scale = self._size / (self.pixelation * 0.9)

    def draw(self):
        self.body_sprite.draw()
