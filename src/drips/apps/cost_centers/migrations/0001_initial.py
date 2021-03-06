# Generated by Django 4.0.6 on 2022-07-08 00:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('unicef_realm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('code', models.CharField(max_length=10, verbose_name='Code')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('business_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='unicef_realm.businessarea')),
            ],
            options={
                'verbose_name': 'CostCentre',
                'verbose_name_plural': 'CostCentres',
            },
        ),
    ]
