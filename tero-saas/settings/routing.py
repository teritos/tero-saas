from channels.routing import route


channel_routing = [
    route("messenger.telegram", "telegram.consumers.telegram_consumer"),
]
