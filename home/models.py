from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=125)
    desc = models.TextField()
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'Message from {self.name} - {self.email}'
