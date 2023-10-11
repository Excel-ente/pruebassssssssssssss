from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import factura
from models import proyeccionGastos
from django.utils import timezone
from datetime import date, timedelta, datetime
from django.db.models.functions import ExtractMonth
import datetime
from django.db.models import Sum

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

@login_required(login_url='/login/')
def detalleFactura(request, factura_detalle_id):
    factura_detalle = factura.objects.get(pk=factura_detalle_id)

    if request.method == 'POST':

        #obtengo el id del que se apreto el boton para marcar como Autorizado
        factura_id = request.POST.get('factura_id')

        #cambio el estado
        if factura_id:
            factura_selec = factura.objects.get(pk=factura_id)
            factura_selec.estado = 'Autorizado'
            factura_selec.save()

        return redirect('facturas')


    context = {
        'factura' : factura_detalle
    }

    return render(request, 'factura_detalle.html', context)

@login_required(login_url='/login/')
def facturas(request):

    fecha_actual = datetime.datetime.now()
    mes_actual = meses[fecha_actual.month - 1]

    facturas = factura.objects.all()
    grupo = request.user.groups.first()

    facturas = facturas.filter(codigo__CODIGO = grupo, estado = 'Pendiente')

    if request.method == 'POST':
    
        #obtengo el id del que se apreto el boton para marcar como Autorizado
        factura_button_id = request.POST.get('factura_button_id')
        factura_detalle_id = request.POST.get('factura_detalle_id')

        #cambio el estado
        if factura_button_id:
            factura_selec = factura.objects.get(pk=factura_button_id)
            factura_selec.autorizado_por = request.user.username
            factura_selec.autorizado_fecha = timezone.now() - timezone.timedelta(hours=3)
            factura_selec.estado = 'Autorizado'
            factura_selec.save()

            return redirect('facturas')


        #cambio el estado si se apreto el boton de autorizar
        if 'autorizar_seleccionados' in request.POST:
            #obtengo lista de todos los que se hicieron check
            facturas_check_id = request.POST.getlist('facturas_check_id')

            for factura_check_id in facturas_check_id:
                factura_selec = factura.objects.get(pk=factura_check_id)
                factura_selec.autorizado_por = request.user.username
                factura_selec.autorizado_fecha = timezone.now() - timezone.timedelta(hours=3)
                factura_selec.estado = 'Autorizado'
                factura_selec.save()

            return redirect('facturas')

        #si se apreto el boton para ver el detalle
        if factura_detalle_id:
            return redirect('detalleFactura', factura_detalle_id = factura_detalle_id)
        
        return redirect('facturas')


    #Listado de proveedores y facturas sin repetidos
    proveedores = facturas.values_list('proveedor', flat=True).distinct()
    nroFacturas = facturas.values_list('nroFactura', flat=True).distinct()

    # Obtener los parámetros de los filtros (si están presentes)
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    proveedores_seleccionados = request.GET.getlist('proveedor')
    facturas_seleccionadas = request.GET.getlist('nroFactura')
    verFacturas = request.GET.get('verFacturas')

    if verFacturas:
        if verFacturas == "autorizadas":
            facturas = factura.objects.filter(codigo__CODIGO = grupo, estado = 'Autorizado')

        elif verFacturas == "todas":
            facturas = factura.objects.filter(codigo__CODIGO = grupo)

        else: 
            facturas = facturas.filter(codigo__CODIGO = grupo, estado = 'Pendiente')

    # Aplicar los filtros si están presentes
    if fecha_desde and fecha_hasta:
        # Convertir las fechas de texto a objetos datetime
        fecha_desde = datetime.datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta = datetime.datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        # Filtrar por rango de fechas
        facturas = facturas.filter(emision__range=(fecha_desde, fecha_hasta))

    if proveedores_seleccionados:
        #filtar por proveedores seleccionados
        facturas = facturas.filter(proveedor__in = proveedores_seleccionados)

    if facturas_seleccionadas:
        #filtrar por facturas
        facturas = facturas.filter(nroFactura__in = facturas_seleccionadas)
        
    cantidad_facturas_pendientes = facturas.count()

    #obtengo el dinero disponible del mes
    proyeccion = proyeccionGastos.objects.filter(CODIGO = grupo, MES = datetime.datetime.now().month, EJERCICIO = datetime.datetime.now().year)
    totalDisponible = proyeccion.aggregate(total=Sum('IMPORTE'))['total'] or 0

    #obtengo el dinero total de las facturas autorizadas del mes
    facturasAutorizadas = factura.objects.filter(codigo__CODIGO = grupo, estado = 'Autorizado', autorizado_fecha__month = ExtractMonth(timezone.now()))
    totalFacturasAutorizadas = facturasAutorizadas.aggregate(total=Sum('total'))['total'] or 0

    totalDisponible = round(totalDisponible - totalFacturasAutorizadas, 2)

    context = {
        'facturas' : facturas,
        'cantidad_facturas_pendientes' : cantidad_facturas_pendientes,
        'mes_actual' : mes_actual,
        'proveedores':proveedores,
        'nroFacturas' : nroFacturas,
        'totalDisponible': totalDisponible,
    }

    return render(request, 'facturas.html', context)