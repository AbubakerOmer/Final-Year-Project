from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from chat.consumers import EchoConsumer,ChatConsumer
from channels.auth import AuthMiddlewareStack

application=ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(URLRouter([
        path('ws/chat/<str:username>/',ChatConsumer.as_asgi()),
        path('ws/chat/',EchoConsumer.as_asgi())
    ])
    )
})
