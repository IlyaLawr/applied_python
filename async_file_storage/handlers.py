from threading import Thread

import aiohttp
import asyncio
import pyperclip

from configs.config import Config
from file_manager import FileManager


class Handler:
    def __init__(self, node_config: Config, file_manager: FileManager) -> None:
        self._node_config = node_config
        self._file_manager = file_manager
        self._file_extension = self._file_manager.file_extension


    async def handler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        self._file_name = request.path.lstrip('/')
        if self._file_manager.сheck_in_storage(self._file_name):
            return aiohttp.web.FileResponse(f'{self._node_config.storage}/{self._file_name}.{self._file_extension}')
        
        if request.query.get('source', None) == 'node':
            return aiohttp.web.Response(status=404)

        self._name_node_where_file = None
        self._launching_checking_other_nodes()
        if self._name_node_where_file is None:
            return aiohttp.web.Response(status=404)

        try:
            save_file = True if self._name_node_where_file in self._node_config.nodes_from_which_we_save else False
            await self._getting(save=save_file)
            return aiohttp.web.FileResponse(f'{self._node_config.storage}/{self._file_name}.{self._file_extension}') if save_file else aiohttp.web.Response(text=pyperclip.paste())
        finally:
            if save_file:
                self._file_manager.delayed_file_deletion(self._file_name)


    def _launching_checking_other_nodes(self) -> None:
        new_thread_with_event_loop = Thread(target=asyncio.run, args=(self._checking_other_nodes(), ))
        new_thread_with_event_loop.start()
        new_thread_with_event_loop.join()


    async def _checking_other_nodes(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as task_group:
                for node in self._node_config.nodes:
                    task_group.create_task(self._get_and_save_node_name(session, f'{self._node_config.nodes[node]}/{self._file_name}', node))


    async def _get_and_save_node_name(self, session: aiohttp.ClientSession, url: str, node: str) -> None:
            async with session.get(url, params={'source': 'node'}) as response:
                if response.status == 200:
                    self._name_node_where_file = node


    async def _getting(self, save: bool) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self._node_config.nodes[self._name_node_where_file]}/{self._file_name}') as response:
                if save:
                    await self._file_manager.saving_to_storage(response, self._file_name)
                else:
                    pyperclip.copy(await response.text())
