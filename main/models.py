from django.db import models

# Create your models here.
class Member(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 200)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return self.fname + ' ' + self.lname
