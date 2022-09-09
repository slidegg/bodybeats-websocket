## BodyBeats Websocket
##### A websocket writen in python using websockets, a library for building WebSocket servers and clients, to enable multiplayer functionality for bodybeats app. Websockets is builded on top of asyncio, Python’s standard asynchronous I/O framework.
###### Heroku is used for the deployment of the app. Developed for 2022 Shape Weekend.

**The wss address is:   ```wss://bodybeats.herokuapp.com/ ```**

### Process
* First a player need to join a game. If he's the first player who creates the session then he needs to pass a string with the word "init" OR if he wants to join to another game then a string with the join key (4 digit pin code).


* After that every player need to pass the name of the instrument as a simple string.


* Finally, the player starts to play and passes json messages like this
    ``` 
    {"type": "play", "sound": "messageFromApp"}
    ```


<ins>[Used Library Documentation](https://websockets.readthedocs.io/en/stable/)</ins>