from django.db import models

class file(models.Model):
    filename = models.CharField(max_length=100)
    file = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
