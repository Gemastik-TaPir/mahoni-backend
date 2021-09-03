from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'username',
            'password',
            'email',
            'last_login',
        ]

        read_only_fields = [
            'id',
            'date_joined', 
            'last_login',
            'is_staff',
        ]

        extra_kwargs = {
            'password': {
            'write_only': True
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(AccountSerializer, self).create(validated_data)

    def validate(self, data):
        # validate password
        password_str = data['password']
        password_is_valid = self.__validate_password(password_str)
        if not password_is_valid:
            raise serializers.ValidationError("password does not meet requirements")
        return data

  
    def __validate_password(self, password):
        valid_password = True
        minimum_password_length = 6

        # check minimum length
        if (len(password) < minimum_password_length):
            valid_password = False
        
        # check for digit
        if not any(char.isdigit() for char in password):
            valid_password = False
        
        return valid_password