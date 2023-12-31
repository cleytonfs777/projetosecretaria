# Generated by Django 5.0 on 2023-12-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empenho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, choices=[('escala', 'Escala'), ('demanda', 'Demanda'), ('dsp', 'DSP')], max_length=10, null=True)),
                ('nome', models.CharField(max_length=100)),
                ('datahorainicial', models.DateTimeField(blank=True, null=True)),
                ('datahorafinal', models.DateTimeField(blank=True, null=True)),
                ('duracao_em_minutos_atipica', models.IntegerField(blank=True, null=True)),
                ('duracao_em_minutos_tipica', models.IntegerField(blank=True, null=True)),
                ('documentacao', models.CharField(blank=True, max_length=100, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Militar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=100, null=True)),
                ('nome', models.CharField(max_length=100)),
                ('postgrad', models.CharField(blank=True, choices=[('sd2cl', 'Sd 2ª Classe BM'), ('sd', 'Sd BM'), ('cb', 'Cb BM'), ('3sgt', '3º Sgt BM'), ('2sgt', '2º Sgt BM'), ('1sgt', '1º Sgt BM'), ('subten', 'Sub Ten BM'), ('2ten', '2º Ten BM'), ('1ten', '1º Ten BM'), ('cap', 'Cap BM'), ('maj', 'Maj BM'), ('tencel', 'Ten Cel BM'), ('cel', 'Cel BM')], max_length=10, null=True)),
                ('local', models.CharField(blank=True, choices=[('acf', 'ACF'), ('acf1', 'ACF-1'), ('acf2', 'ACF-2'), ('acf3', 'ACF-3'), ('sdts1', 'SDTS-1'), ('sdts2', 'SDTS-2'), ('sdts3', 'SDTS-3'), ('nts', 'NTS'), ('gol', 'GOL'), ('sdal', 'SDAL'), ('sdal1', 'SDAL-1'), ('sdal2', 'SDAL-2'), ('sdal3', 'SDAL-3'), ('sdal4', 'SDAL-4'), ('secretaria', 'Secretaria')], max_length=10, null=True)),
                ('qtd_empenhos', models.IntegerField(blank=True, null=True)),
                ('empenhos_minutos_atipica', models.IntegerField(blank=True, null=True)),
                ('empenhos_minutos_tipica', models.IntegerField(blank=True, null=True)),
                ('empenhos', models.ManyToManyField(related_name='militares', to='cadastros.empenho')),
            ],
        ),
    ]
