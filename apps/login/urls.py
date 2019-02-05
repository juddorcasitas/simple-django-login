from django.urls import path, re_path
from .views import create_user, account_activation
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from .serializer import UserLoginSerializer
urlpatterns = [
    path('create-user/', create_user),
    re_path('activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         account_activation, name='activate_account'),
    path('login/', ObtainJSONWebToken.as_view(serializer_class=UserLoginSerializer)),
    path('refresh/', refresh_jwt_token),
    path('verify/', verify_jwt_token),
]