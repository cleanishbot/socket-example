# Socket examples

So yeah, this is a thing...

## Blocking example from https://www.geeksforgeeks.org/socket-programming-python/

Client connects to the server and gets sent two messages.

in really-simple-socket

> poetry run python .\really-simple-socket\server.py

> poetry run python .\really-simple-socket\client.py

## Non-blocking example from https://www.demo2s.com/python/python-socket-and-selectors-non-blocking-communication-and-timeouts.html

Echo server and client, original disconnected when all the messages were sent but this doesn't

in src

> poetry run python .\src\server.py

> poetry run python .\src\client.py