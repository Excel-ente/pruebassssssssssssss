from django.contrib import admin
from django.db import models
from .models import factura
from .models import codigoFinanciero
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets


admin.site.site_header = "Gestion Pilar"
admin.site.site_title = "Gestion Pilar"


#controlo como se importa/exporta
class facturaResource(resources.ModelResource):
        autorizado_por = fields.Field(attribute='autorizado_por',  column_name='autorizado_por')
        autorizado_fecha = fields.Field(attribute='autorizado_fecha',  column_name='autorizado_fecha')
        emision = fields.Field(attribute='emision',  column_name='emision')
        alta = fields.Field(attribute='alta', column_name='alta')
        codigo = fields.Field(attribute='codigo', column_name='codigo', widget=widgets.ForeignKeyWidget(codigoFinanciero, 'CODIGO')) # Acceso al campo 'codigo' en codigoFinanciero
        nroFactura = fields.Field(attribute='nroFactura', column_name='nroFactura')
        proveedor = fields.Field(attribute='proveedor', column_name='proveedor')
        oc = fields.Field(attribute='oc', column_name='oc')
        total = fields.Field(attribute='total', column_name='total')
        ff = fields.Field(attribute='ff', column_name='ff')
        unidadEjecutora = fields.Field(attribute='unidadEjecutora', column_name='unidadEjecutora')
        objeto = fields.Field(attribute='objeto', column_name='objeto')
        fondoAfectado = fields.Field(attribute='fondoAfectado', column_name='fondoAfectado')

        class Meta:
                model = factura


@admin.register(factura)
class facturaAdmin(ImportExportModelAdmin):
        resource_class = facturaResource
        list_display = ('nroFactura', 'proveedor', 'total',)
        list_filter = ('estado', 'codigo', 'nroFactura', 'proveedor',)
        exclude = ('estado',)
        
 