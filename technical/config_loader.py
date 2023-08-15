from shutil import copy2

import yaml

from technical.settings import CFG_FOLDER_PATH, ASSETS_FOLDER_PATH, Path

Path(CFG_FOLDER_PATH).mkdir(parents=True, exist_ok=True)

if not Path(CFG_FOLDER_PATH, 'cfg.yml').exists() or True:
    copy2(Path(ASSETS_FOLDER_PATH, 'standard_config.yml'), Path(CFG_FOLDER_PATH, 'cfg.yml'))


with open(Path(CFG_FOLDER_PATH, 'cfg.yml')) as f:
    config = yaml.load(f, yaml.FullLoader)
