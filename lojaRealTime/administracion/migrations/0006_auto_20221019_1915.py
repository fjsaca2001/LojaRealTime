# Generated by Django 3.2.4 on 2022-10-20 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0005_alter_vehiculos_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculos',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculos',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]