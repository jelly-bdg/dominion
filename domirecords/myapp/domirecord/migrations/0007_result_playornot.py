# Generated by Django 2.1.5 on 2019-03-14 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domirecord', '0006_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='playornot',
            field=models.BooleanField(default=False),
        ),
    ]