#!/usr/bin/env python

import asyncio
import signal
import os

import websockets
import json


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        hello,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())