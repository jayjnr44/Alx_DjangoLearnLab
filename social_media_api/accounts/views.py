from django.shortcuts import render
from rest_framework import generics, status,permissions,viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer,LoginSerializer
from .models import CustomUser,user
from rest_framework.decorators import action
from .serializers import UserSerializer

# Create your views here.
class RegisterView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user= user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})

class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['posts'])
    def follow(self, request, pk=None):
        '''follow another user'''
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.follow(user_to_follow)
        return Response({'detail': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['posts'])
    def unfollow(self, request, pk=None):
        '''unfollow another user'''
        user_to_unfollow = self.get_object()

        if user_to_unfollow == request.user:
            return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.unfollow(user_to_unfollow)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        ''' Get a list of followers for a user'''
        user = self.get_object()
        followers = user.followers.all()
        page = self.paginate_queryset(followers)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
        
    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        ''' Get a list of users that a user is following'''
        user = self.get_object()
        following = user.following.all()
        page = self.paginate_queryset(following)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)