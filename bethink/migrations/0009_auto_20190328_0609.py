# Generated by Django 2.1.7 on 2019-03-28 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bethink', '0008_tgmessage_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tgmessage',
            name='notification_date',
            field=models.DateTimeField(null=True),
        ),
    ]
