from django.utils import timezone

from django.db import models

from quickstart.managers import ApplicationManager


class ApplicationData(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nid_front = models.CharField(max_length=100)
    nid_back = models.CharField(max_length=100)
    passport = models.CharField(max_length=100)
    signature = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = ApplicationManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Application Data'
        verbose_name_plural = 'Application Data'

class FileSystemData(models.Model):
    application = models.ForeignKey(ApplicationData, on_delete=models.CASCADE, related_name='file_system_data')
    filename = models.CharField(max_length=100)
    file = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = ApplicationManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'File System Data'
        verbose_name_plural = 'File System Data'

