from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


class CreateUser(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class LoginUser(AuthenticationForm):

    def login(self, user):
        pass 
