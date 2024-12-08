from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TelegramUser(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name='full_name'
    )
    username = models.CharField(
        max_length=200,
        verbose_name='username'
    )
    user_id = models.BigIntegerField(
        unique=True,
        validators=[MinValueValidator(0)],
        verbose_name='user_id'
    )

    def __str__(self):
        return str(self.user_id)

    def get_user(self):
        try:
            return User.objects.get(telegramusers=self)
        except User.DoesNotExist:
            return None

    def set_user(self, user):
        self.user = user
        self.save()



class MenuButton(models.Model):
    title = models.CharField(max_length=255)
    callback_data = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class BotControl(models.Model):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return "Telegram Bot boshqaruvi"