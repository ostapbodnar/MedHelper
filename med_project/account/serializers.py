from requests.models import Request
from django.db.models import fields
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Doctor, Profile, User, get_user_by_type
from assignment.serializers import SpecificationSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        return token


class RegisterSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        # validators=[validate_password],
        max_length=128,
        min_length=8)
    password2 = serializers.CharField(
        write_only=True,
        required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'user_type')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            user_type=validated_data['user_type'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializers for changing a user's password."""
    password = serializers.CharField(
        write_only=True, required=True,
        # validators=[validate_password]
        min_length=8, max_length=128)
    password2 = serializers.CharField(
        write_only=True, required=True)
    old_password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    number_of_requests = fields.IntegerField()

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class DocotorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    number_of_requests = fields.IntegerField()
    specification = SpecificationSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    number_of_requests = fields.IntegerField()

    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class DoctorUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    number_of_requests = fields.IntegerField()
    isAlreadyDoctorOfThisUser = fields.BooleanField()
    specification = SpecificationSerializer()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = None
        request = self.context.get("request", False)
        if request:
            user = request.user
        print(get_user_by_type(user), instance.patients.all())
        inList = get_user_by_type(user) in instance.patients.all()
        rep['isAlreadyDoctorOfThisUser'] = inList

        rep['isRequested'] = Request.objects.filter(
            sender=user, reciever=instance.user, type=2 if inList else 1).count() > 0

        return rep

    class Meta:
        model = Profile
        fields = ['user', "name", 'surname', 'sex',
                  'contact_number', 'specification']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'specification': {'read_only': True}
        }


class ProfileSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
        }


class DoctorSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'surname', 'contact_number', 'sex', 'specification']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'specification': {'required': False}
        }

    def is_valid(self, raise_exception):
        return super().is_valid(raise_exception=raise_exception)
