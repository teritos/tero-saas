import logging
import telegram

from django.db import models
from telegram.error import TelegramError

from notifications.models import NotificationHandler
from django.core.exceptions import PermissionDenied


logger = logging.getLogger(__name__)


class TelegramBot(models.Model):

    name = models.CharField(max_length=25, null=False, primary_key=True)
    # allows more than one telegram bot implementation with the same token
    token = models.CharField(max_length=100, null=False, unique=True)

    module_name = models.CharField(max_length=25, null=True)

    def __str__(self):
        return "@%s" % self.name

    def _get_telegram_bot(self):
        return telegram.Bot(token=self.token)

    def subscribe(self, nup):
        self.telegramnotificationhandler.subscribe(nup)

    def unsubscribe(self, nup):
        self.telegramnotificationhandler.unsubscribe(nup)

    def is_active(self):
        return self.telegramnotificationhandler.ftp_user.user.is_active

    def is_subscribed(self, nup):
        return self.telegramnotificationhandler.subscribers.filter(id=nup.id).exists()

    def toggle_activate(self, nup, value):
        if not nup.user.is_superuser:
            raise PermissionDenied()
        ftp_user = self.telegramnotificationhandler.ftp_user
        logger.debug("Changing is_active = %s... %s", value, ftp_user.user)
        ftp_user.user.is_active = value
        logger.debug("Saving associated user...")
        ftp_user.user.save()
        logger.debug("User saved!")

    def activate(self, nup):
        self.toggle_activate(nup, True)

    def deactivate(self, nup):
        self.toggle_activate(nup, False)


class TelegramNotificationHandler(NotificationHandler):

    telegram_bot = models.OneToOneField(TelegramBot, on_delete=models.CASCADE)

    def _handle_new_notification(self, file=None):
        logger.debug("New notification received, sending data to telegram subscribers...")

        tbot = self._get_telegram_bot()
        msg = "Motion detected!"
        file_id = None
        for s in self.subscribers.all():
            logger.info("Sending notification to %s", s)
            try:
                logger.debug("Sending telegram message...")
                tbot.sendMessage(chat_id=s.telegram_bot_id, text=msg)
                if file_id:
                    logger.debug("Sending telegram photo (existing server photo)...")
                    tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file_id)
                elif file:
                    logger.debug("Sending telegram photo (new photo)...")
                    tmsg = tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file)
                    file_id = tmsg.photo[0].file_id
            except TelegramError:
                logger.error("Message could not be sent to chat id: %s", s.telegram_bot_id)

    def __str__(self):
        return "%s [%s] | subscribers: %d" % (self.name, self.telegram_bot,
                                              self.subscribers.count())

    def _get_telegram_bot(self):
        return self.telegram_bot._get_telegram_bot()
