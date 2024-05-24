from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20)
    password = serializers.CharField(
        write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", 'username', 'password', 'password2',
                  'first_name', 'last_name', 'email', 'phone_number']
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Invalid phone number")
        return value

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        if phone_number:
            user.phone_number = phone_number
        user.save()
        return user