# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-04 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NmCinema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[('荔湾区', '荔湾区'), ('黄埔区', '黄埔区'), ('天河区', '天河区'), ('白云区', '白云区'), ('越秀区', '越秀区'), ('海珠区', '海珠区'), ('从化区', '从化区'), ('番禺区', '番禺区'), ('花都区', '花都区'), ('萝岗区', '萝岗区'), ('南沙区', '南沙区'), ('增城区', '增城区')], max_length=32)),
                ('name', models.CharField(max_length=64)),
                ('nm_id', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'nmcinema',
            },
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(choices=[('糯米', '糯米'), ('时光', '时光')], max_length=8),
        ),
    ]
