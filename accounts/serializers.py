from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=True)
    medical_license = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ("full_name", "email", "password", "password2", "role", "medical_license")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match."})
        if attrs["role"] == "clinician" and not attrs.get("medical_license"):
            raise serializers.ValidationError({"medical_license": "Medical license is required for clinicians."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        role = validated_data.get("role")
        email = validated_data["email"]
        # Use email as username
        validated_data["username"] = email
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
