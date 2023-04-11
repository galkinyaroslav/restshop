from djoser.views import UserViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.

User = get_user_model()


class SomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response('darow')


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        print(kwargs)

        kwargs['context'] = self.get_serializer_context()

        kwargs['data'] = {"uid": self.kwargs["uid"],
                          "token": self.kwargs["token"]}
        return serializer_class(*args, **kwargs)
