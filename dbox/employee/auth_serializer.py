from rest_framework import serializers
from django.core.validators import RegexValidator
class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message={'invalid': 'Phone number must be 11 digits'}
            )
        ]
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['user', 'admin'])