# Generated by Django 2.1.7 on 2019-03-30 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_accepted_tos'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
    ]