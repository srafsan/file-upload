from django.db import models


class ApplicationManager(models.Manager):
    def create_application_obj(self, **kwargs):
        return self.create(**kwargs)

