from core import signals
from django.dispatch import receiver


@receiver(signals.userprofile_created)
def on_userprofile_create(sender, **kwargs):
    from plugins.ftpd.models import FTPUser
    userprofile = kwargs.get('userprofile', None)
    if userprofile and not \
            FTPUser.objects.filter(user=userprofile.user).exists():
        FTPUser.objects.create(user=userprofile.user)
