# Generated by Django 5.1.2 on 2024-11-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
