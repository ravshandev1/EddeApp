from modeltranslation.translator import register, TranslationOptions
from .models import Subject, Level, Lesson
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline


class CustomAdmin(TranslationAdmin):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class InlineAdmin(TranslationStackedInline):
    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@register(Subject)
class SubjectTrans(TranslationOptions):
    fields = ['name']


@register(Level)
class LevelTrans(TranslationOptions):
    fields = ['name']


@register(Lesson)
class LessonTrans(TranslationOptions):
    fields = ['dialog_text', 'phrase_text', 'dialog_audio', 'phrase_audio']
