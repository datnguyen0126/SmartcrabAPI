# Generated by Django 3.0.8 on 2020-11-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_data', '0009_laptop_train'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='seller',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
