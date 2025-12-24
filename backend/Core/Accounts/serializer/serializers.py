from rest_framework import serializers
from ..models import CustomUser




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,max_length=250)
    password_confirm = serializers.CharField(write_only=True,max_length=250)

    class Meta:
        model = CustomUser
        fields = ("email","password","password_confirm","role")

    def validate(self,data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("passwords dont match")
        return data

    def create(self,validate_data):
        validate_data.pop("password_confirm")
        return CustomUser.objects.create_user(**validate_data)

