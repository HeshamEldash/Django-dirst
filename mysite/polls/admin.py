from django.contrib import admin
from .models import Question, Choice, User, CustomUser
# Register your models here.

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("blablaba", {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Fullname", {"fields": ["first_name","last_name"]}),
        ("Password", {"fields": ["password"]}),
        ("Email",{"fields":["email"]}),
        ("Activity", {"fields": ["questions", "choices" ]})
    ]


admin.site.register(Question, QuestionAdmin)
admin.site.register(CustomUser)
