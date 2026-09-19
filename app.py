"""Vercel entry point: the Starlette app, discovered by Vercel's Python preset.

Only the request/response half works on a serverless function. The live call needs a
socket shared between the phone and whatever drives the call, and Vercel binds each
WebSocket to one function instance with no guarantee the next connection lands on the
same one -- so /ws, /listen and the demo pipeline need a real server (a tunnel, or any
host that runs the process).
"""

from backend.api import app

__all__ = ['app']
