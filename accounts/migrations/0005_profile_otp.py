# Generated by Django 3.0.5 on 2020-05-16 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200424_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='otp',
            field=models.CharField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]
