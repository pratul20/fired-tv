from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
)

from auth.helpers import send_otp_to_phone
from auth.models import User
from auth.serializer import PhoneSerializer, OTPSerializer

@api_view(['POST'])
def send_otp(request):
    data = request.data

    serializer = PhoneSerializer(data=data)
    if serializer.is_valid():
        user = User.objects.create(
            phone_number = serializer.validated_data('phone_number'),
            otp = send_otp_to_phone(serializer.validated_data('phone_number'))
        )
        user.set_password(serializer.validated_data('password'))
        user.save()
        return Response({
            'status': HTTP_200_OK,
            'message': 'OTP sent successfully',
        })
    else:
        return Response({
            'status': HTTP_400_BAD_REQUEST,
            'message': 'Phone Number and password is required'
        })


@api_view(['POST'])
def verify_otp(request):
    data = request.data
    serializer = OTPSerializer(data=data)
    if serializer.is_valid():
        try:
            user_obj = User.objects.get(phone_number=serializer.validated_data['phone_number'])
            if user_obj.otp == serializer.validated_data('otp'):
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({
                    'status': HTTP_200_OK,
                    'message': 'User verified'
                })
            else:
                return Response({
                    'status': HTTP_400_BAD_REQUEST,
                    'message': 'Invalid OTP'
                })

        except Exception as e:
            return Response({
                'status': HTTP_400_BAD_REQUEST,
                'message': f'Invlid phone number. {e}'
            })

    else:
        return Response({
            'status': HTTP_400_BAD_REQUEST,
            'message': 'Phone Number and otp is required'
        })



