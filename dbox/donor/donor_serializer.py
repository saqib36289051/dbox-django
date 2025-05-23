from rest_framework import serializers
from django.core.validators import RegexValidator

class DonorSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        min_length=11,
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message={'invalid': 'Phone number must be 11 digits'}
            )
        ]
    )
    name = serializers.CharField()
    province = serializers.CharField()
    city = serializers.CharField()
    area = serializers.CharField()
    complete_address = serializers.CharField()
    gender = serializers.CharField()
    longitude = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    latitude = serializers.CharField(required=False, allow_blank=True, allow_null=True)

