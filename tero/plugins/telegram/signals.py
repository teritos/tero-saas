from core import signals
from django.dispatch import receiver


@receiver(signals.motion_detected)
def on_motion_detected(sender, **kwargs):
    """Movimiento detectado"""
    print(sender)
    print(**kwargs)
