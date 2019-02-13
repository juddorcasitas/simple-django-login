from django.utils.encoding import force_text
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework.status as status
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer
from .models import User
from .tokens import account_activation_token
import logging


logger = logging.getLogger(__name__)

# Create Profile & Email verification

# test route for server status
@api_view(['GET'])
@permission_classes([AllowAny])
def sample_json(request):

    res = {"status": "success",
           "message": "Looks like the server is up and running"}
    return Response(res, status=status.HTTP_200_OK)


class CreateUserAPIView(APIView):
    # Any new user can create a profile
    permission_classes(AllowAny,)

    def post(self, request):
        try:
            user = request.data
            serializer = UserSerializer(data=user)
        except(TypeError, ValueError, OverflowError):
            user = None
            serializer = None

        if user and serializer.is_valid(raise_exception=True):
            serializer.save()
            user_obj = User.objects.get_by_natural_key(serializer.data['username'])
            token = account_activation_token.make_token(user_obj)
            message = 'http://127.0.0.1:8000/user/activate_account/%s/%s' % (serializer.data['username'], token)
            send_mail('Registered user', message, settings.EMAIL_HOST_USER,
                      [serializer.data['email']], fail_silently=False)
            return Response("User Created Successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserAPIView(APIView):
    # Any user can verify from an email link
    permission_classes(AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = force_text(uidb64)
            user = User.objects.get_by_natural_key(uid)
        except(TypeError, ValueError, OverflowError):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.email_verified = True
            user.save()
            # Response("User has been verified successfully", status=status.HTTP_200_OK)
            return redirect("/")
        else:
            return Response("Failed to verify User", status=status.HTTP_400_BAD_REQUEST)


create_user = CreateUserAPIView.as_view()
account_activation = VerifyUserAPIView.as_view()
