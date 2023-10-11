from django.db import models


# CLASE FONDOS
class codigoFinanciero(models.Model):
    CODIGO = models.CharField(max_length=20,unique=True,null=False, blank=False)
    NOMBRE = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        NAME = str(self.CODIGO) + " - " + str(self.NOMBRE)
        return NAME
    
    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural ='Codigos financieros' 

class factura(models.Model):
    estado_choice = (
        ('Pendiente', 'Pendiente'),
        ('Autorizado', 'Autorizado'),
    )

    autorizado_por = models.CharField(max_length=255, blank=True, null=True)
    autorizado_fecha = models.DateTimeField(blank=True, null=True)
    emision = models.DateField(blank=True, null = True)
    alta = models.DateField(blank=True, null = True)
    codigo = models.ForeignKey(codigoFinanciero, on_delete=models.CASCADE, blank=True, null=True)
    nroFactura = models.CharField(max_length = 255, blank=True, null = True)
    proveedor = models.CharField(max_length = 255, blank=True, null = True)
    oc = models.CharField(max_length = 255, blank=True, null = True)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True, null = True )
    ff = models.CharField(max_length = 255, blank=True, null = True)
    unidadEjecutora = models.CharField(max_length = 255, blank=True, null = True)
    objeto = models.CharField(max_length = 255, blank=True, null = True)
    fondoAfectado = models.CharField(max_length = 255, blank=True, null = True)

    estado = models.CharField(max_length=20, choices=estado_choice, default='Pendiente')
    
