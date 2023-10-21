from rest_framework import serializers

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.IntegerField()