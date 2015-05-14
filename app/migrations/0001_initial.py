# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('metainfo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CodeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=32)),
                ('value', models.CharField(max_length=256)),
                ('code', models.ForeignKey(to='app.Code')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('start', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PeriodType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Spending',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('details', models.CharField(max_length=200, null=True, blank=True)),
                ('amount', models.CharField(max_length=200, null=True, blank=True)),
                ('date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpendingDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SpendingLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SpendingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='spending',
            name='description',
            field=models.ForeignKey(to='app.SpendingDescription', null=True),
        ),
        migrations.AddField(
            model_name='spending',
            name='location',
            field=models.ForeignKey(blank=True, to='app.SpendingLocation', null=True),
        ),
        migrations.AddField(
            model_name='spending',
            name='payment',
            field=models.ForeignKey(blank=True, to='app.PaymentType', null=True),
        ),
        migrations.AddField(
            model_name='spending',
            name='type',
            field=models.ForeignKey(blank=True, to='app.SpendingType', null=True),
        ),
        migrations.AddField(
            model_name='spending',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='period',
            name='type',
            field=models.ForeignKey(to='app.PeriodType'),
        ),
    ]
