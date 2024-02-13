import logging
import asyncio

import argparse

from market_monitor_client import Client

if __name__ == "__main__":
    logging.basicConfig()
    logging.root.setLevel(level=logging.DEBUG)
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()
    client = Client(dev=args.dev)
    try:
        client.start()
    except KeyboardInterrupt:
        asyncio.run(client.stop())
