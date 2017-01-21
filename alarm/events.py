"""Alarm Event names"""

from observer import Observable
import logging

LOGGER = logging.getLogger('alarm')

# Events
MOTION_DETECTED = 'motion_detected'

# Basic handlers
def log_it(*args, **kwargs):
    LOGGER.debug("%s, %s", args, kwargs)


# Setup events
observable = Observable()
observable.on(MOTION_DETECTED, [log_it])

