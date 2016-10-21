import logging
import importlib

from notifications.telegram.models import TelegramBot

logger = logging.getLogger(__name__)


class TelegramBotRunner():

    @staticmethod
    def run_telelgram_bot(botname):
        logger.debug("Loading telegram bot %s...", botname)
        try:
            logger.debug("Retrieving telegram bot model...")
            telegram_bot = TelegramBot.objects.get(name=botname)

            logger.debug("Loading telegram bot module...")
            telegram_bot_module_name = 'notifications.telegram.%s' % telegram_bot.module_name
            telegram_bot_module = importlib.import_module(telegram_bot_module_name)
            updater = telegram_bot_module.get_telegram_updater(telegram_bot)
            logger.debug("Running telegram bot...")
            updater.start_polling()
            logger.debug("Telegram bot %s running...", telegram_bot)
            updater.idle()
        except ImportError:
            logger.error("Telegram bot %s not implemented!", telegram_bot)
        except TelegramBot.DoesNotExist:
            logger.error("Telegram bot %s not registered!", botname)
        except:
            logger.exception("Error trying to run telegram bot %s!")
