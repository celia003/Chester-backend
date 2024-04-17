from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import User, Role, RoleUser


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField()


# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(read_only=True)
#     first_name = serializers.CharField(read_only=True)
#     last_name = serializers.CharField(read_only=True)
#     email = serializers.CharField(read_only=True)
#     is_active = serializers.BooleanField()
#     is_staff = serializers.BooleanField()
#     last_login = serializers.DateTimeField()
#     created = serializers.DateTimeField()
#     updated = serializers.DateTimeField()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'is_active']

    def to_representation(self, instance): 
        data = super().to_representation(instance)

        try:
            role_user = RoleUser.objects.get(user=instance)
            if role_user:
                role = Role.objects.get(id=role_user.role_id)
                data.update({'role_id': role_user.role_id})
                data.update({'role_name': role.name})
        except ObjectDoesNotExist:
            pass

        return data


class UsersListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    created = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    role_name = serializers.CharField(read_only=True)


class UserStatusSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(write_only=True, allow_null=False)

    class Meta:
        model = User
        fields = ['is_active']


class RoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        # fields = '__all__'
        fields = ['role']


# # class UsersSerializerCreate(serializers.ModelSerializer):
# #     # roleuser_role = RoleUserSerializer()
# #     role = RoleUserSerializer(read_only=True)
# #     # roleuser_user = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    

# #     class Meta:
# #         model = User
# #         fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'role']
# #         # fields = '__all__'

# #     # def create(self, validated_data):
# #     #     import ipdb; ipdb.set_trace()
# #     #     nested_data = validated_data.pop('role_id')
# #     #     nested_serializer = RoleUserSerializer(data=nested_data)
# #     #     if nested_serializer.is_valid():
# #     #         nested_instance = nested_serializer.save()
# #     #     else:
# #     #         raise serializers.ValidationError(nested_serializer.errors)

# #     #     user = User.objects.create(**validated_data, nested_model=nested_instance)
# #     #     return user
        
class UsersSerializerCreate(serializers.ModelSerializer):
    # roleuser_user = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = User
        # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'roleuser_role']
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone']

    # def create(self, validated_data):
    #     role_data = validated_data.pop('role')
    #     role = Role.objects.create(**role_data)
    #     user = User.objects.create(role=role, **validated_data)
    #     return user
    
    # def update(self, instance, validated_data):
    #     import ipdb; ipdb.set_trace()
    #     role_data = validated_data.pop('roleuser_user')
    #     ru, created = RoleUser.objects.get_or_create(user = instance)
    #     # role = RoleUser.objects.create(**role_data)
    #     ru.user = instance
    #     ru.role = role_data
    #     instance.save()
    #     return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']




