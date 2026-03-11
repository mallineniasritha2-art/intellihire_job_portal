from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    is_candidate = models.BooleanField(default=False)
    is_interviewer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, default="Unknown")
    salary = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Application(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )

    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"