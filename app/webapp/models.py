from django.db import models
import telegram


class TelegramProfile(models.Model):
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_lenght=255)

    @property
    def bot(self):
        """Return a telegram bot instance."""
        return telegram.Bot(token=self.bot_token)

    def send_message(self, message):
        self.bot.sendMessage(chat_id=id_, text='Movimiento detectado en casa! Archivo incompleto')
        
    def send_photo(self, path):
        self.bot.sendPhoto(id_, photo=open(path, 'rb'))

    def __str__(self):
        return "{}".format(self.bot_id)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram = models.OneToOneField(
        TelegramProfile,
        null=True,
        blank=True, 
        on_delete=models.CASCADE
        )