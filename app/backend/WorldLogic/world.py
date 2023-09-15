import asyncio
import pickle as pk
import time

import pymunk as pmk

from pathlib import Path

from app.backend.Entities.base_entity import BaseEntity
from technical.settings import CFG_FOLDER_PATH, CWD_PATH

import random as rn

from technical.config_loader import config
from technical.settings import SAVES_FOLDER_PATH

boundary_points = [
    (-100, -30), (-100, 300), (0, 300), (0, 0), (1000, 0), (1000, 300), (1100, 300), (1100, -30)
]

ShortEntityData = dict[int, tuple[float, float, float, float,
tuple[int, int, int, int], int]]


class World:
    def __init__(self, name):
        # Misc World info
        self.name = name
        self.save_path = Path(SAVES_FOLDER_PATH, f'save-{name}')
        self.savefile_path = Path(self.save_path, f'{name}.cryopreserved')
        self.tickrate = 0
        while not config:
            ...
        self.settings = config.copy()

        # Simulation info
        self.world_age = 0
        self.entities: list[BaseEntity] = []

        self._setup_space()

    def _setup_space(self):
        radius = self.settings['world']['petridish_radius']

        self.space = pmk.Space()
        self.space.use_spatial_hash(20, 30000)
        down = pmk.Segment(self.space.static_body, (-radius, -radius), (radius, -radius), 10)
        right = pmk.Segment(self.space.static_body, (radius, -radius), (radius, radius), 10)
        left = pmk.Segment(self.space.static_body, (-radius, -radius), (-radius, radius), 10)
        top = pmk.Segment(self.space.static_body, (-radius, radius), (radius, radius), 10)
        [e._set_elasticity(1.0) for e in [down, right, left, top]]
        self.space.add(down, right, left, top)
        self.space.gravity = 0, 0

    def generate(self):
        ...

    def populate(self):
        for _ in range(10000):
            e = BaseEntity(self)
            e.position = pmk.Vec2d((rn.random() - .5) * 9000, (rn.random() - .5) * 9000)
            e.rotation = 360 * rn.random()
            self.entities.append(e)
            self.space.add(*e.objects)
            e.body.apply_impulse_at_local_point((100, 20), (0, 0))

    async def simulate_step(self, processor):
        sub_time_step = self.settings['physics']['time_step'] / self.settings['physics']['iterations_per_tick']
        t1 = time.time()
        for _ in range(self.settings['physics']['sim_speed']):
            for _ in range(self.settings['physics']['iterations_per_tick']):
                self.space.step(1 / 60 / self.settings['physics']['iterations_per_tick'])
            [
                entity.update(sub_time_step)
                for entity in self.entities
            ]
            if -.1 < 1 / 60 - (time.time() - t1) < .1:
                processor.send_single_tick()
        self.world_age += 1 / 60
        processor.send_single_tick()
        dt = 1 / 60 - (time.time() - t1)
        # print(dt)
        if dt > 0:
            p = dt / (self.settings['physics']['time_step'] * self.settings['physics']['sim_speed'])
            # print(f"!!! {dt=}, {p:.2f}%")
            await asyncio.sleep(dt)
            return
        # print(f"??? {dt=}, {dt / self.settings['physics']['time_step']:.2f}%")

    def light_getstate(self) -> tuple[ShortEntityData, int]:
        return {id(entity): (
            entity.position.x,
            entity.position.y,
            entity.rotation,
            entity.size,
            entity.color,
            id(entity),
        )
            for entity in self.entities
        }, self.world_age

    def __getstate__(self):
        return self.name, self.settings, self.world_age, self.entities

    def __setstate__(self, state):
        self.name, self.settings, self.world_age, self.entities = state
        self.save_path = Path(SAVES_FOLDER_PATH, f'save-{self.name}')
        self.savefile_path = Path(self.save_path, f'{self.name}.cryopreserved')

        self._setup_space()

        self.space.add(*[o for e in self.entities for o in e.objects])


class WorldLoader:
    def __init__(self, processor):
        self.processor = processor
        self.world: World | None = None

    def load_world(self, name):
        with open(Path(SAVES_FOLDER_PATH, f'save-{name}/{name}.cryopreserved'), 'rb') as savefile:
            self.world = pk.load(savefile)

    def save_world(self):
        if not self.loaded:
            raise Warning('Tried to save while not loaded.')
        Path(SAVES_FOLDER_PATH, f'save-{self.world.name}').mkdir(parents=True, exist_ok=True)
        with open(Path(SAVES_FOLDER_PATH, f'save-{self.world.name}/{self.world.name}.cryopreserved'), 'wb') as savefile:
            pk.dump(self.world, savefile)

    def unload_world(self):
        self.save_world()
        self.world = None

    def new_world(self, name):
        self.world = World(name)
        self.world.populate()
        self.save_world()

    @property
    def loaded(self):
        return bool(self.world)

    def __bool__(self):
        return self.loaded
