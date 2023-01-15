"""
ASGI config for web_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_app.settings')

from channels.routing import URLRouter,ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application
from django.urls import path

http_application = get_asgi_application()

from chat.consumers import ChatConsumer


application = ProtocolTypeRouter({
    'http': http_application,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/',ChatConsumer.as_asgi()),
        ])
    )
})
