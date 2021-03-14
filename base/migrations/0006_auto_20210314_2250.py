# Generated by Django 3.1.4 on 2021-03-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210314_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='razorpay_order_id',
        ),
        migrations.AlterField(
            model_name='timing',
            name='weekday',
            field=models.CharField(blank=True, choices=[('Thursday', 'Thursday'), ('Wednesday', 'Wednesday'), ('Monday', 'Monday'), ('Saturday', 'Saturday'), ('Tuesday', 'Tuesday'), ('Sunday', 'Sunday'), ('Friday', 'Friday')], max_length=100, null=True),
        ),
    ]
