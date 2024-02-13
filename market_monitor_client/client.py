import asyncio
import json

from .gatt_server import GATTServer
from .financial_monitor import Config, Monitor


class Client:
    def __init__(self, loop, **kwargs):
        self._monitor_config = Config.from_yaml("config.yml", **kwargs)
        self._monitor = Monitor(self._monitor_config)
        self._gatt_server = GATTServer("Market Monitor", loop)
        self._gatt_server.on_write = self.change_monitor_config

    def change_monitor_config(self, value: str):
        decoded_value = value.decode('utf-8')
        self._monitor.pause = True
        changes = json.loads(decoded_value)
        for k, v in changes.items():
            if hasattr(self._monitor_config, k):
                setattr(self._monitor_config, k, v)
        self._monitor.pause = False

    async def start(self):
        await asyncio.gather(self._monitor.start(), self._gatt_server.start())
    
    async def stop(self):
        await asyncio.gather(self._monitor.stop(), self._gatt_server.stop())
            
