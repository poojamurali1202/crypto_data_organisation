from rest_framework import serializers
from .models import Organisation,CryptoPriceModel,AuthUser

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPriceModel
        fields = '__all__'

class CreateOrganisationSerializer(serializers.Serializer):
    name = serializers.CharField()

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ["username","password","first_name","last_name","email","org"]

    extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = AuthUser.objects.create_user(**validated_data)
        return user

class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    org_id = serializers.CharField()