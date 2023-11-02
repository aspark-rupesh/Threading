from django.db import models

# Create your models here.

class RoomClock(models.Model):
    room_code = models.CharField(max_length=100)
    clock = models.IntegerField(default=0)
    is_on_hold = models.BooleanField(default=False)
    threshold = models.IntegerField(default=120)
