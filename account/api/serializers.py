import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Profile, User
from organization.models import Organization

# from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    organization_id = serializers.ReadOnlyField()

    class Meta:
        model = User
        exclude = ["password", "user_permissions", "groups"]


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    organization = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "password", "organization"]

    def validate(self, attrs):

        # if not re.match(r"[^@]+@[^@]+\.[^@]+", attrs.get("email")):
        #     raise serializers.ValidationError({"email": "Invalid email provided."})
        if not re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{8,}", attrs.get("password")):
            raise serializers.ValidationError(
                {
                    "password": "Invalid password provided.",
                    "assist": "Password must be 8 char long with some case, number and special characters.",
                }
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(email=validated_data["email"])
        if org := Organization.objects.filter(name=validated_data["organization"]):
            user.organization = org.first()
        user.set_password(validated_data["password"])
        user.save()
        return user


class HindsiteUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
        ]

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["email"],
            validated_data["password"],
        )


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "user",
            "first_name",
            "last_name",
        ]


class HindsiteTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token


class HindsiteTokenObtainPairView(TokenObtainPairView):
    serializer_class = HindsiteTokenObtainPairSerializer
