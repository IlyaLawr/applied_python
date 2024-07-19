from threading import Thread

from aiohttp import web

from handlers import Handler
from file_manager import FileManager
from configs.config import Config


class FileDaemon(Thread):
    def __init__(self, config_path) -> None:
        super().__init__()
        self._config = Config(config_path)
        self._file_manager = FileManager(self._config, file_extension='txt')
        self._handler = Handler(self._config, self._file_manager)


    def run(self):
        app = web.Application()
        app.add_routes([web.get(r'/{file_name:\w+}', self._handler.handler)])
        web.run_app(app, host=self._config.host, port=self._config.port)
