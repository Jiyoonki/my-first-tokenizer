# Generated by Django 3.0.3 on 2020-07-14 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0002_keyword'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Keyword',
            new_name='Keywords',
        ),
    ]
