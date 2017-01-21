"""Channel routes."""
from channels.routing import route


channel_routing = [
    route("messenger.telegram", "telegram.consumers.telegram_consumer"),
    route("websocket.connect", "mordor.consumers.ws_auth"),
    route("websocket.receive", "mordor.consumers.ws_echo"),
    route("websocket.disconnect", "mordor.consumers.ws_disconnect"),
    route("mordor.images", "mordor.consumers.handle_image"),
]
