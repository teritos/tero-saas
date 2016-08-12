from telegram.ext import Updater, CommandHandler
from webapp.models import UserProfile
import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def main():

    def get_user_profile(chat_id):
        if UserProfile.objects.filter(telegram__chat_id=chat_id).exists():
            return UserProfile.objects.get(telegram__chat_id=chat_id)
        else:
            return None

    def start(bot, update):
        bot.sendMessage(update.message.chat_id, text='Hello World!')

    def hello(bot, update):
        bot.sendMessage(update.message.chat_id,
                        text='Hello {0}'.format(update.message.from_user.first_name))

    def activate(bot, update):
        """Activate alarm"""
        user_profile = get_user_profile(update.message.chat_id)
        if user_profile is None:
            logger.info('no user found with chat_id {}'.format(update.message.chat_id))
            return
        user_profile.alarm.activate()
        bot.sendMessage(update.message.chat_id, text='Alarma activada :)')

    def deactivate(bot, update):
        """Deactivate alarm"""
        user_profile = get_user_profile(update.message.chat_id)
        if user_profile is None:
            logger.info('no user found with chat_id {}'.format(update.message.chat_id))
            return
        user_profile.alarm.deactivate()
        bot.sendMessage(update.message.chat_id, text='Alarma desactivada :)')

    def status(bot, update):
        """Return alarm status"""
        user_profile = get_user_profile(update.message.chat_id)
        if user_profile is None:
            logger.info('no user found with chat_id {}'.format(update.message.chat_id))
            return
        status = user_profile.alarm.active
        msg_status = 'Alarma desactivada' if status is False else 'Alarma esta activa'
        bot.sendMessage(update.message.chat_id, text=msg_status)

    token = os.environ['KAIA_TOKEN']
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('status', status))
    updater.dispatcher.add_handler(CommandHandler('st', status))
    updater.dispatcher.add_handler(CommandHandler('activate', activate))
    updater.dispatcher.add_handler(CommandHandler('ac', activate))
    updater.dispatcher.add_handler(CommandHandler('de', deactivate))

    updater.start_polling()
    updater.idle()
