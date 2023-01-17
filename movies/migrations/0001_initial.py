# Generated by Django 4.1.5 on 2023-01-17 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('score', models.DecimalField(decimal_places=1, max_digits=2)),
                ('description', models.TextField(blank=True)),
                ('review', models.TextField(blank=True)),
            ],
        ),
    ]
