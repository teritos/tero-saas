import logging

from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError

from notifications.models import NotificationUserProfile
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


class UnregisterdNotificationUserProfile(Exception):
    pass


class UnauthorizedUser(Exception):
    pass


class SCameraBotTelgramHandlers():
    """
    Commands - /setcommands BotFather message
    ping - check availability
    status - current notification status
    register - start to receive notifications
    subscribe - subscription on
    unsubscribe - subscription off
    activate - notifications on
    deactivate - notifications off
    """

    def __init__(self, telegrambot):
        logger.debug("Initializing telegram bot handlers...")
        self.telegrambot = telegrambot

    def _send_message(self, bot, update, msg):
        try:
            chat_id = update.message.chat_id
            logger.debug("chat_id: %s", chat_id)
            bot.sendMessage(chat_id=chat_id, text=msg)
        except TelegramError:
            logger.error("Error sending message! chat_id: %s")

    def _check_user_registered(self, update):
        logger.debug("Verifying user registered...")
        chat_id = update.message.chat_id
        try:
            nup = NotificationUserProfile.objects.get(telegram_bot_id=chat_id)
            logger.debug("User is registered!")
            return nup
        except NotificationUserProfile.DoesNotExist:
            logger.error("User is not registered!")
            raise UnregisterdNotificationUserProfile()

    def _handle_user_unregistered(self, bot, update):
        msg = "Sorry! You are not registered to operate this bot."
        self._send_message(bot, update, msg)

    def _handle_user_not_superuser(self, bot, update):
        msg = "Sorry! You don't have permission to use this command."
        self._send_message(bot, update, msg)

    def ping(self, bot, update):
        logger.info("Pinging...")
        try:
            self._check_user_registered(update)
            me = bot.getMe()
            logger.debug(me)
            msg = "botname: @%s\nid: %s" % (me['username'], me['id'])
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Ping OK!")

    def status(self, bot, update):
        logger.info("Checking status...")
        try:
            nup = self._check_user_registered(update)
            chat_id = update.message.chat_id
            username = update.message.chat.username
            logger.info("Checking subscription...")
            subscribed = 'on' if self.telegrambot.is_subscribed(nup) else 'off'
            logger.info("Checking activation...")
            active = 'on' if self.telegrambot.is_active() else 'off'
            msg = "username: %s\n" % username
            msg += "id: %s\n" % chat_id
            msg += "bot notifications: %s\n" % active
            msg += "user subscription: %s" % subscribed
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except:
            logger.exception()
        logger.info("Status check OK!")

    def subscribe(self, bot, update):
        logger.info("Enabling subscription...")
        try:
            nup = self._check_user_registered(update)
            self.telegrambot.subscribe(nup)
            msg = "Successfully subscribed!"
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Subscription enabled!")

    def unsubscribe(self, bot, update):
        logger.info("Disabling subscription...")
        try:
            nup = self._check_user_registered(update)
            self.telegrambot.unsubscribe(nup)
            msg = "Successfully unsubscribed!"
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except:
            logger.exception()
        logger.info("Subscription disabled!")

    def register(self, bot, update):
        msg = "Sorry! At this moment this option is unavailable."
        self._send_message(bot, update, msg)

    def activate(self, bot, update):
        try:
            logger.info("Activating notifications...")
            nup = self._check_user_registered(update)
            self.telegrambot.activate(nup)
            msg = "Notifications activated successfully!"
            self._send_message(bot, update, msg)
            logger.info("Notifications activated!")
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except PermissionDenied:
            self._handle_user_not_superuser(bot, update)
        except:
            logger.exception()

    def deactivate(self, bot, update):
        try:
            logger.info("Deactivating notifications...")
            nup = self._check_user_registered(update)
            self.telegrambot.deactivate(nup)
            msg = "Notifications deactivated successfully!"
            self._send_message(bot, update, msg)
            logger.info("Notifications deactivated!")
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except PermissionDenied:
            self._handle_user_not_superuser(bot, update)
        except:
            logger.exception()

    def _build_updater(self):
        logger.debug("Building telegram bot updater...")
        updater = Updater(self.telegrambot.token)
        updater.dispatcher.add_handler(CommandHandler('ping', self.ping))
        updater.dispatcher.add_handler(CommandHandler('status', self.status))
        updater.dispatcher.add_handler(CommandHandler('subscribe', self.subscribe))
        updater.dispatcher.add_handler(CommandHandler('unsubscribe', self.unsubscribe))
        updater.dispatcher.add_handler(CommandHandler('register', self.register))
        updater.dispatcher.add_handler(CommandHandler('activate', self.activate))
        updater.dispatcher.add_handler(CommandHandler('deactivate', self.deactivate))
        return updater


def get_telegram_updater(telegrambot):
    handlers = SCameraBotTelgramHandlers(telegrambot)
    return handlers._build_updater()
