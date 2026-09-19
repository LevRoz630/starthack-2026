"""Vercel entry point: the same Starlette app, on a serverless function.

Only the request/response half of the API works here. The live call needs a socket
shared between the phone and whatever is driving the call, and on Vercel each
WebSocket binds to one function instance with no guarantee the next connection
lands on the same one -- so /ws, /listen and the demo pipeline stay on a real
server (a tunnel, or any host that runs the process). See README "Hosting".
"""

from backend.api import app

__all__ = ['app']
