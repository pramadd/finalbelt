# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-22 23:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('datefrom', models.DateTimeField()),
                ('dateto', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='belt.User')),
                ('users', models.ManyToManyField(related_name='userstrips', to='belt.User')),
            ],
        ),
        migrations.CreateModel(
            name='TravelManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]