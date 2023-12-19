# Generated by Django 5.0 on 2023-12-19 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaZero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('classe', models.CharField(blank=True, choices=[('feriado', 'Feriado'), ('pontof', 'Ponto Facultativo'), ('libaracao', 'Libaracao')], max_length=10, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data', models.DateTimeField(blank=True, null=True)),
                ('horainicial', models.TimeField(blank=True, null=True)),
                ('horafinal', models.TimeField(blank=True, null=True)),
                ('all_day', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='IndispMilitar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, choices=[('ferias', 'Férias'), ('licenca', 'Licença'), ('dispensa', 'Dispensa'), ('outros', 'Outros')], max_length=10, null=True)),
                ('datainicial', models.DateTimeField(blank=True, null=True)),
                ('datafinal', models.DateTimeField(blank=True, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('militar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indisp_militar', to='cadastros.militar')),
            ],
        ),
    ]
