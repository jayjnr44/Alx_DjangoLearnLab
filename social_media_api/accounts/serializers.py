from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields= ['id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'password']
        extra_kwargs = {'password': {'write_only' : True}}
    
    #def create(self, validated_data):
    def create(self, validated_data):
        # Extract fields that can't be passed to create_user
        profile_picture = validated_data.pop('profile_picture', None)
        
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        
        # Set additional fields after user creation
        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        
        # create an auth token for the newly created user
        Token.objects.create(user=user)
        return user        # create an auth token for the newly created user
        #Token.objects.create(user=user)
        #return user
    
class LoginSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

        def validate(self, data):
            user = authenticate(username=data['username'], password=data['password'])
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            data['user'] = user
            return data

