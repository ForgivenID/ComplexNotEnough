import multiprocessing as mp

import asyncio
from asyncio import AbstractEventLoop

from app.backend.WorldLogic.world import WorldLoader
from technical.funcs import dprint
from technical.info import CURRENT_VERSION
import uuid
import pymunk as pmk


class BackendProcessor(mp.Process):
    def __init__(self, f_to_b_queue, b_to_f_queue):

        self.f_to_b_queue: mp.Queue = f_to_b_queue
        self.b_to_f_queue: mp.Queue = b_to_f_queue
        self.loop: AbstractEventLoop | None = None
        self.kill_switch: asyncio.Event | None = None
        self.world_loader: WorldLoader | None = None

        import platform

        super().__init__(name=f'CECE-{CURRENT_VERSION}-{platform.python_version()=}-back')

    def run(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.kill_switch = asyncio.Event()
        dprint(f'process {self.name} started')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_coroutines())

    async def run_coroutines(self):
        await asyncio.gather(self.connection_process(), self.simulation_process())

    async def simulation_process(self):
        while not (self.world_loader or self.kill_switch.is_set()):
            await asyncio.sleep(2)

        while not self.kill_switch.is_set():
            self.world_loader.world.simulate_step()
            if self.b_to_f_queue.qsize():
                self.b_to_f_queue.put(('entities', self.world_loader.world.light_getstate()))
            await asyncio.sleep(0)

    async def connection_process(self):
        # ------------
        # processors
        # ------------
        def process_cmd(command):
            match command:
                case 'load_world', *args:
                    ...

                case 'new_world', *args:
                    dprint('new_world')
                    if not self.world_loader:
                        self.world_loader = WorldLoader(self)
                    self.world_loader.new_world(str(uuid.uuid4()))

                case _:
                    dprint(f"backend received a cmd and couldn't process it: {command=}")

        def process_request(request):
            match request:
                case 'set_viewport', *args:
                    ...

                case 'get_data', *args:
                    ...

                case 'get_simulation_speed', *args:
                    ...

                case 'set_simulation_speed', *args:
                    ...

                case _:
                    dprint(f"backend received a request and couldn't process it: {request=}")

        # ------------
        # process loop
        # ------------
        while not self.kill_switch.is_set():
            data = await self.loop.run_in_executor(None, self.f_to_b_queue.get)
            match data:

                case 'cmd', *cmd:

                    process_cmd(cmd)

                case 'request', *req:

                    process_request(req)

                case 'front_exit' | 'exit':

                    self.kill_switch.set()
                    break

                case _:
                    dprint(f"backend received some data and couldn't process it: {data=}")
