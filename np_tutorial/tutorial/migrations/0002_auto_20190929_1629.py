# Generated by Django 2.1.7 on 2019-09-29 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='row',
            name='message',
            field=models.CharField(default='', max_length=50),
        ),
    ]
