import logging
from typing import Any

from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)

class GATTServer:
    def __init__(self, name: str):
        self.name = name
        self.gatt = {
            "A07498CA-AD5B-474E-940D-16F1FBE7E8CD": {
                "664161df-1bae-4003-968f-5b5a6713cde4": {
                    "Properties": (
                        GATTCharacteristicProperties.read
                        | GATTCharacteristicProperties.write
                    ),
                    "Permissions": (
                        GATTAttributePermissions.readable
                        | GATTAttributePermissions.writeable
                    ),
                    "Value": None,
                },
                "22b2d76a-a1dd-48be-90c7-092f07e8fd56": {
                    "Properties": (
                        GATTCharacteristicProperties.read
                        | GATTCharacteristicProperties.write
                    ),
                    "Permissions": (
                        GATTAttributePermissions.readable
                        | GATTAttributePermissions.writeable
                    ),
                    "Value": None,
                },
            },
        }
        self._server = BlessServer(self.name)
        self._server.read_request_func = self._read_request
        self._server.write_request_func = self._write_request
        self._on_write = None
    
    @property
    def on_write(self):
        return self._on_write

    @on_write.setter
    def on_write(self, value):
        self._on_write = value
        
    def _read_request(self, characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
        logging.debug(f"Reading {characteristic.value}")
        return characteristic.value

    def _write_request(self, characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        characteristic.value = value
        logging.debug(f"Char value set to {characteristic.value}")
        if self.on_write:
            self.on_write(characteristic.value)

    async def start(self):
        await self._server.add_gatt(self.gatt)
        await self._server.start()

    async def stop(self):
        await self._server.stop()
