# Generated by Django 4.0.5 on 2022-07-03 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fourapp', '0002_post_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
