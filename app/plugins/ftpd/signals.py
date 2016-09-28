from core import signals
from django.dispatch import receiver


@receiver(signals.userprofile_created)
def on_userprofile_create(sender, **kwargs):
    from plugins.ftpd.models import FTPUser
    import ipdb; ipdb.set_trace()
    if not FTPUser.objects.filter(user=user).exists():
        FTPUser.objects.create(user=user)
