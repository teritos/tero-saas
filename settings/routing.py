"""Channel routes."""
from channels.routing import route


channel_routing = [
    route("websocket.connect", "alarm.consumers.ws_auth"),
    route("websocket.receive", "alarm.consumers.ws_echo"),
    route("websocket.disconnect", "alarm.consumers.ws_disconnect"),
    route("vision.images", "vision.consumers.handle_image"),
]
