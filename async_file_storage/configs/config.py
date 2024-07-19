import yaml


class Config:
    def __init__(self, path: str) -> None:
        with open(path, 'r') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)

        self.host = config['host']
        self.port = config['port']
        self.name = config['name']
        self.storage = config['storage']
        self.file_lifetime = config['file_lifetime']
        self.nodes = config['nodes']
        self.nodes_from_which_we_save = config['nodes_from_which_we_save']
