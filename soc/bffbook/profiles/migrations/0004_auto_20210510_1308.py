# Generated by Django 3.1.2 on 2021-05-10 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20210510_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='user.jpg', upload_to='avatars/'),
        ),
    ]
