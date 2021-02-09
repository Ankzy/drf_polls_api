from django.contrib import admin
from .models import Poll, Question, Option


class QuestionInline(admin.TabularInline):
    model = Question

class PollAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Poll, PollAdmin)


class OptionInline(admin.TabularInline):
    model = Option

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)