"""Utils related with Django Channels."""
from channels import Group
from django.utils.text import slugify


def get_group_name_by(username):
    """Return an alarm group name by given username."""
    return slugify("alarm-%s" % username)


def send_message_by_ws(message, username):
    """Send a message to given username."""
    group_name = get_group_name_by(username)
    send_message_to_group(message, group_name)


def send_message_to_group(message, group_name):
    """Send message to a group."""
    assert isinstance(message, dict), "message must be a dict instance."
    group = Group(group_name)
    group.send(message)


def get_alarm_group(user):
    """Return a django channels Group for given user."""
    group_name = get_group_name_by(user.username)
    group = Group(group_name)
    return group
