from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if update_fields and 'updated_at' not in update_fields:
            if isinstance(update_fields, tuple):
                update_fields = list(update_fields)
            update_fields.append('updated_at')
        super().save(force_insert, force_update, using, update_fields)
