from django.db import models


class Ticket(models.Model):
    first_name = models.CharField(max_length=128,
                                  verbose_name="First name")
    last_name = models.CharField(max_length=128,
                                  verbose_name="Last name")
