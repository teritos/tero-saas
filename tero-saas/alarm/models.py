from django.db import models


class Alarm(models.Model):
    owner = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    members = models.ManyToManyField('customer.Customer', related_name='alarm_members')
    active = models.BooleanField(default=False)
    joined = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def __str__(self):
        return "{} {}".format(self.owner, self.active)

