import logging
import asyncio

import argparse

from market_monitor_client import Client

if __name__ == "__main__":
    logging.basicConfig()
    logging.root.setLevel(level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    client = Client(loop, dev=args.dev)
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        asyncio.run(client.stop())
