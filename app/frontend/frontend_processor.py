import multiprocessing as mp
import asyncio
import os
import queue
import sys

from app.frontend.views.game_views import MainMenu
from app.frontend.windows.base_window import BaseWindow
from technical.funcs import dprint
from technical.info import CURRENT_VERSION

import arcade as arc

prefix = __file__ if False else sys.path[1]


class FrontendProcessor(mp.Process):
    def __init__(self, f_to_b_queue, b_to_f_queue):
        self.f_to_b_queue: mp.Queue = f_to_b_queue
        self.b_to_f_queue: mp.Queue = b_to_f_queue
        self.world_age = 0
        self.entities: dict[int, tuple] = {}
        self.backend_tickrate = 0
        self.selection_data = {}
        import platform
        super().__init__(name=f'CNE-{CURRENT_VERSION}-{platform.python_version()=}-front')

    def preload_misc(self):
        arc.load_font(os.path.join(prefix, 'assets/Good Times 400.ttf'))

    def send_to_back(self, *args):
        [self.f_to_b_queue.put(i) for i in args]

    def run(self) -> None:

        dprint(f'process {self.name} started')

        self.preload_misc()

        window = BaseWindow()
        window.show_view(MainMenu(self))
        arc.schedule(self.connection_process, 1/60)
        arc.run()

    def quit(self):
        self.send_to_back('front_exit')
        arc.exit()

    def connection_process(self, _):
        if self.b_to_f_queue.empty():
            return

        data = self.b_to_f_queue.get()

        match data:

            case 'drawables', drawables:
                self.entities, self.world_age = drawables
                print(len(self.entities))

            case 'tickrate', tickrate:
                self.backend_tickrate = tickrate

            case 'back_exit' | 'exit':
                dprint('frontend exited')
                self.quit()

            case _:
                dprint(f"frontend received some data and couldn't process it: {data=}")
