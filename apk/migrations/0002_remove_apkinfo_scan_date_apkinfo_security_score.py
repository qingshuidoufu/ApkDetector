# Generated by Django 4.0.2 on 2022-03-23 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apkinfo',
            name='scan_date',
        ),
        migrations.AddField(
            model_name='apkinfo',
            name='security_score',
            field=models.CharField(default=1, max_length=8, verbose_name='安全得分'),
            preserve_default=False,
        ),
    ]