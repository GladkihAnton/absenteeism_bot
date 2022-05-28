from django.db import models


class TelegramUser(models.Model):
    telegram_user_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=256, verbose_name='Имя в телеграме')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=False)
    office = models.ForeignKey('Office', on_delete=models.SET_NULL, null=True, blank=False)

    active = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = '"absence"."user"'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Role(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        db_table = '"absence"."role"'
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class Office(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        db_table = '"absence"."office"'
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы'

    def __str__(self):
        return self.name


class Absence(models.Model):
    date = models.DateField(null=False)
    message = models.CharField(max_length=256, null=False, blank=False)

    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.PROTECT, db_index=True)

    class Meta:
        db_table = '"absence"."absence"'
        verbose_name = 'Пропуск'
        verbose_name_plural = 'Пропуски'
