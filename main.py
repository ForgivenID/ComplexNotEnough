import multiprocessing as mp

from app.backend.backend_processor import BackendProcessor
from app.frontend.frontend_processor import FrontendProcessor

from technical.info import CURRENT_VERSION
from technical.funcs import dprint

from technical import config_loader

if __name__ == '__main__':
    dprint(CURRENT_VERSION)
    f_to_b_queue = mp.Queue()
    b_to_f_queue = mp.Queue()
    fp = FrontendProcessor(f_to_b_queue=f_to_b_queue, b_to_f_queue=b_to_f_queue)
    fp.start()
    bp = BackendProcessor(f_to_b_queue=f_to_b_queue, b_to_f_queue=b_to_f_queue)
    bp.start()
