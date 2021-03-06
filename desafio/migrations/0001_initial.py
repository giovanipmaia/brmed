# Generated by Django 3.2.9 on 2021-11-30 03:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Moeda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, verbose_name='Moeda')),
                ('abreviatura', models.CharField(max_length=3, verbose_name='Sigla')),
            ],
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now_add=True, verbose_name='Data da cotação')),
                ('valor', models.DecimalField(decimal_places=16, default=0, max_digits=21, verbose_name='Valor')),
                ('moeda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desafio.moeda')),
            ],
        ),
    ]
