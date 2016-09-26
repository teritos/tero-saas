import django.dispatch


motion_detected = django.dispatch.Signal(providing_args=["alarm", "active", "filepath"])
