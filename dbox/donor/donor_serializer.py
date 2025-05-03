from rest_framework import serializers

class DonorSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(
        min_length=11,
        max_length=11,
        validators=[
            serializers.RegexField(
                regex=r'^\d{11}$',
                error_messages={'invalid': 'Phone number must be 11 digits'}
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

