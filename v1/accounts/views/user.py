from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from v1.accounts.models.profile import Profile
from v1.accounts.models.user import User
from v1.accounts.serializers.user import UserSerializer, UserSerializerCreate


# users
class UserView(APIView):

    @staticmethod
    def get(request):
        """
        List users
        """

        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        """
        Create user
        """

        serializer = UserSerializerCreate(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            Profile(sponsor=request.user, user=user).save()
            return Response(UserSerializer(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# users/{user_id}
class UserDetail(APIView):

    @staticmethod
    def get(request, user_id):
        """
        View individual user
        """

        user = get_object_or_404(User, pk=user_id)
        return Response(UserSerializer(user).data)
