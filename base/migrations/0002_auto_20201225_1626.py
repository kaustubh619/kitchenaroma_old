# Generated by Django 3.1.4 on 2020-12-25 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='kitchenratingsandreviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kitchengallery',
            name='kitchen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.kitchen'),
        ),
        migrations.AddField(
            model_name='category',
            name='kitchen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.kitchen'),
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.menuitem'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
