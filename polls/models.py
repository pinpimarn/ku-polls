import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Model for Question, including question text, publish date, and end date."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('End date', default=None, blank=True, null=True)

    def __str__(self):
        """Return the output as string for question object."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Check that question was published and display recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check that question is displayed on the index page."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check that question is allowing visitors for voting."""
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date < now
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Model for Choice, including question, choice_text, and votes."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the output as string for choice object."""
        return self.choice_text
