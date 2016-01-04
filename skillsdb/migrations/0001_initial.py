# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import skillsdb.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('entry_id', models.AutoField(serialize=False, primary_key=True)),
                ('candidate_fullname', models.CharField(max_length=100, blank=True)),
                ('file_name', models.CharField(max_length=100)),
                ('file1', models.FileField(upload_to=skillsdb.models.content_file_name)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SkillDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skills_name', models.CharField(max_length=100)),
                ('skill_count', models.IntegerField(max_length=100)),
                ('entry_id', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='skillsdb.Skill', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
