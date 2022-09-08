#!/usr/bin/env python

import asyncio
import signal
import os
import redis
import websockets
import json


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def hello(websocket):
    await websocket.send('hey dude whats ur name?')
    name = await websocket.recv()
    greeting = f"Hello {name}!"
    await websocket.send(greeting)

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        hello,
        echo,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())