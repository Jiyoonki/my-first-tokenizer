# Generated by Django 3.0.3 on 2020-07-15 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0004_auto_20200714_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywords',
            name='words_selected',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='keywords',
            name='keywords',
            field=models.TextField(null=True),
        ),
    ]
