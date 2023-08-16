import arcade as arc

from technical.settings import ASSETS_FOLDER_PATH, Path

base_body_textures = [
    arc.load_texture(Path(ASSETS_FOLDER_PATH, 'sprites/entities/Base/15.png')),
    arc.load_texture(Path(ASSETS_FOLDER_PATH, 'sprites/entities/Base/40.png')),
    arc.load_texture(Path(ASSETS_FOLDER_PATH, 'sprites/entities/Base/100.png')),
    arc.load_texture(Path(ASSETS_FOLDER_PATH, 'sprites/entities/Base/300.png')),
]

pixelation_alias = [
    15,
    40,
    100,
    300,
]


class BaseEntity:
    def __init__(self, x: float, y: float, diam: float,
                 angle: float, color: arc.color.Color, sprite_list: arc.SpriteList):
        self._position = (x, y)
        self._rotation = angle
        self._size = diam
        self._color = color

        self._quality = 3
        self.body_sprite = arc.Sprite(
            base_body_textures[self._quality],
            scale=self._size / (pixelation_alias[self._quality] * 0.9),
            center_x=8,
            center_y=8
        )
        self.body_sprite.color = color

        sprite_list.append(self.body_sprite)

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, q):
        self._quality = q
        self.body_sprite.texture = base_body_textures[self._quality]
        self.body_sprite.scale = self._size / (pixelation_alias[self._quality] * 0.9)

    def set_quality(self, q):
        self.quality = q

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
        self.body_sprite.scale = self._size / (pixelation_alias[self._quality] * 0.9)

    def draw(self):
        self.body_sprite.draw()

    def disappear(self):
        self.body_sprite.kill()
