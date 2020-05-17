# Generated by Django 3.0.5 on 2020-04-24 06:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0004_auto_20200424_0026'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', models.TextField()),
                ('image', models.ImageField(default='default.jpg', upload_to='blogs')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
    ]