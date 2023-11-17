from rest_framework import serializers
from .models import User, Parent, Age, StudentClass


class AgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Age
        fields = ['id', 'name']


class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ['id', 'name']


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'image', 'first_name', 'last_name', 'phone']

    id = serializers.IntegerField(source='children.id')
    image = serializers.CharField(source='children.get_image')
    first_name = serializers.CharField(source='children.first_name')
    last_name = serializers.CharField(source='children.last_name')
    phone = serializers.CharField(source='children.phone')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'image', 'get_image', 'age', 'student_class']

    get_image = serializers.CharField(read_only=True)
