# Generated by Django 3.0.8 on 2020-10-22 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_data', '0003_auto_20201022_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]