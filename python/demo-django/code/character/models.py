from django.db import models
from game.models import Game


class Character(models.Model):
    name = models.CharField(max_length=250)
    game = models.ManyToManyField(Game, related_name='characters')

    def __unicode__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)