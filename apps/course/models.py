from django.db import models
from django.conf import settings
from user.models import User


class Level(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='subjects')

    def __str__(self):
        return self.name

    @property
    def general_price(self):
        lessons = self.lessons.all()
        return sum([i.price for i in lessons])

    @property
    def get_image(self):
        return f"{settings.SITE_URL}{self.image.url}"


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    count_lesson = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=300)
    level = models.ForeignKey(Level, models.CASCADE, related_name='lessons')
    price = models.PositiveIntegerField(default=100)
    dialog_audio = models.FileField(upload_to='lesson/dialog')
    dialog_text = models.TextField()
    phrase_audio = models.FileField(upload_to='lesson/phrase')
    phrase_text = models.TextField()
    dictionary_text = models.TextField()

    def __str__(self):
        return self.name

    @property
    def get_dialog_audio(self):
        return f"{settings.SITE_URL}{self.dialog_audio.url}"

    @property
    def get_phrase_audio(self):
        return f"{settings.SITE_URL}{self.phrase_audio.url}"


class Dictionary(models.Model):
    lesson = models.ForeignKey(Lesson, models.CASCADE, related_name='dictionaries')
    to_lang = models.CharField(max_length=250)
    audio = models.FileField(upload_to='lesson/dictionary')

    def __str__(self):
        return self.lesson.name

    @property
    def get_audio(self):
        return f"{settings.SITE_URL}{self.audio.url}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='wishlists')
    subject = models.ForeignKey(Subject, models.CASCADE, related_name='wishlists')

    def __str__(self):
        return self.user.phone


class StudentSubject(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='student_subjects')
    subject = models.ForeignKey(Subject, models.CASCADE, related_name='student_subjects')

    def __str__(self):
        return self.subject.name

    @property
    def percent(self):
        th = self.subject.lessons.count()
        isv = 0
        for i in self.student_lessons.all():
            if i.is_view:
                isv += 1
        if th == 0:
            th = 1
        return round((isv * 100) / th)


class StudentLesson(models.Model):
    subject = models.ForeignKey(StudentSubject, models.CASCADE, related_name='student_lessons')
    lesson = models.ForeignKey(Lesson, models.CASCADE, related_name='student_lessons')
    is_view = models.BooleanField(default=False)

    def __str__(self):
        return self.subject.subject.name
