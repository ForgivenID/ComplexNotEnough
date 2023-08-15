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


class World:
    def __init__(self, name):
        # Misc World info
        self.name = name
        self.save_path = Path(SAVES_FOLDER_PATH, f'save-{name}')
        self.savefile_path = Path(self.save_path, f'{name}.cryopreserved')
        while not config:
            ...
        self.settings = config.copy()
        self.variable_timestep = self.settings['physics']['time_step']

        # Simulation info
        self.world_age = 0
        self.entities: list[BaseEntity] = []

        # Physics
        self.space = pmk.Space()
        down = pmk.Segment(self.space.static_body, (0, 0), (1000, 0), 10)
        right = pmk.Segment(self.space.static_body, (1000, 0), (1000, 1000), 10)
        left = pmk.Segment(self.space.static_body, (0, 0), (0, 1000), 10)
        self.space.add(down, right, left)
        self.space.gravity = 0, -10

    def populate(self):
        for _ in range(10):
            e = BaseEntity()
            e.position = pmk.Vec2d(rn.random() * 1000, rn.random() * 1000)
            e.rotation = 360 * rn.random()
            self.entities.append(e)
            self.space.add(e.body, e.shape)

    async def simulate_step(self, processor):
        sub_time_step = self.settings['physics']['time_step'] / self.settings['physics']['iterations_per_tick']
        t1 = time.time()
        [
            entity.update(sub_time_step)
            for entity in self.entities
        ]

        for _ in range(self.settings['physics']['iterations_per_tick'] * self.settings['physics']['sim_speed']):
            self.world_age += sub_time_step
            self.space.step(sub_time_step)
            await asyncio.sleep(sub_time_step)
        dt = self.settings['physics']['time_step'] * self.settings['physics']['sim_speed'] - (time.time() - t1)
        # print(dt)
        if dt > 0:
            p = dt/(self.settings['physics']['time_step'] * self.settings['physics']['sim_speed'])
            print(f"!!! {dt=}, {p:.2f}%")
            await asyncio.sleep(0)
            return
        print(f"??? {dt=}, {dt/self.settings['physics']['time_step']:.2f}%")

    def light_getstate(self) -> tuple[list[tuple[float, float, float, float, tuple[int, int, int, int], int]], int]:
        return [
            (
                entity.position.x,
                entity.position.y,
                entity.rotation,
                entity.size,
                entity.color,
                id(entity),
            )
            for entity in self.entities
        ], self.world_age

    def __getstate__(self):
        return self.name, self.settings, self.world_age, self.entities

    def __setstate__(self, state):
        self.name, self.settings, self.world_age, self.entities = state
        self.save_path = Path(SAVES_FOLDER_PATH, f'save-{self.name}')
        self.savefile_path = Path(self.save_path, f'{self.name}.cryopreserved')


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
            return
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
