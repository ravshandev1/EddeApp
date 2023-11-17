from django.contrib import admin
from .models import User, StudentClass, Age, Parent, Payment, VerifyPhone


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone', 'first_name', 'last_name']


@admin.register(Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(VerifyPhone)
class VerifyPhoneAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'method']


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user', 'children']
