from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, default="Staff")
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default="Active")

    def __str__(self):
        return self.name
