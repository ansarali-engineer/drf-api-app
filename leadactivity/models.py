from django.db import models
from lead.models import Lead
from user.models import User


class LeadActivity(models.Model):
    lead = models.ForeignKey(
        Lead,
        related_name="activities",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name="lead_activities",
        on_delete=models.CASCADE
    )

    activity_type = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    activity_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject