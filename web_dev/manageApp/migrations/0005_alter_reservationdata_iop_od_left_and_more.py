# Generated by Django 5.1.1 on 2024-09-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageApp', '0004_rename_iop_od_right_reservationdata_iop_os_right_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationdata',
            name='IOP_OD_left',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservationdata',
            name='IOP_OS_right',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservationdata',
            name='position',
            field=models.CharField(max_length=15),
        ),
    ]
