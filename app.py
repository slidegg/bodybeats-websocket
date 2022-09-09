#!/usr/bin/env python

import asyncio
import signal
import os
import websockets
import json
import random

from bodybeats import bodybeats

JOIN = {}

# REFFERENCE
async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def hello(websocket):
    await websocket.send('hey dude whats ur name?')
    name = await websocket.recv()
    greeting = f"Hello {name}!"
    await websocket.send(greeting)
    await echo(websocket)

# END OF REFERENCE

async def error(websocket, message):
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def play(websocket, game, player, connected):
    """
    Receive and process moves from a player.

    Expects json like
    {"type": "play", "sound": "messageFromApp"}

    """
    await websocket.send('Joined to the session! Now lets rock!')

    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        move = event["sound"]

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "player": player,
            "move": move
        }
        websockets.broadcast(connected, json.dumps(event))



async def start(websocket):
    """
    Handle a connection from the first player: start a new game.

    """
    # Initialize a music session, the set of WebSocket connections
    # receiving moves from this game, and secret access tokens.
    await websocket.send('The game starts now...')
    
    game = bodybeats()
    connected = {websocket}

    join_key = random.randint(1111,9999)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access tokens to the first player,
        # where they'll be used for building "join" links.
        event = {
            "type": "init",
            "join": join_key
        }
        # send the join key
        await websocket.send(str(join_key))
        await websocket.send('Type your instrument...')
        instrument = await websocket.recv()
        # Receive and process sounds from the first player.
        await play(websocket, game, instrument, connected)
    finally:
        del JOIN[join_key]


async def join(websocket, join_key):
    """
    Handle a connection from the second player: join an existing game.

    """
    # Find the bodybeats game.
    try:
        game, connected = JOIN[int(join_key)]
    except KeyError:
        await error(websocket, "Session not found :(")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        await websocket.send('Joined! Type your instrument...')
        instrument = await websocket.recv()
        # Receive and process moves from the second player.
        await play(websocket, game, instrument, connected)
    finally:
        connected.remove(websocket)


async def handler(websocket):
    """
    Handle a connection and dispatch it according to who is connecting.
    
    Expects a join key as a string or for new game
    { "type": "init" } 

    """
    await websocket.send('You are connected to the websocket! Now provide the event!')
    # Receive and parse the "init" event.
    message = await websocket.recv()

    if message  == 'init':
        await websocket.send('Starting the game...')
        # First player starts a new game.
        await start(websocket)
    else:
        # Second player joins an existing game.
        await websocket.send('Joining the game...')
        await join(websocket, message)
        

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        handler,
        host="",
        port=int(os.environ["PORT"]),
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())