from rest_framework import serializers
from .models import Subject, Lesson, Level, Dictionary, Wishlist, StudentSubject


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['user', 'subject']


class DictionaryTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'text']

    text = serializers.CharField(source='lesson.dictionary_text')


class DictionaryAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['get_audio']


class DialogTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'dialog_text']


class DialogAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['get_dialog_audio']


class PhraseTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'phrase_text']


class PhraseAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['get_phrase_audio']


class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = ['id', 'name', 'image', 'percent', 'count_themes']

    image = serializers.CharField(source='subject.get_image')
    id = serializers.IntegerField(source='subject.id')
    name = serializers.CharField(source='subject.name')
    count_themes = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_count_themes(obj):
        return obj.subject.lessons.count()


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'get_image']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'count_lesson', 'name', 'level', 'price', 'dialog_text']

    level = serializers.CharField(source='level.name')


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
