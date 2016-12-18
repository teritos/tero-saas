from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from django.views.generic.edit import FormView
from django.contrib.auth import (
    login,
    authenticate
)

from .forms import (
    CreateUser,
    LoginUser
)


class Register(FormView):
    template_name = 'register.html'
    form_class = CreateUser
    success_url = '/dash/login'

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)

class Login(View):

    def get(self, request):
        return render(template_name='login.html',
                      request=request,
                      context={'form': LoginUser()})

    def post(self, request):
        form = LoginUser(data=request.POST)
        import pdb;pdb.set_trace()
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponse('loggedin')
        else:
            return render(template_name='login.html',
                          request=request,
                          context={'form': form})
