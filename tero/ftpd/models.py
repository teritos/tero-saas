import logging

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class FTPUser(models.Model):

    user = models.OneToOneField(User, models.PROTECT)

    # FTPD permissions
    change_directory = models.BooleanField(help_text="e = change directory (CWD, CDUP commands)",
                                           default=True,)
    list_files = models.BooleanField(help_text=
                                     "l = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)",
                                     default=True)
    retrieve_file = models.BooleanField(help_text=
                                        "r = retrieve file from the server (RETR command)",
                                        default=True)
    append_data = models.BooleanField(help_text=
                                      "a = append data to an existing file (APPE command)",
                                      default=False)
    delete = models.BooleanField(help_text="d = delete file or directory (DELE, RMD commands)",
                                 default=False)
    rename = models.BooleanField(help_text="f = rename file or directory (RNFR, RNTO commands)",
                                 default=False)
    create_dir = models.BooleanField(help_text="m = create directory (MKD command)",
                                     default=False)
    store = models.BooleanField(help_text="w = store a file to the server (STOR, STOU commands)",
                                default=False)
    change_mode_perm = models.BooleanField(help_text=
                                           "M = change mode/permission (SITE CHMOD command)",
                                           default=False)

    @property
    def homedir(self):
        return slugify(self.user.username)

    @property
    def ftpd_perm(self):
        l = [(self.change_directory, 'e'),
             (self.list_files, 'l'),
             (self.retrieve_file, 'r'),
             (self.append_data, 'a'),
             (self.delete, 'd'),
             (self.rename, 'f'),
             (self.create_dir, 'm'),
             (self.store, 'w'),
             (self.change_mode_perm, 'M')]
        perm = map(lambda x: x[1], filter(lambda x: True if x[0] else False, l))
        return ''.join(perm)

    def get_notification_handlers(self, active=False):
        handlers = []
        if active:
            handlers.extend(self.telegramnotificationhandler_set.filter(active=True))
        return handlers

    def get_active_notification_handlers(self):
        return self.get_notification_handlers(active=True)

    def get_notification_handlers_count(self):
        count = self.telegramnotificationhandler_set.count()
        return count

    def __str__(self):
        return "%s - %s (Notification Handlers: %d)" % (self.user,
                                                        self.ftpd_perm,
                                                        self.get_notification_handlers_count())
