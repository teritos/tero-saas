"""Tero FTPD Authorizers."""
import os
import logging

from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from django.contrib.auth import authenticate
from alarm.models import Alarm
from ftpd.models import FTPAccount


logger = logging.getLogger("ftpd")  # pylint: disable=C0103


class FTPDjangoUserAuthorizer(DummyAuthorizer):
    """
    FTPD Authorizer that use DJANGO users decorated with FTPUser model
    """

    def __init__(self, rootdir):
        self.root = rootdir
        super(FTPDjangoUserAuthorizer, self).__init__()

    def validate_authentication(self, username, password, handler):
        """Validate user and password."""
        _ = handler
        logger.info("Authenticating user %s...", username)
        user = authenticate(username=username, password=password)
        if not user:
            logger.info('Authentication failed for user %s with password %s', username, password)
            raise AuthenticationFailed()

        if not Alarm.is_active_for(username):
            logger.info('User %s alarm is deactivated, ignoring session', username)
            raise AuthenticationFailed()

        try:
            ftp_user = FTPAccount.objects.get(alarm__owner=user)  # pylint: disable=E1101
            homedir = ftp_user.homedir
            perm = ftp_user.ftpd_perm
            root_homedir = os.path.join(self.root, homedir)
            os.makedirs(root_homedir, exist_ok=True)
            if not self.has_user(username):
                self.add_user(username, password, root_homedir, perm)
        except FTPAccount.DoesNotExist:  # pylint: disable=E1101
            logger.info(
                "User %s with password %s doesnt have an FTPAccount related object.",
                username,
                password
                )
            raise AuthenticationFailed()
