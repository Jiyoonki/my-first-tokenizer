# Generated by Django 3.0.3 on 2020-07-14 02:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('session_id', models.CharField(max_length=100)),
                ('session_index', models.IntegerField()),
                ('text', models.TextField()),
                ('words', models.TextField()),
                ('Keywords', models.TextField()),
            ],
        ),
    ]
