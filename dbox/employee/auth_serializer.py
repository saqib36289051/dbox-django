from rest_framework import serializers
import re

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(
        min_length=11,
        max_length=11,
        validators=[
            serializers.RegexField(
                regex=r'^\d{11}$',
                error_messages={'invalid': 'Phone number must be 11 digits'}
            )
        ]
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['user', 'admin'])