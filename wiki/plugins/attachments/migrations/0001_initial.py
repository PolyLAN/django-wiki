# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import wiki.plugins.attachments.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('reusableplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ReusablePlugin')),
                ('original_filename', models.CharField(max_length=256, null=True, verbose_name='original filename', blank=True)),
            ],
            options={
                'db_table': 'wiki_attachments_attachment',
                'verbose_name': 'attachment',
                'verbose_name_plural': 'attachments',
            },
            bases=('wiki.reusableplugin',),
        ),
        migrations.CreateModel(
            name='AttachmentRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision_number', models.IntegerField(verbose_name='revision number', editable=False)),
                ('user_message', models.TextField(blank=True)),
                ('automatic_log', models.TextField(editable=False, blank=True)),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('locked', models.BooleanField(default=False, verbose_name='locked')),
                ('file', models.FileField(upload_to=wiki.plugins.attachments.models.upload_path, max_length=255, verbose_name='file')),
                ('description', models.TextField(blank=True)),
                ('attachment', models.ForeignKey(to='wiki_attachments.Attachment')),
                ('previous_revision', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wiki_attachments.AttachmentRevision', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'db_table': 'wiki_attachments_attachmentrevision',
                'verbose_name': 'attachment revision',
                'verbose_name_plural': 'attachment revisions',
                'get_latest_by': 'revision_number',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='attachment',
            name='current_revision',
            field=models.OneToOneField(related_name='current_set', null=True, to='wiki_attachments.AttachmentRevision', blank=True, help_text='The revision of this attachment currently in use (on all articles using the attachment)', verbose_name='current revision'),
            preserve_default=True,
        ),
    ]
