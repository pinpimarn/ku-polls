"""Create required question admin features."""
from django.contrib import admin
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    """Align the choices inline."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Set up for showing information on the admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information',
         {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
