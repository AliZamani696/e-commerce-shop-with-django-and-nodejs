from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # دسترسی به فیلدهای مدل CustomUser از طریق رابطه OneToOne
    email = serializers.ReadOnlyField(source='user.email')
    wallet_balance = serializers.ReadOnlyField(source='user.wallet_balance')
    date_joined = serializers.ReadOnlyField(source='user.date_joined')
    role = serializers.ReadOnlyField(source='user.role')

    class Meta:
        model = Profile
        fields = (
            'id',
            'email',
            'wallet_balance',
            'date_joined',
            'role',
            'bio',
            'avatar'
        )
