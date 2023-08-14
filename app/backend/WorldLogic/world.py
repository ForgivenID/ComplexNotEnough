import asyncio
import pickle as pk
from asyncio import Future
import pymunk as pmk

from shutil import copy2
from pathlib import Path

from app.backend.Entities.base_entity import BaseEntity
from technical.settings import CFG_FOLDER_PATH, CWD_PATH

from technical.config_loader import config
from technical.settings import SAVES_FOLDER_PATH

class World:
    def __init__(self, name):
        # Misc World info
        self.name = name
        self.save_path = Path(SAVES_FOLDER_PATH, f'save-{name}')
        self.savefile_path = Path(self.save_path, f'{name}.cryopreserved')
        self.settings = config

        # Simulation info
        self.world_age = 0
        self.entities = []

        # Physics
        self.space = pmk.Space()

    def populate(self):
        for _ in range(10):
            e = BaseEntity()
            self.entities.append(e)
            self.space.add(e.body, e.shape)

    def simulate_step(self):
        self.space.step(1 / self.settings['physics']['calculations_per_second'])

    def light_getstate(self):
        return [(entity.position, entity.size, entity.color) for entity in self.entities], self.world_age

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
        self.save_world()

    @property
    def loaded(self):
        return bool(self.world)

    def __bool__(self):
        return self.loaded

