from django.contrib import admin

from bot.models import TgUser


# Register your models here
@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'user')
    read_only_fields = ('chat_id', 'verification_code')
