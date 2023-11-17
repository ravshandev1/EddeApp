from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.db import models
from django.conf import settings


class StudentClass(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise TypeError('Invalid phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        if not password:
            raise TypeError('password no')
        user = self.create_user(phone, password, **extra_fields)
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    image = models.ImageField(upload_to='users', null=True, blank=True)
    student_class = models.ForeignKey(StudentClass, models.SET_NULL, null=True, blank=True)
    age = models.ForeignKey(Age, models.SET_NULL, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone

    @property
    def get_image(self):
        if self.image:
            return f"{settings.SITE_URL}{self.image.url}"
        return None


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=5)

    def __str__(self):
        return self.phone


class Parent(models.Model):
    children = models.ForeignKey(User, models.CASCADE, limit_choices_to={'is_parent': 0}, related_name='parent')
    user = models.ForeignKey(User, models.CASCADE, limit_choices_to={'is_parent': 1}, related_name='parents')

    def __str__(self):
        return self.user.first_name


class ParentControl(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='parent_control')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.phone


class Payment(models.Model):
    method = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.method}"
