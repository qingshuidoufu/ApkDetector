# Generated by Django 4.0.2 on 2022-03-23 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apk', '0002_remove_apkinfo_scan_date_apkinfo_security_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='apkinfo',
            name='size',
            field=models.CharField(default=1, max_length=32, verbose_name='文件大小'),
            preserve_default=False,
        ),
    ]
