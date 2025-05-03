from rest_framework import serializers
# first_name,last_name,email,phone_number,user_type,password
class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(min_length=11, max_length=11)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['user', 'admin'])