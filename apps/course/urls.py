from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubjectListAPI.as_view()),
    path('parent-subjects/', views.SubjectsAPI.as_view()),
    path('my-subjects/', views.StudentSubjectAPI.as_view()),
    path('my-child-subjects/', views.ParentSubjectAPI.as_view()),
    path('<int:pk>/', views.SubjectDetailAPI.as_view()),
    path('child-subject/<int:pk>/', views.ParentSubjectDetailAPI.as_view()),
    path('dialog-text/<int:pk>/', views.DialogTextAPI.as_view()),
    path('dialog-audio/<int:pk>/', views.DialogAudioAPI.as_view()),
    path('phrase-text/<int:pk>/', views.PhraseTextAPI.as_view()),
    path('phrase-audio/<int:pk>/', views.PhraseAudioAPI.as_view()),
    path('dictionary-text/<int:pk>/', views.DictionaryTextAPI.as_view()),
    path('dictionary-audio/<int:pk>/', views.DictionaryAudioAPI.as_view()),
    path('is-view/<int:pk>/', views.IsViewAPI.as_view()),
    path('levels/', views.LevelView.as_view()),
    path('wishlist/', views.WishlistView.as_view()),
]
