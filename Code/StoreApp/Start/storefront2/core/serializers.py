from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer , UserSerializer as BaseUserSerilaizer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['id','username','email','password','first_name','last_name']

class UserSerializer(BaseUserSerilaizer):
    class Meta(BaseUserSerilaizer.Meta):
        fields = ['id','first_name','last_name','email','username']
