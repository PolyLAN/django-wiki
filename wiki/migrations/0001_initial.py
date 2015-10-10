# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(help_text='Article properties last modified', verbose_name='modified', auto_now=True)),
                ('group_read', models.BooleanField(default=True, verbose_name='group read access')),
                ('group_write', models.BooleanField(default=True, verbose_name='group write access')),
                ('other_read', models.BooleanField(default=True, verbose_name='others read access')),
                ('other_write', models.BooleanField(default=True, verbose_name='others write access')),
            ],
            options={
                'permissions': (('moderate', 'Can edit all articles and lock/unlock/restore'), ('assign', 'Can change ownership of any article'), ('grant', 'Can assign permissions to other users')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleForObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='object ID')),
                ('is_mptt', models.BooleanField(default=False, editable=False)),
                ('article', models.ForeignKey(to='wiki.Article')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_articleforobject', verbose_name='content type', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Article for object',
                'verbose_name_plural': 'Articles for object',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticlePlugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deleted', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleRevision',
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
                ('content', models.TextField(verbose_name='article contents', blank=True)),
                ('title', models.CharField(help_text='Each revision contains a title field that must be filled out, even if the title has not changed', max_length=512, verbose_name='article title')),
                ('article', models.ForeignKey(verbose_name='article', to='wiki.Article')),
                ('previous_revision', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wiki.ArticleRevision', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'get_latest_by': 'revision_number',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReusablePlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ArticlePlugin')),
                ('articles', models.ManyToManyField(related_name='shared_plugins_set', to='wiki.Article')),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='RevisionPlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ArticlePlugin')),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='RevisionPluginRevision',
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
                ('plugin', models.ForeignKey(related_name='revision_set', to='wiki.RevisionPlugin')),
                ('previous_revision', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wiki.RevisionPluginRevision', null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-created',),
                'get_latest_by': 'revision_number',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePlugin',
            fields=[
                ('articleplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ArticlePlugin')),
                ('article_revision', models.ForeignKey(to='wiki.ArticleRevision')),
            ],
            options={
            },
            bases=('wiki.articleplugin',),
        ),
        migrations.CreateModel(
            name='URLPath',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(null=True, verbose_name='slug', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('article', models.ForeignKey(editable=False, to='wiki.Article', verbose_name='Cache lookup value for articles')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='wiki.URLPath', null=True)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'verbose_name': 'URL path',
                'verbose_name_plural': 'URL paths',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='urlpath',
            unique_together=set([('site', 'parent', 'slug')]),
        ),
        migrations.AddField(
            model_name='revisionplugin',
            name='current_revision',
            field=models.OneToOneField(related_name='plugin_set', null=True, to='wiki.RevisionPluginRevision', blank=True, help_text='The revision being displayed for this plugin. If you need to do a roll-back, simply change the value of this field.', verbose_name='current revision'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articlerevision',
            unique_together=set([('article', 'revision_number')]),
        ),
        migrations.AddField(
            model_name='articleplugin',
            name='article',
            field=models.ForeignKey(verbose_name='article', to='wiki.Article'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articleforobject',
            unique_together=set([('content_type', 'object_id')]),
        ),
        migrations.AddField(
            model_name='article',
            name='current_revision',
            field=models.OneToOneField(related_name='current_set', null=True, to='wiki.ArticleRevision', blank=True, help_text='The revision being displayed for this article. If you need to do a roll-back, simply change the value of this field.', verbose_name='current revision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='auth.Group', help_text='Like in a UNIX file system, permissions can be given to a user according to group membership. Groups are handled through the Django auth system.', null=True, verbose_name='group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(related_name='owned_articles', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, help_text='The owner of the article, usually the creator. The owner always has both read and write access.', null=True, verbose_name='owner'),
            preserve_default=True,
        ),
    ]
