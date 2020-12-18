import yaml


CONFIG_DIR= "config/"
CONFIG_FILE = {
    'scraper': 'scraper.yaml',
    'actions': 'actions.yaml',
}


class Config:
    def __init__(self):
        self.path = str()
        self.config = dict()

    def get_config_data(self):
        with open(self.path, "r") as stream:
            self.config = yaml.safe_load(stream)