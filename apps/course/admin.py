from django.contrib import admin
from .models import Subject, Lesson, Level, Dictionary, Wishlist, StudentSubject, StudentLesson
from .translations import CustomAdmin, InlineAdmin


class StudentLessonInline(admin.StackedInline):
    model = StudentLesson
    extra = 0


@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    inlines = [StudentLessonInline]
    list_display = ['user', 'subject']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject']


@admin.register(Level)
class LevelAdmin(CustomAdmin):
    list_display = ['id', 'name']


@admin.register(Dictionary)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'to_lang']


class LessonAdminInline(InlineAdmin):
    model = Lesson
    extra = 0


@admin.register(Subject)
class CourseVideoAdmin(CustomAdmin):
    inlines = [LessonAdminInline]
    list_display = ['id', 'name']
