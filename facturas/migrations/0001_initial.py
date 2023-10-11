# Generated by Django 4.1.7 on 2023-10-11 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='codigoFinanciero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CODIGO', models.CharField(max_length=20, unique=True)),
                ('NOMBRE', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Codigo',
                'verbose_name_plural': 'Codigos financieros',
            },
        ),
        migrations.CreateModel(
            name='factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autorizado_por', models.CharField(blank=True, max_length=255, null=True)),
                ('autorizado_fecha', models.DateTimeField(blank=True, null=True)),
                ('emision', models.DateField(blank=True, null=True)),
                ('alta', models.DateField(blank=True, null=True)),
                ('nroFactura', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('oc', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15, null=True)),
                ('ff', models.CharField(blank=True, max_length=255, null=True)),
                ('unidadEjecutora', models.CharField(blank=True, max_length=255, null=True)),
                ('objeto', models.CharField(blank=True, max_length=255, null=True)),
                ('fondoAfectado', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Autorizado', 'Autorizado')], default='Pendiente', max_length=20)),
                ('codigo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='facturas.codigofinanciero')),
            ],
        ),
    ]
