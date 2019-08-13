from django.db import models

# Class to store the date, room number, name
class reservation(models.Model):
    date = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    roomNumber = models.CharField(max_length=500)
    bookedOn = models.DateTimeField(auto_now_add=True)