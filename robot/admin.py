from django.contrib import admin
from .models import TelegramUser, MenuButton, BotControl
from robot.utils.control import start_bot, stop_bot, BOT_IS_RUNNING

class BotControlAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'status']
    list_editable = ['is_active']

    def save_model(self, request, obj, form, change):
        """Botning holatini o'zgartirish."""
        if obj.is_active and not change:  # Yangi botni ishga tushirish
            if not BOT_IS_RUNNING:
                start_bot()  # Start the bot safely
                obj.status = "Running"
        elif not obj.is_active and change:  # Botni to'xtatish
            if BOT_IS_RUNNING:
                stop_bot()  # Stop the bot safely
                obj.status = "Stopped"
        super().save_model(request, obj, form, change)

admin.site.register(BotControl, BotControlAdmin)
@admin.register(MenuButton)
class MenuButtonAdmin(admin.ModelAdmin):
    list_display = ('title', 'callback_data')


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['full_name','username','user_id',]
    search_fields = ['full_name','username','user_id']

admin.site.register(TelegramUser, TelegramUserAdmin)
