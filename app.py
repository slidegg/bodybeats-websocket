#!/usr/bin/env python

import asyncio
import signal
import os

import websockets
import json


async def echo(websocket):
    async for message in websocket:
        # dictData = json.load(message)
        dictData = json.dumps(message, separators=(',', ':'))
        # await websocket.send(json.dumps(message, separators=(',', ':')))
        await websocket.send(dictData)
        # await websocket.send(dictData['name'])


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())