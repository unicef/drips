# Generated by Django 4.0.6 on 2022-07-08 00:41

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('report_metadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutocompleteMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('category', models.CharField(choices=[('bap', 'BAP Document No'), ('ip', 'IP No')], max_length=128, verbose_name='Category')),
                ('code', models.CharField(blank=True, max_length=128, null=True, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Autocomplete Metadata',
                'verbose_name_plural': 'Autocomplete Metadata',
            },
        ),
        migrations.CreateModel(
            name='BAPAutocompleteMetadata',
            fields=[
            ],
            options={
                'verbose_name': 'BAP Autocomplete Metadata',
                'verbose_name_plural': 'BAP Autocomplete Metadata',
                'abstract': False,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('report_metadata.autocompletemetadata',),
        ),
        migrations.CreateModel(
            name='IPAutocompleteMetadata',
            fields=[
            ],
            options={
                'verbose_name': 'IP Autocomplete Metadata',
                'verbose_name_plural': 'IP Autocomplete Metadata',
                'abstract': False,
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('report_metadata.autocompletemetadata',),
        ),
    ]
