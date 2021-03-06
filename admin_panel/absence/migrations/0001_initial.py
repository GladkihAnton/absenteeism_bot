# Generated by Django 4.0.2 on 2022-05-28 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL('CREATE SCHEMA IF NOT EXISTS "absence";'),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
                'db_table': '"absence"."office"',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
                'db_table': '"absence"."role"',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('telegram_user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256, verbose_name='Имя в телеграме')),
                ('active', models.BooleanField(default=False)),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='absence.office')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='absence.role')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': '"absence"."user"',
            },
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('message', models.CharField(max_length=256)),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='absence.telegramuser')),
            ],
            options={
                'verbose_name': 'Пропуск',
                'verbose_name_plural': 'Пропуски',
                'db_table': '"absence"."absence"',
            },
        ),
    ]
