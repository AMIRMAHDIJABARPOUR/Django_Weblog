from django.db import models
from django.urls import reverse


class Contact(models.Model):
    name = models.CharField(max_length=128)
    subject = models.CharField(max_length=256)
    email = models.EmailField()
    massage = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    email = models.EmailField()
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
