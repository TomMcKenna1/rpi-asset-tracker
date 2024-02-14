import asyncio
import json
import logging

from .gatt_server import GATTServer
from .financial_monitor import Config, Monitor


class Client:
    def __init__(self, **kwargs):
        self.loop = asyncio.get_event_loop()
        self._monitor_config = Config.from_yaml("config.yml", **kwargs)
        self._monitor = Monitor(self._monitor_config)
        self._gatt_server = GATTServer("Market Monitor", self.loop)
        self._gatt_server.on_write = self.change_monitor_config

    def change_monitor_config(self, value: str):
        logging.debug(value)
        decoded_value = value.decode('utf-8')
        logging.debug(decoded_value)
        self._monitor.pause = True
        changes = json.loads(decoded_value)
        for k, v in changes.items():
            if hasattr(self._monitor_config, k):
                setattr(self._monitor_config, k, v)
        self._monitor.pause = False

    def start(self):
        self.loop.run_until_complete(asyncio.gather(self._monitor.start(), self._gatt_server.start()))
    
    def stop(self):
        self.loop.run_until_complete(asyncio.gather(self._monitor.stop(), self._gatt_server.stop()))
            
