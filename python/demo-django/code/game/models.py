from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)