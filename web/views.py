"""Dashboard views."""

import json

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.edit import FormView
from django.contrib.auth import (
    login,
    logout
)

from alarm.models import Alarm
from .forms import (
    CreateUser,
    LoginUser
)


class Register(FormView):
    """Register view."""
    template_name = 'register.html'
    form_class = CreateUser
    success_url = '/dash/login'

    def form_valid(self, form):
        user = form.save()
        Alarm.create(user.username, form.cleaned_data['password1'])
        return super(Register, self).form_valid(form)


class Login(View):
    """Login view."""
    def get(self, request):
        """Render login form."""
        return render(template_name='login.html',
                      request=request,
                      context={'form': LoginUser()})

    def post(self, request):
        """Create an user."""
        form = LoginUser(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(template_name='login.html',
                          request=request,
                          context={'form': LoginUser()})
        else:
            return render(template_name='login.html',
                          request=request,
                          context={'form': form})


class Logout(View):
    """Logout view."""
    def get(self, request):
        """Log out user."""
        logout(request)
        return render(template_name='login.html',
                      request=request,
                      context={'form': LoginUser()})


@csrf_exempt
def ajax_login(request):
    """Ajax Login."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf8'))
        form = LoginUser(data={
            'username': data.get('username'),
            'password': data.get('password')
        })
        if form.is_valid():
            user = form.get_user()
            return HttpResponse(json.dumps({
                'status': 'ok', 
                'message': 'Logeado',
                'alarms': {
                    a.label: {'status': a.active} 
                    for a in user.alarms.all()
                }
            }), content_type='application/json')

        return HttpResponse(json.dumps({
            'status': 'error', 
            'message': 'Error en autenticacion'
        }), status=401, content_type='application/json')

    return HttpResponse(content_type='application/json')
