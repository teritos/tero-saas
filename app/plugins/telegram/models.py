from django.db import models


class Profile(models.Model):
    """A telegram profile"""
    # Provided by Telegram BotFather
    token = models.CharField(max_length=255)

    # User id
    user_id = models.CharField(max_length=255)
    # name = models.CharField(max_length=255)

    @property
    def bot(self):
        """Return a telegram bot instance."""
        return telegram.Bot(token=self.token)

    def send_message(self, message):
        self.bot.sendMessage(chat_id=self.user_id, text=message)

    def send_photo(self, path):
        self.bot.sendPhoto(chat_id=self.user_id, photo=open(path, 'rb'))

    def __str__(self):
        return "{}".format(self.user_id)
