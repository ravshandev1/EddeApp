from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('verify-login/', views.VerifyPhoneAPI.as_view()),
    path('parent-login/', views.ParentLoginAPI.as_view()),
    path('children/', views.ParentAPI.as_view()),
    path('search/', views.SearchAPI.as_view()),
    path('request-to-jion/', views.RequestToJoinAPI.as_view()),
    path('verify-to-jion/', views.RequestToJoinVerifyAPI.as_view()),
    path('card-create/', views.CardCreate.as_view()),
    path('card-verify/', views.CardVerify.as_view()),
    path('student-apple-pay/', views.ApplePayStudent.as_view()),
    path('parent-apple-pay/', views.ApplePayParent.as_view()),
    path('student-pay/', views.ReceiptCreateStudent.as_view()),
    path('parent-pay/', views.ReceiptCreateParent.as_view()),
    path('ages/', views.AgeAPI.as_view()),
    path('classes/', views.ClassAPI.as_view()),
    path('payment/', views.PaymentAPI.as_view()),
]
