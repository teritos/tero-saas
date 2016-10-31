import logging

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class FTPAccount(models.Model):

    alarm = models.OneToOneField('alarm.Alarm', on_delete=models.PROTECT)

    @property
    def homedir(self):
        return slugify(self.alarm.id)

    @property
    def ftpd_perm(self):
        # e = change directory (CWD, CDUP commands)
        # l = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)
        # r = retrieve file from the server (RETR command)
        # a = append data to an existing file (APPE command)
        # m = create directory (MKD command)",
        # w = store a file to the server (STOR, STOU commands)",
        # f = rename file or directory (RNFR, RNTO commands)",
        # d = delete file or directory (DELE, RMD commands)",
        # M = change mode/permission (SITE CHMOD command)",
        return 'elamw'.join(perm)

    def __str__(self):
        return self.alarm.id
