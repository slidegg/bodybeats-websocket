#!/usr/bin/env python

import asyncio
import signal
import os
import websockets
import json
import secrets

from bodybeats import PLAYER1, PLAYER2, bodybeats

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

    """
    async for message in websocket:
        # Parse a "play" event from the UI.
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        # Send a "play" event to update the UI.
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        websockets.broadcast(connected, json.dumps(event))

        # If move is winning, send a "win" event.
        # if game.winner is not None:
        #     event = {
        #         "type": "win",
        #         "player": game.winner,
        #     }
        #     websockets.broadcast(connected, json.dumps(event))



async def start(websocket):
    """
    Handle a connection from the first player: start a new game.

    """
    # Initialize a music session, the set of WebSocket connections
    # receiving moves from this game, and secret access tokens.
    await websocket.send('The game starts now...')
    
    game = bodybeats()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access tokens to the first player,
        # where they'll be used for building "join" links.
        event = {
            "type": "init",
            "join": join_key
        }
        await websocket.send(json.dumps(event))
        # Receive and process moves from the first player.
        await play(websocket, game, PLAYER1, connected)
    finally:
        del JOIN[join_key]


async def join(websocket, join_key):
    """
    Handle a connection from the second player: join an existing game.

    """
    # Find the bodybeats game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Beat not found :(")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Receive and process moves from the second player.
        await play(websocket, game, PLAYER2, connected)
    finally:
        connected.remove(websocket)


async def handler(websocket):
    """
    Handle a connection and dispatch it according to who is connecting.
    Expects a json like
    {"event": { 
        "type": "init",
         "join": "join_key"
         }
    }

    or for new game
    { "event": { "type": "init" } }

    """
    await websocket.send('You are connected to the websocket! Now provide the event!')
    # Receive and parse the "init" event.
    message = await websocket.recv()
    event = json.loads(message)
    # assert event["type"] == "init"
    await websocket.send(type(message))

    if "join" in event:
        # Second player joins an existing game.
        await join(websocket, event["join"])
    else:
        await websocket.send('Starting the game...')
        # First player starts a new game.
        await start(websocket)


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