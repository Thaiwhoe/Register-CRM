from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Lead(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    NEW = 'new'
    CONTACTED = 'contacted'
    CONVERTED = 'converted'
    LOST = 'lost'

    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (CONVERTED, 'Converted'),
        (LOST, 'Lost'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(
        max_length=10, choices=CHOICES_STATUS, default=NEW)
    converted = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, related_name='lead', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name