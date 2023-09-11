from django.contrib.auth.models import User
from django.db import models


class Avatar(models.Model):
    """User avatar model"""

    default_path = 'users/avatars/default.png'

    src = models.ImageField(upload_to='users/avatars/')

    @property
    def alt(self) -> str:
        if self.src == self.default_path:
            return 'Default avatar'
        return f'{Profile.objects.filter(avatar=self).get().user.username} avatar'

    @classmethod
    def get_default_pk(cls) -> int:
        avatar, _ = cls.objects.get_or_create(src=cls.default_path)
        return avatar.pk

    def __str__(self) -> str:
        return self.alt


class Profile(models.Model):
    """User profile info model"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    fullName = models.CharField(
        max_length=128,
        verbose_name='Полное имя',
    )
    email = models.CharField(
        max_length=128,
        verbose_name='Электронная почта',
    )
    phone = models.PositiveIntegerField(
        blank=True,
        null=True,
        unique=True,
        verbose_name='Номер телефона',
    )
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=0,
        verbose_name='Баланс',
    )
    avatar = models.ForeignKey(
        Avatar,
        on_delete=models.SET_DEFAULT,
        related_name='profile',
        verbose_name='Аватар',
        default=Avatar.get_default_pk,
    )

    def __str__(self) -> str:
        return self.user.username
