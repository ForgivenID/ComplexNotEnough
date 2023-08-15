import sys
from os import getenv
from pathlib import Path

import __main__

...

#    ----------
#   PATH OPTIONS
#    ----------
APP_FOLDER_PATH = Path(getenv('LOCALAPPDATA'), 'FYDEs Lil Projects/ComplexNotEnough')
SAVES_FOLDER_PATH = Path(APP_FOLDER_PATH, 'saves')
CFG_FOLDER_PATH = Path(APP_FOLDER_PATH, 'cfg')

CWD_PATH = Path(__main__.__file__).parent if hasattr(__main__, '__file__') else sys.path[1]
ASSETS_FOLDER_PATH = Path(CWD_PATH, 'assets')

...

#    -----------
#   DEBUG OPTIONS
#    -----------
DEBUG = True
SKIP_STARTUP = False

...

#  ---------------
# GRAPHICAL OPTIONS
#  ---------------
FULLSCREEN = True

...
