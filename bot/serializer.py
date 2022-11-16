from typing import Any

from rest_framework import serializers


from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)
    tg_id = serializers.SlugField(source='chat_id', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_id', 'verification_code', 'username', 'user_id')
        read_only_fields = ('tg_id', 'user_id', 'username')

        def validate(self, attrs: dict[str, Any]):
            verification_code = attrs.get('verification_code')
            tg_user =TgUser.objects.filter(verification_code='verification_code').first()
            if not tg_user:
                raise serializers.ValidationError('Invalid verification code')
            attrs['tg_user'] = tg_user
            return attrs


