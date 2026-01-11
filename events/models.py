from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    location = models.TextField(max_length=100)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True
    )

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    events = models.ManyToManyField("Event", related_name="Participants")

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()