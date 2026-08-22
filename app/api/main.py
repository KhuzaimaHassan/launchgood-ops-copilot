"""ASGI entrypoint for deployment."""

from .app import create_app

app = create_app()
