import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing
from .middleware import QueryAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": QueryAuthMiddleware(
        AuthMiddlewareStack(
                URLRouter(
                        routing.websocket_urlpatterns
                )
        )
    ),
})
