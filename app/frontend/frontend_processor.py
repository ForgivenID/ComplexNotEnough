import multiprocessing as mp
import os
import sys

from app.frontend.views.game_views import MainMenu
from app.frontend.windows.base_window import BaseWindow
from technical.funcs import dprint
from technical.info import CURRENT_VERSION

prefix = __file__ if False else sys.path[1]

class FrontendProcessor(mp.Process):
    def __init__(self, f_to_b_queue, b_to_f_queue):
        self.f_to_b_queue: mp.Queue = f_to_b_queue
        self.b_to_f_queue: mp.Queue = b_to_f_queue
        import platform
        super().__init__(name=f'CECE-{CURRENT_VERSION}-{platform.python_version()=}-front')


    def preload_misc(self):
        import arcade as arc
        arc.load_font(os.path.join(prefix, 'assets/Good Times 400.ttf'))

    def send_to_back(self, *args):
        for i in args:
            self.f_to_b_queue.put(i)

    def run(self) -> None:
        import arcade as arc

        dprint(f'process {self.name} started')

        self.preload_misc()

        window = BaseWindow()
        window.show_view(MainMenu(self))

        arc.run()
        self.f_to_b_queue.put('front_exit')
