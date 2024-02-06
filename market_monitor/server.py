import logging
import asyncio
import json

from typing import Any

from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)


class Server:
    def __init__(self, loop, market_monitor=None):
        # Instantiate the server
        self.gatt = {
            "A07498CA-AD5B-474E-940D-16F1FBE7E8CD": {
                "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B": {
                    "Properties": (
                        GATTCharacteristicProperties.read
                        | GATTCharacteristicProperties.write
                        | GATTCharacteristicProperties.indicate
                    ),
                    "Permissions": (
                        GATTAttributePermissions.readable
                        | GATTAttributePermissions.writeable
                    ),
                    "Value": None,
                },
                "bfc0c92f-317d-4ba9-976b-cc11ce77b4ca": {
                    "Properties": (
                        GATTCharacteristicProperties.read
                        | GATTCharacteristicProperties.write
                        | GATTCharacteristicProperties.indicate
                    ),
                    "Permissions": (
                        GATTAttributePermissions.readable
                        | GATTAttributePermissions.writeable
                    ),
                    "Value": None,
                },
            },
        }
        my_service_name = "Market Monitor"
        self.server = BlessServer(name=my_service_name, loop=loop)
        self.server.read_request_func = self.read_request
        self.server.write_request_func = self.write_request

    def read_request(
        self, characteristic: BlessGATTCharacteristic, **kwargs
    ) -> bytearray:
        logging.debug(f"Reading {characteristic.value}")
        return characteristic.value

    def write_request(
        self, characteristic: BlessGATTCharacteristic, value: Any, **kwargs
    ):
        characteristic.value = value
        logging.debug(f"Char value set to {characteristic.value}")

    async def stop(self):
        await self.server.stop()
        logging.debug("BLE server stopped successfully")

    async def start(self):

        await self.server.add_gatt(self.gatt)
        await self.server.start()
        self.server.get_characteristic("51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B").value = (
            json.dumps(
                [
                    {"name": "BTC", "ticker": "BTC-USD"},
                    {"name": "S&P 500", "ticker": "^GSPC"},
                ]
            ).encode("utf-8")
        )
        self.server.get_characteristic("bfc0c92f-317d-4ba9-976b-cc11ce77b4ca").value = 20
        self.server.update_value(
            "A07498CA-AD5B-474E-940D-16F1FBE7E8CD",
            "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B",
        )
        self.server.update_value(
            "A07498CA-AD5B-474E-940D-16F1FBE7E8CD",
            "bfc0c92f-317d-4ba9-976b-cc11ce77b4ca",
        )
        logging.debug("Advertising")
