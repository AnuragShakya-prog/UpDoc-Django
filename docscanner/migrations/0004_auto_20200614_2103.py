# Generated by Django 3.0.7 on 2020-06-14 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docscanner', '0003_auto_20200614_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentimage',
            name='document_outline',
            field=models.ImageField(upload_to='images/imgs/'),
        ),
        migrations.AlterField(
            model_name='documentimage',
            name='scanned_image',
            field=models.ImageField(upload_to='images/scannedimgs/'),
        ),
    ]
