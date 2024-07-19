from datetime import datetime, timedelta
from collections.abc import Callable
from dataclasses import dataclass
from threading import Thread
from queue import Queue
from time import sleep
import os

from aiohttp.web import FileResponse
from aiofiles import open

from configs.config import Config


@dataclass
class RemovalInfo:
    file_name: str
    removal_time : int


class FileManager:
    def __init__(self, node_config: Config,  file_extension: str) -> None:
        self.storage_path = node_config.storage
        self.node_name = node_config.name
        self.file_extension = file_extension
        self.file_lifetime = node_config.file_lifetime


    async def saving_to_storage(self, response: FileResponse, file_name: str) -> None:
        async with open(f'{self.storage_path}/{file_name}.{self.file_extension}', 'wb') as fd:
            async for chunk in response.content.iter_chunked(1024):
                await fd.write(chunk)


    def deleting_from_storage(self, file_name: str) -> None:
        os.remove(f'{self.storage_path}/{file_name}.{self.file_extension}')


    def сheck_in_storage(self, file_name: str) -> bool:
        return True if os.path.exists(f'{self.storage_path}/{file_name}.{self.file_extension}') else False


    def delayed_file_deletion(self, file_name: str) -> None:
        self.file_deletion_queue_handler = FileDeletionQueueHandler(self.node_name, self.file_lifetime, self.deleting_from_storage)
        self.file_deletion_queue_handler.start()

        self.file_deletion_queue_handler.add(self._creating_information_about_deletions(file_name))


    def _creating_information_about_deletions(self, file_name: str) -> RemovalInfo:
        return RemovalInfo(file_name, datetime.now() + timedelta(seconds=self.file_lifetime))  


class FileDeletionQueueHandler(Thread):
    def __init__(self, name_node: str, file_lifetime: int, delete_function: Callable) -> None:
        super().__init__()
        self._name_node = name_node
        self._file_lifetime = file_lifetime
        self._delete_function = delete_function


    def run(self) -> None:
        exec(f'self._delete_queue_{self._name_node} = Queue()')
        while True:
            removal_info = eval(f'self._delete_queue_{self._name_node}').get()
            sleep((removal_info.removal_time - datetime.now()).seconds)
            self._delete_function(removal_info.file_name)


    def add(self, removal_info: RemovalInfo) -> None:
        eval(f'self._delete_queue_{self._name_node}').put(removal_info)
