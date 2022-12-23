# Generated by Django 4.1.4 on 2022-12-23 11:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0002_alter_borrow_unique_together_borrow_renewed_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='borrow',
            unique_together={('user', 'book')},
        ),
        migrations.RemoveField(
            model_name='borrow',
            name='renewed_at',
        ),
    ]
