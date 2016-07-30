from django.db import models
from django.contrib.auth.models import User
import telegram


class TelegramProfile(models.Model):
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255)

    @property
    def bot(self):
        """Return a telegram bot instance."""
        return telegram.Bot(token=self.bot_token)

    def send_message(self, message):
        self.bot.sendMessage(chat_id=id_, text='Movimiento detectado en casa! Archivo incompleto')
        
    def send_photo(self, path):
        self.bot.sendPhoto(id_, photo=open(path, 'rb'))

    def __str__(self):
        return "{}".format(self.chat_id)


class AlarmProfile(models.Model):
    active = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def activate(self):
        self.active = True
        self.save()
    
    def deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        return "{} - {}".format(self.id, self.active)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alarm = models.OneToOneField(AlarmProfile)
    telegram = models.OneToOneField(
        TelegramProfile,
        null=True,
        blank=True, 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        return "{}".format(self.user)