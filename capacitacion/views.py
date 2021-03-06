# -*- coding: utf-8 -*-
from django.db.models.sql.compiler import cursor_iter
from rest_framework.views import APIView
from django.db.models import Count, Value
from django.http import JsonResponse
from django.http import HttpResponse
from django.template import loader
from serializer import *
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Sum
from datetime import datetime
import pandas as pd
from django.db.models.functions import Concat
from django.core.exceptions import ObjectDoesNotExist

import json
from random import sample
from django.db.models import Q
from consecucion_traspaso.models import *

def modulo_registro(request):
    template = loader.get_template('capacitacion/modulo_registro.html')
    funcionarios = FuncionariosINEI.objects.values('id_per', 'ape_paterno', 'ape_materno',
                                                   'nombre', 'dni')
    context = {
        'titulo_padre': 'Capacitación /',
        'titulo_hijo': 'Módulo de registro de local',
        'funcionarios': funcionarios,
    }
    return HttpResponse(template.render(context, request))


def cursos_evaluaciones(request):
    template = loader.get_template('capacitacion/cursos_evaluaciones.html')

    context = {
        'titulo_padre': 'Capacitación /',
        'titulo_hijo': 'Cursos y Evaluaciones',
    }
    return HttpResponse(template.render(context, request))


def asistencia(request):
    template = loader.get_template('capacitacion/asistencia.html')
    instructores = Instructor.objects.all()
    context = {
        'titulo_padre': 'Capacitación /',
        'titulo_hijo': 'Modulo de Asistencia',
        'instructores': instructores
    }
    return HttpResponse(template.render(context, request))


def distribucion(request):
    template = loader.get_template('capacitacion/distribucion.html')
    context = {
        'titulo_padre': 'Capacitación /',
        'titulo_hijo': 'Módulo de Distribución de PEA'
    }
    return HttpResponse(template.render(context, request))


def evaluacion(request):
    template = loader.get_template('capacitacion/evaluacion.html')

    context = {
        'titulo_padre': 'Capacitación /',
        'titulo_hijo': 'Módulo de registro de notas y resultado',
    }
    return HttpResponse(template.render(context, request))


# Create your views here.

class DepartamentosList(APIView):
    def get(self, request):
        departamentos = list(
            Ubigeo.objects.values('ccdd', 'departamento').annotate(dcount=Count('ccdd', 'departamento')))
        response = JsonResponse(departamentos, safe=False)
        return response


class ProvinciasList(APIView):
    def get(self, request, ccdd):
        provincias = list(
            Ubigeo.objects.filter(ccdd=ccdd).values('ccpp', 'provincia').annotate(dcount=Count('ccpp', 'provincia')))
        response = JsonResponse(provincias, safe=False)
        return response


class DistritosList(APIView):
    def get(self, request, ccdd, ccpp):
        distritos = list(Ubigeo.objects.filter(ccdd=ccdd, ccpp=ccpp).values('ccdi', 'distrito').annotate(
            dcount=Count('ccdi', 'distrito')))
        response = JsonResponse(distritos, safe=False)
        return response


class ZonasList(APIView):
    def get(self, request, ubigeo):
        zonas = list(
            Zona.objects.filter(UBIGEO=ubigeo).values('UBIGEO', 'ZONA', 'ETIQ_ZONA').annotate(
                dcount=Count('UBIGEO', 'ZONA')))
        response = JsonResponse(zonas, safe=False)
        return response


class TbLocalByUbigeoViewSet(generics.ListAPIView):
    serializer_class = LocalSerializer

    def get_queryset(self):
        ubigeo = self.kwargs['ubigeo']
        id_curso = self.kwargs['id_curso']
        return Local.objects.filter(ubigeo=ubigeo, id_curso=id_curso)


class TbLocalByMarcoViewSet(generics.ListAPIView):
    serializer_class = MarcoLocalSerializer

    def get_queryset(self):
        ubigeo = self.kwargs['ubigeo']
        # zona = self.kwargs['zona']
        return MarcoLocal.objects.filter(ubigeo=ubigeo)


class TbDirectorioLocalViewSet(generics.ListAPIView):
    serializer_class = DirectorioLocalSerializer

    def get_queryset(self):
        ubigeo = self.kwargs['ubigeo']
        return DirectorioLocal.objects.filter(ubigeo=ubigeo)


def getDirectoriolocal(request, ubigeo):
    query = DirectorioLocal.objects.filter(ubigeo=ubigeo).values('cantidad_disponible_auditorios',
                                                                 'cantidad_disponible_aulas',
                                                                 'cantidad_disponible_computo',
                                                                 'cantidad_disponible_oficina',
                                                                 'cantidad_disponible_otros',
                                                                 'cantidad_disponible_sala',
                                                                 'cantidad_total_auditorios', 'cantidad_total_aulas',
                                                                 'cantidad_total_computo', 'cantidad_total_oficina',
                                                                 'cantidad_total_otros', 'cantidad_total_sala',
                                                                 'cantidad_usar_auditorios', 'cantidad_usar_aulas',
                                                                 'cantidad_usar_computo', 'cantidad_usar_oficina',
                                                                 'cantidad_usar_otros', 'cantidad_usar_sala',
                                                                 'capacidad_local_total', 'capacidad_local_usar',
                                                                 'especifique_otros', 'fecha_fin', 'fecha_inicio',
                                                                 'funcionario_cargo', 'funcionario_celular',
                                                                 'funcionario_email', 'funcionario_nombre', 'id_curso',
                                                                 'id_curso_id', 'id_local', 'km_direccion', 'local',
                                                                 'lote_direccion', 'mz_direccion', 'n_direccion',
                                                                 'nombre_local', 'nombre_via', 'piso_direccion',
                                                                 'referencia', 'responsable_celular',
                                                                 'responsable_email', 'responsable_nombre',
                                                                 'responsable_telefono', 'telefono_local_celular',
                                                                 'telefono_local_fijo', 'tipo_via', 'turno_uso_local',
                                                                 'ubigeo', 'ubigeo_id', 'usuariolocal', 'zona',
                                                                 'zona_ubicacion_local', 'usuariolocal__id_usuario')
    return JsonResponse(list(query), safe=False)


class TbLocalByZonaViewSet(generics.ListAPIView):
    serializer_class = LocalSerializer

    def get_queryset(self):
        curso = self.kwargs['curso']
        ubigeo = self.kwargs['ubigeo']
        zona = self.kwargs['zona']
        return Local.objects.filter(ubigeo=ubigeo, curso_local__curso=curso, zona=zona)


# class TbLocalByZonaViewSet(generics.ListAPIView):
#     serializer_class = LocalAulasSerializer
#
#     def get_queryset(self):
#         ubigeo = self.kwargs['ubigeo']
#         zona = self.kwargs['zona']
#         return Local.objects.filter(ubigeo=ubigeo, zona=zona)


def TbLocalAmbienteByLocalViewSet(request, id_local, fecha=None):
    local = Local.objects.get(pk=id_local)
    query_response = []
    if fecha is not None:
        if fecha == 0:
            query = LocalAmbiente.objects.order_by('-capacidad').filter(id_local=id_local,
                                                                        pea_aula__pea_fecha=local.fecha_inicio).annotate(
                nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso', 'cant_pea').order_by(
                'id_ambiente')
            query_union = LocalAmbiente.objects.order_by('-capacidad').exclude(
                id_localambiente__in=LocalAmbiente.objects.order_by('-capacidad').filter(id_local=id_local,
                                                                                         pea_aula__pea_fecha=local.fecha_inicio).annotate(
                    nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                    'id_localambiente')).filter(id_local=id_local).annotate(
                nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso', 'cant_pea').order_by(
                'id_ambiente')
            query_response = query | query_union
        else:
            query = LocalAmbiente.objects.order_by('-capacidad').filter(id_local=id_local,
                                                                        pea_aula__pea_fecha=local.fecha_fin).annotate(
                nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso', 'cant_pea').order_by(
                'id_ambiente')
            query_union = LocalAmbiente.objects.order_by('-capacidad').exclude(
                id_localambiente__in=LocalAmbiente.objects.order_by('-capacidad').filter(id_local=id_local,
                                                                                         pea_aula__pea_fecha=local.fecha_fin).annotate(
                    nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                    'id_localambiente')).filter(id_local=id_local).annotate(
                nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
                'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso', 'cant_pea').order_by(
                'id_ambiente')
            query_response = query | query_union
    elif fecha is None:
        print 'hola'
        query_response = LocalAmbiente.objects.order_by('-capacidad').filter(id_local=id_local).annotate(
            nombre_ambiente=F('id_ambiente__nombre_ambiente'), cant_pea=Count('pea')).values(
            'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso', 'cant_pea').order_by(
            'id_ambiente')
    return JsonResponse(
        {'ambientes': list(query_response), 'ubigeo': local.ubigeo_id, 'zona': local.zona,
         'id_curso': local.id_curso_id},
        safe=False)


def Directorio_Local_Ambientes(request, id_local, is_directorio="1"):
    if is_directorio == "1":
        local = DirectorioLocal.objects.get(pk=id_local)
        ambientes = DirectorioLocalAmbiente
    else:
        local = Local.objects.get(pk=id_local)
        ambientes = LocalAmbiente

    query_response = ambientes.objects.order_by('-capacidad').filter(id_local=id_local).annotate(
        nombre_ambiente=F('id_ambiente__nombre_ambiente')).values(
        'id_localambiente', 'numero', 'capacidad', 'nombre_ambiente', 'n_piso').order_by(
        'id_ambiente')

    return JsonResponse(
        {'ambientes': list(query_response), 'ubigeo': local.ubigeo_id, 'zona': local.zona,
         'id_curso': local.id_curso_id},
        safe=False)


class LocalAmbienteByLocalAulaViewSet(generics.ListAPIView):
    serializer_class = LocalAmbienteSerializer

    def get_queryset(self):
        id_local = self.kwargs['id_local']
        id_ambiente = self.kwargs['id_ambiente']
        return LocalAmbiente.objects.filter(id_local=id_local, id_ambiente=id_ambiente)


class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambiente.objects.all()
    serializer_class = AmbienteSerializer


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer


class DirectorioLocalViewSet(viewsets.ModelViewSet):
    queryset = DirectorioLocal.objects.all()
    serializer_class = DirectorioLocalSerializer


class DirectorioLocalAmbienteViewSet(viewsets.ModelViewSet):
    queryset = DirectorioLocalAmbiente.objects.all()
    serializer_class = DirectorioLocalAmbienteSerializer


class CargosViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = CargoSerializer


class CursoLocalViewSet(viewsets.ModelViewSet):
    queryset = CursoLocal.objects.all()
    serializer_class = CursoLocalSerializer


class LocalAmbienteViewSet(viewsets.ModelViewSet):
    queryset = LocalAmbiente.objects.all()
    serializer_class = LocalAmbienteSerializer


class CursobyEtapaViewSet(generics.ListAPIView):
    serializer_class = CursoSerializer

    def get_queryset(self):
        id_etapa = self.kwargs['id_etapa']
        return Curso.objects.filter(id_etapa=id_etapa)


class CriteriosViewSet(viewsets.ModelViewSet):
    queryset = Criterio.objects.all()
    serializer_class = CriterioSerializer


class PeaNotaFinalViewSet(viewsets.ModelViewSet):
    queryset = PeaNotaFinal.objects.all()
    serializer_class = PeaNotaFinalSerializer


class CursoCriteriosViewSet(viewsets.ModelViewSet):
    queryset = CursoCriterio.objects.all()
    serializer_class = CursoCriterioSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class CursoCriteriobyCursoViewSet(generics.ListAPIView):
    serializer_class = CursoCriterioSerializer

    def get_queryset(self):
        id_curso = self.kwargs['id_curso']
        return CursoCriterio.objects.filter(id_curso=id_curso)


class PEA_BY_AULAViewSet(viewsets.ModelViewSet):
    queryset = LocalAmbiente.objects.all()
    serializer_class = PEA_BY_AULASerializer


class PEA_ASISTENCIAViewSet(viewsets.ModelViewSet):
    queryset = PEA_ASISTENCIA.objects.all()
    serializer_class = PEA_ASISTENCIASerializer


class PEAViewSet(viewsets.ModelViewSet):
    queryset = PEA.objects.all()
    serializer_class = PEA_Serializer


class PEA_AULAViewSet(generics.ListAPIView):
    serializer_class = PEA_AULASerializer

    def get_queryset(self):
        id_localambiente = self.kwargs['id_localambiente']
        return PEA_AULA.objects.filter(id_localambiente=id_localambiente).order_by('id_pea__ape_paterno')


class PEA_AULAbyLocalAmbienteViewSet(generics.ListAPIView):
    serializer_class = PEA_AULASerializer

    def get_queryset(self):
        id_localambiente = self.kwargs['id_localambiente']
        return PEA_AULA.objects.filter(id_localambiente=id_localambiente)


class PEA_CURSOCRITERIOViewSet(generics.ListAPIView):
    serializer_class = PEA_CURSOCRITERIOSerializer

    def get_queryset(self):
        id_peaaula = self.kwargs['id_peaaula']
        return PEA_CURSOCRITERIO.objects.filter(id_peaaula=id_peaaula)


@csrf_exempt
def sobrantes_zona(request):
    if request.method == "POST" and request.is_ajax():
        ubigeo = request.POST['ubigeo']
        zona = request.POST['zona']
        id_curso = request.POST['id_curso']
        contingencia = request.POST['contingencia']
        if id_curso == "1":
            sobrantes = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).annotate(
                cargo=F('id_cargofuncional__nombre_funcionario')).filter(
                dni__in=['25709168', '10172799', '08158910']).order_by('ape_paterno').values('dni', 'ape_paterno',
                                                                                             'ape_materno', 'nombre',
                                                                                             'cargo', 'id_pea')
        else:
            if id_curso == "13":
                sobrantes = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).annotate(
                    cargo=F('id_cargofuncional__nombre_funcionario')).filter(ubigeo=ubigeo,
                                                                             id_cargofuncional__cursofuncionario__id_curso_id=id_curso,
                                                                             contingencia=contingencia,
                                                                             baja_estado=0, is_grupo=1).order_by(
                    'ape_paterno').values('dni', 'ape_paterno', 'ape_materno', 'nombre',
                                          'cargo', 'id_pea')
            elif id_curso == "5":
                sobrantes = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).annotate(
                    cargo=F('id_cargofuncional__nombre_funcionario')).filter(ubigeo=ubigeo,
                                                                             id_cargofuncional__cursofuncionario__id_curso_id=id_curso,
                                                                             contingencia=contingencia,
                                                                             is_grupo=5,
                                                                             baja_estado=0).order_by(
                    'ape_paterno').values('dni', 'ape_paterno', 'ape_materno', 'nombre',
                                          'cargo', 'id_pea')
            else:
                sobrantes = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).annotate(
                    cargo=F('id_cargofuncional__nombre_funcionario')).filter(ubigeo=ubigeo,
                                                                             id_cargofuncional__cursofuncionario__id_curso_id=id_curso,
                                                                             contingencia=contingencia,
                                                                             is_grupo=6,
                                                                             baja_estado=0).order_by(
                    'ape_paterno').values('dni', 'ape_paterno', 'ape_materno', 'nombre',
                                          'cargo', 'id_pea')

        return JsonResponse(list(sobrantes), safe=False)

    return JsonResponse({'msg': False})


@csrf_exempt
def getMeta(request):
    if request.method == "POST" and request.is_ajax():
        id_curso = request.POST['id_curso']
        ubigeo = request.POST['ubigeo']
        zona = request.POST['zona']
        if id_curso == "13":
            meta = PEA.objects.filter(id_cargofuncional__cursofuncionario__id_curso=id_curso, ubigeo=ubigeo,
                                      contingencia=0, alta_estado=0, is_grupo=1).count()
            meta_reclutada = PEA.objects.filter(id_cargofuncional__cursofuncionario__id_curso=id_curso,
                                                ubigeo=ubigeo, is_grupo=1).count()
        else:
            meta = PEA.objects.filter(id_cargofuncional__cursofuncionario__id_curso=id_curso, ubigeo=ubigeo,
                                      contingencia=0, alta_estado=0, is_grupo=6).count()
            meta_reclutada = PEA.objects.filter(id_cargofuncional__cursofuncionario__id_curso=id_curso,
                                                is_grupo=6, ubigeo=ubigeo).count()

        capacidad_zona = LocalAmbiente.objects.filter(id_local__zona=zona, id_local__ubigeo=ubigeo,
                                                      id_local__id_curso=id_curso).aggregate(
            cantidad_zona=Sum('capacidad'))
        capacidad_distrito = LocalAmbiente.objects.filter(id_local__ubigeo=ubigeo,
                                                          id_local__id_curso=id_curso).aggregate(
            cantidad_distrito=Sum('capacidad'))
        total_ambientes_distrito_query = Local.objects.filter(id_curso=id_curso, ubigeo=ubigeo).values(
            'cantidad_usar_auditorios', 'cantidad_usar_aulas', 'cantidad_usar_computo', 'cantidad_usar_oficina',
            'cantidad_usar_otros', 'cantidad_usar_sala')

        total_ambientes_zona_query = Local.objects.filter(id_curso=id_curso, ubigeo=ubigeo).values(
            'cantidad_usar_auditorios', 'cantidad_usar_aulas', 'cantidad_usar_computo', 'cantidad_usar_oficina',
            'cantidad_usar_otros', 'cantidad_usar_sala')
        total_ambientes_zona = 0
        total_ambientes_distrito = 0
        for i in total_ambientes_zona_query:
            for v in i:
                if i[v] is not None:
                    total_ambientes_zona = total_ambientes_zona + int(i[v])

        for i in total_ambientes_distrito_query:
            for v in i:
                if i[v] is not None:
                    total_ambientes_distrito = total_ambientes_distrito + int(i[v])

        return JsonResponse(
            {'cant': meta, 'cant_reclutada': meta_reclutada, 'cantidad_zona': capacidad_zona['cantidad_zona'],
             'cantidad_distrito': capacidad_distrito['cantidad_distrito'],
             'total_ambientes_zona': total_ambientes_zona,
             'total_ambientes_distrito': total_ambientes_distrito}, safe=False)

    return JsonResponse({'msg': False})


@csrf_exempt
def asignar(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST
        ubigeo = data['ubigeo']
        zona = data['zona']
        curso = data['id_curso']
        cargos = list(CursoFuncionario.objects.filter(id_curso=curso).values_list('id_funcionario', flat=True))
        alta = None
        if 'alta' in data:
            alta = data['alta']

        if 'aulaambiente' in data:
            id_aulaambiente = data['aulaambiente']

        if curso == '7':
            return JsonResponse(distribucion_curso4(ubigeo, zona, curso, alta), safe=False)
        elif curso == '1':
            return JsonResponse(distribucion_curso1(), safe=False)
        else:
            if 'alta' in data:
                if curso == "5":
                    _pea_cantidad = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(
                        ubigeo=ubigeo, id_cargofuncional__in=cargos, contingencia=0, is_grupo=6, alta_estado=1).count()
                    pea_baja = PEA_AULA.objects.filter(id_localambiente__id_local__ubigeo=ubigeo,
                                                       # id_localambiente__id_local__zona=zona,
                                                       id_pea__is_grupo=5,
                                                       id_localambiente=id_aulaambiente,
                                                       id_pea__id_cargofuncional__in=cargos,
                                                       id_pea__baja_estado=1).values('id_localambiente_id', 'id_pea_id',
                                                                                     'pea_fecha')[:_pea_cantidad]
                else:
                    _pea_cantidad = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(
                        ubigeo=ubigeo, id_cargofuncional__in=cargos, contingencia=0, alta_estado=1).count()
                    pea_baja = PEA_AULA.objects.filter(id_localambiente__id_local__ubigeo=ubigeo,
                                                       # id_localambiente__id_local__zona=zona,
                                                       id_localambiente=id_aulaambiente,
                                                       id_pea__id_cargofuncional__in=cargos,
                                                       id_pea__baja_estado=1).values('id_localambiente_id', 'id_pea_id',
                                                                                     'pea_fecha')[:_pea_cantidad]

                for i in pea_baja:
                    if curso == "5":
                        _pea = list(
                            PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(ubigeo=ubigeo,
                                                                                                     # zona=zona,
                                                                                                     id_cargofuncional__in=cargos,
                                                                                                     is_grupo=5,
                                                                                                     contingencia=0,
                                                                                                     alta_estado=1).values_list(
                                'id_pea', flat=True))[:1]
                    else:
                        _pea = list(
                            PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(ubigeo=ubigeo,
                                                                                                     # zona=zona,
                                                                                                     id_cargofuncional__in=cargos,
                                                                                                     contingencia=0,
                                                                                                     alta_estado=1).values_list(
                                'id_pea', flat=True))[:1]
                    dar_alta = PEA_AULA(id_localambiente_id=i['id_localambiente_id'], pea_fecha=i['pea_fecha'],
                                        id_pea_id=_pea[0])
                    dar_alta.save()
            else:
                if 'zona' in data:
                    locales_zona = Local.objects.filter(ubigeo=ubigeo, id_curso=curso)
                else:
                    locales_zona = Local.objects.filter(ubigeo=ubigeo, id_curso=curso)

                for e in locales_zona:
                    aulas_by_local = LocalAmbiente.objects.filter(id_local=e.id_local).order_by('-capacidad')
                    for a in aulas_by_local:
                        disponibilidad = disponibilidad_aula(a.id_localambiente)
                        if disponibilidad > 0:
                            if 'alta' not in data:
                                if curso == "5":
                                    pea_ubicar = PEA.objects.exclude(
                                        id_pea__in=PEA_AULA.objects.values('id_pea')).filter(
                                        ubigeo=ubigeo, contingencia=0, baja_estado=0,
                                        id_cargofuncional__in=cargos,
                                        is_grupo=5).order_by(
                                        'ape_paterno', 'zona')[:a.capacidad]
                                else:
                                    pea_ubicar = PEA.objects.exclude(
                                        id_pea__in=PEA_AULA.objects.values('id_pea')).filter(
                                        ubigeo=ubigeo, contingencia=0, baja_estado=0,
                                        id_cargofuncional__in=cargos).order_by(
                                        'zona', 'ape_paterno')[:a.capacidad]
                            else:
                                pea_ubicar = PEA.objects.exclude(
                                    id_pea__in=PEA_AULA.objects.filter(id_pea__baja_estado=0).values('id_pea')).filter(
                                    alta_estado=1)[:disponibilidad]
                            for p in pea_ubicar:
                                pea = PEA.objects.get(pk=p.id_pea)
                                aula = LocalAmbiente.objects.get(pk=a.id_localambiente)
                                pea_aula = PEA_AULA(id_pea=pea, id_localambiente=aula)
                                pea_aula.save()

            return JsonResponse({'msg': curso == "13"}, safe=False)

    return JsonResponse({'msg': False})


"""
EMPADRONADOR URBANO : 901
EMPADRONADOR RURAL : 284
JEFE DE SECCION URBANO : 165
JEFE DE SECCION RURAL : 3
"""


def distribucion_curso4(ubigeo, zona, curso, alta=None):
    locales = Local.objects.filter(ubigeo=ubigeo, zona=zona, id_curso=curso)
    cargos = list(CursoFuncionario.objects.filter(id_curso=curso).values_list('id_funcionario', flat=True))
    pea_distribuida = []
    pea = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(ubigeo=ubigeo, zona=zona,
                                                                                   id_cargofuncional__in=cargos,
                                                                                   contingencia=0,
                                                                                   baja_estado=0).values_list('id_pea',
                                                                                                              flat=True).order_by(
        'ape_paterno')

    if alta is not None:
        pea_baja = PEA_AULA.objects.filter(id_localambiente__id_local__ubigeo=ubigeo,
                                           id_localambiente__id_local__zona=zona,
                                           id_pea__id_cargofuncional__in=cargos,
                                           id_pea__baja_estado=1).values('id_localambiente_id', 'id_pea_id',
                                                                         'pea_fecha')

        for i in pea_baja:
            _pea = list(
                PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(ubigeo=ubigeo, zona=zona,
                                                                                         id_cargofuncional__in=cargos,
                                                                                         contingencia=0,
                                                                                         alta_estado=1).values_list(
                    'id_pea', flat=True))[:1]
            dar_alta = PEA_AULA(id_localambiente_id=i['id_localambiente_id'], pea_fecha=i['pea_fecha'],
                                id_pea_id=_pea[0])
            dar_alta.save()
    else:
        pea_grupo1 = pea[0:pea.count() / 2]
        pea_grupo2 = pea[pea.count() / 2:pea.count()]
        pea_distribuida = [{'pea': list(pea_grupo1), 'dia': 1}, {'pea': list(pea_grupo2), 'dia': 2}]

        for p in pea_distribuida:
            for l in locales:
                for a in l.localambiente_set.all().order_by('-capacidad'):
                    disponibilidad = disponibilidad_aula(a.id_localambiente, True, p['dia'])
                    if disponibilidad > 0:
                        pea_ubicar = p['pea'][:disponibilidad]
                        p['pea'] = list(set(p['pea']) - set(pea_ubicar))
                        for pu in pea_ubicar:
                            if p['dia'] == 1:
                                ubicada = PEA_AULA(id_pea_id=pu, id_localambiente_id=a.id_localambiente,
                                                   pea_fecha=l.fecha_inicio)
                                ubicada.save()
                            else:
                                ubicada = PEA_AULA(id_pea_id=pu, id_localambiente_id=a.id_localambiente,
                                                   pea_fecha=l.fecha_fin)
                                ubicada.save()
    return pea_distribuida


def distribucion_curso1():
    personas = PEA.objects.exclude(id_pea__in=PEA_AULA.objects.values('id_pea')).filter(
        dni__in=['25709168', '10172799', '08158910']).values_list('id_pea', flat=True)
    locales = Local.objects.all().filter(id_curso=1)
    for i in locales:
        for l in i.localambiente_set.all():
            for p in personas:
                save = PEA_AULA(id_localambiente_id=l.id_localambiente, id_pea_id=p)
                save.save()
    return [{'msg': True}]


def distribucion_curso5(ubigeo, zona, curso):
    locales = Local.objects.filter(ubigeo=ubigeo, zona=zona, id_curso=curso)
    cargos = list(CursoFuncionario.objects.filter(id_curso=curso).values_list('id_funcionario', flat=True))
    pea_distribuida = []
    pea_distribuida_junta = {'pea_dia1': [], 'pea_dia2': [], 'pea_jefe_rural': []}
    pea_ok = list(PEA_AULA.objects.values_list('id_pea', flat=True))
    for i in cargos:
        pea_cantidad = PEA.objects.filter(ubigeo=ubigeo, zona=zona, id_cargofuncional=i, contingencia=0,
                                          baja_estado=0).count()
        pea_dia1_ids = list(
            PEA.objects.exclude(id_pea__in=pea_ok).filter(ubigeo=ubigeo, zona=zona, id_cargofuncional=i,
                                                          contingencia=0, baja_estado=0).values_list(
                'id_pea', flat=True))[:pea_cantidad / 2]
        pea_distribuida.append(
            {'id_cargofuncional': i,
             'pea_dia1': pea_dia1_ids,
             'pea_dia2': list(PEA.objects.exclude(id_pea__in=pea_dia1_ids).filter(
                 ubigeo=ubigeo, zona=zona, id_cargofuncional=i, contingencia=0, baja_estado=0).values_list(
                 'id_pea', flat=True))})

    for d in pea_distribuida:
        if d['id_cargofuncional'] != 3:
            pea_distribuida_junta['pea_dia1'] = pea_distribuida_junta['pea_dia1'] + d['pea_dia1']
            pea_distribuida_junta['pea_dia2'] = pea_distribuida_junta['pea_dia2'] + d['pea_dia2']

        else:
            pea_distribuida_junta['pea_dia1'] = pea_distribuida_junta['pea_dia1'] + d['pea_dia1'] + d['pea_dia2']
            pea_distribuida_junta['pea_jefe_rural'] = d['pea_dia1'] + d['pea_dia2']

    pea_a_distribuir = [{'pea': pea_distribuida_junta['pea_dia1'], 'dia': 1},
                        {'pea': pea_distribuida_junta['pea_dia2'], 'dia': 2},
                        {'pea': pea_distribuida_junta['pea_jefe_rural'], 'dia': 2, 'jefe_rural': 1}]

    for k in pea_a_distribuir:
        for i in locales:
            for a in i.localambiente_set.all():
                disponibilidad = disponibilidad_aula(a.id_localambiente, True, k['dia'])
                if disponibilidad > 0:
                    if 'jefe_rural' not in k:
                        pea_ubicar = k['pea'][:disponibilidad]
                        k['pea'] = list(set(k['pea']) - set(pea_ubicar))
                        for u in pea_ubicar:
                            if k['dia'] == 1:
                                fecha = i.fecha_inicio
                            else:
                                fecha = i.fecha_fin
                            pea = PEA_AULA(id_pea_id=u, id_localambiente_id=a.id_localambiente, pea_fecha=fecha)
                            pea.save()
                    else:
                        if int(a.capacidad) == disponibilidad:
                            pea_ubicar = k['pea'][:disponibilidad]
                            k['pea'] = list(set(k['pea']) - set(pea_ubicar))
                            for u in pea_ubicar:
                                if k['dia'] == 1:
                                    fecha = i.fecha_inicio
                                else:
                                    fecha = i.fecha_fin
                                pea = PEA_AULA(id_pea_id=u, id_localambiente_id=a.id_localambiente, pea_fecha=fecha)
                                pea.save()

    return pea_distribuida_junta


def disponibilidad_aula(aula, curso5=False, dia=1):
    aula = LocalAmbiente.objects.get(pk=aula)
    if dia == 1:
        fecha = aula.id_local.fecha_inicio
    else:
        fecha = aula.id_local.fecha_fin

    if curso5:
        cantidad_asignada = PEA_AULA.objects.filter(id_localambiente=aula, id_pea__baja_estado=0,
                                                    pea_fecha=fecha).count()
    else:
        cantidad_asignada = PEA_AULA.objects.filter(id_localambiente=aula, id_pea__baja_estado=0).count()

    if aula.capacidad == None:
        return 0
    return aula.capacidad - cantidad_asignada


"""
TURNO
0 = MANANA
1 = TARDE
2 = TODO EL DIA
"""


@csrf_exempt
def redistribuir_aula(request, id_localambiente):
    PEA_AULA.objects.filter(id_localambiente=id_localambiente).delete()

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def copy_directorio_to_seleccionado(request, id_directoriolocal, id_curso):
    curso_local = CursoLocal.objects.get(curso=id_curso, id_cursolocal=id_directoriolocal)
    directorio = DirectorioLocal.objects.get(pk=id_directoriolocal)
    localambientes = DirectorioLocalAmbiente.objects.filter(id_local=id_directoriolocal)
    print directorio
    local = Local(curso_local=curso_local, nombre_local=directorio.nombre_local, nombre_via=directorio.nombre_via,
                  zona_ubicacion_local=directorio.zona_ubicacion_local,
                  mz_direccion=directorio.mz_direccion, tipo_via=directorio.tipo_via, referencia=directorio.referencia,
                  n_direccion=directorio.n_direccion, km_direccion=directorio.km_direccion,
                  lote_direccion=directorio.lote_direccion, piso_direccion=directorio.piso_direccion,
                  telefono_local_fijo=directorio.telefono_local_fijo,
                  telefono_local_celular=directorio.telefono_local_celular,
                  funcionario_nombre=directorio.funcionario_nombre, funcionario_email=directorio.funcionario_email,
                  funcionario_cargo=directorio.funcionario_cargo, responsable_nombre=directorio.responsable_nombre,
                  responsable_email=directorio.responsable_email, responsable_telefono=directorio.responsable_telefono,
                  responsable_celular=directorio.responsable_celular, ubigeo_id=directorio.ubigeo_id,
                  fecha_inicio=directorio.fecha_inicio, fecha_fin=directorio.fecha_fin,
                  cantidad_total_aulas=directorio.cantidad_total_aulas,
                  cantidad_disponible_aulas=directorio.cantidad_disponible_aulas,
                  cantidad_usar_aulas=directorio.cantidad_usar_aulas,
                  cantidad_total_auditorios=directorio.cantidad_total_auditorios,
                  cantidad_disponible_auditorios=directorio.cantidad_disponible_auditorios,
                  cantidad_usar_auditorios=directorio.cantidad_usar_auditorios,
                  cantidad_total_sala=directorio.cantidad_total_sala,
                  cantidad_disponible_sala=directorio.cantidad_disponible_sala,
                  cantidad_usar_sala=directorio.cantidad_usar_sala,
                  cantidad_total_oficina=directorio.cantidad_total_oficina,
                  cantidad_disponible_oficina=directorio.cantidad_disponible_oficina,
                  cantidad_usar_oficina=directorio.cantidad_usar_oficina,
                  cantidad_total_otros=directorio.cantidad_total_otros,
                  cantidad_disponible_otros=directorio.cantidad_disponible_otros,
                  cantidad_usar_otros=directorio.cantidad_usar_otros,
                  especifique_otros=directorio.especifique_otros,
                  cantidad_total_computo=directorio.cantidad_total_computo,
                  cantidad_disponible_computo=directorio.cantidad_disponible_computo,
                  cantidad_usar_computo=directorio.cantidad_usar_computo,
                  zona=directorio.zona, id_curso=Curso.objects.get(pk=id_curso))
    local.save()
    for i in localambientes:
        ambientes = LocalAmbiente(id_local_id=local.id_local, id_ambiente_id=i.id_ambiente_id, capacidad=i.capacidad,
                                  n_piso=i.n_piso)
        ambientes.save()

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def delete_curso_local(request, id_local, curso):
    cursolocal = CursoLocal.objects.get(id_local=id_local, curso=curso)
    cursolocal.delete()
    return JsonResponse({'msg': True}, safe=False)


def getRangeDatesLocal(request, id_local):
    format_fechas = []
    local = Local.objects.filter(pk=id_local).values('fecha_inicio', 'fecha_fin', 'turno_uso_local')
    fecha_inicio = datetime.strptime(local[0]['fecha_inicio'], '%d/%m/%Y').strftime('%Y-%m-%d')
    fecha_fin = datetime.strptime(local[0]['fecha_fin'], '%d/%m/%Y').strftime('%Y-%m-%d')
    rango_fechas = pd.Series(pd.date_range(fecha_inicio, fecha_fin).format())
    for f in rango_fechas:
        format_fechas.append(datetime.strptime(f, '%Y-%m-%d').strftime('%d/%m/%Y'))

    return JsonResponse({'fechas': format_fechas, 'turno': local[0]['turno_uso_local']}, safe=False)


def getPeaAsistencia(request):
    id_localambiente = request.POST['id_localambiente']
    fecha = request.POST['fecha']
    pea = PEA_AULA.objects.filter(id_localambiente=id_localambiente).annotate(
        nombre_completo=Concat(
            'id_pea__ape_paterno', Value(' '), 'id_pea__ape_materno', Value(' '), 'id_pea__nombre'),
        cargo=F('id_pea__cargo')).values('nombre_completo', 'cargo', 'id_pea__pea_aula__pea_asistencia__turno_manana',
                                         'id_pea__pea_aula__pea_asistencia__turno_tarde')

    return JsonResponse(list(pea), safe=False)


class PEA_AULACurso5ViewSet(generics.ListAPIView):
    serializer_class = PEA_AULASerializer

    def get_queryset(self):
        id_localambiente = self.request.POST['id_localambiente']
        fecha = self.request.POST['fecha']
        return PEA_AULA.objects.filter(id_localambiente=id_localambiente, pea_fecha=fecha).order_by(
            'id_pea__ape_paterno')

    def post(self, request, *args, **kwargs):
        return super(PEA_AULACurso5ViewSet, self).get(request, *args, **kwargs)


@csrf_exempt
def save_asistencia(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)

        for i in data:
            try:
                pea = PEA_ASISTENCIA.objects.get(fecha=i['fecha'],
                                                 id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']))
            except ObjectDoesNotExist:
                pea = None

            if pea is None:
                pea_asistencia = PEA_ASISTENCIA(fecha=i['fecha'], turno_manana=i['turno_manana'],
                                                id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']))
                pea_asistencia.save()
            else:
                pea_asistencia = PEA_ASISTENCIA.objects.get(fecha=i['fecha'],
                                                            id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']))
                pea_asistencia.turno_manana = i['turno_manana']
                pea_asistencia.save()

    return JsonResponse({'msg': True})


def getCriteriosCurso(request, id_curso):
    criterios = list(
        CursoCriterio.objects.filter(id_curso=id_curso).annotate(
            criterio=F('id_criterio__nombre_criterio')).values('id_cursocriterio', 'criterio', 'ponderacion',
                                                               'id_criterio'))

    return JsonResponse(criterios, safe=False)


@csrf_exempt
def save_notas(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)

        for i in data:
            try:
                pea = PEA_CURSOCRITERIO.objects.get(
                    id_cursocriterio=CursoCriterio.objects.get(pk=i['id_cursocriterio']),
                    id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']))
            except ObjectDoesNotExist:
                pea = None

            if pea is None:
                pea_cursocriterio = PEA_CURSOCRITERIO(nota=i['nota'],
                                                      id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']),
                                                      id_cursocriterio=CursoCriterio.objects.get(
                                                          pk=i['id_cursocriterio']))
                pea_cursocriterio.save()
            else:
                pea_cursocriterio = PEA_CURSOCRITERIO.objects.get(id_cursocriterio=CursoCriterio.objects.get(
                    pk=i['id_cursocriterio']),
                    id_peaaula=PEA_AULA.objects.get(pk=i['id_peaaula']))
                pea_cursocriterio.nota = i['nota']
                pea_cursocriterio.save()

    return JsonResponse({'msg': True})


@csrf_exempt
def generar_ambientes(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST
        ambientes = {}
        for i in data:
            if data[i] == '':
                ambientes[i] = 0
            else:
                ambientes[i] = int(data[i])

        id_local = data['id_local']

        if data['directorio'] == "1":
            ambiente_local = DirectorioLocalAmbiente
            local = DirectorioLocal
        else:
            ambiente_local = LocalAmbiente
            local = Local

        object = {
            'cantidad_usar_aulas': [restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=1).count(),
                                           ambientes['cantidad_usar_aulas']), 1],
            'cantidad_usar_auditorios': [
                restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=2).count(),
                       ambientes['cantidad_usar_auditorios']), 2],
            'cantidad_usar_sala': [restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=3).count(),
                                          ambientes['cantidad_usar_sala']), 3],
            'cantidad_usar_oficina': [
                restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=4).count(),
                       ambientes['cantidad_usar_oficina']), 4],
            'cantidad_usar_computo': [
                restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=5).count(),
                       ambientes['cantidad_usar_computo']), 5],
            'cantidad_usar_otros': [restar(ambiente_local.objects.filter(id_local=id_local, id_ambiente=6).count(),
                                           ambientes['cantidad_usar_otros']), 6]
        }

        for i in object:
            if object[i][0] > 0:
                for a in range(object[i][0]):
                    localambiente = ambiente_local(id_local=local.objects.get(pk=id_local),
                                                   id_ambiente=Ambiente.objects.get(pk=object[i][1]))
                    localambiente.save()
            elif object[i][0] < 0:
                borrar = ambiente_local.objects.filter(id_local=local.objects.get(pk=id_local),
                                                       id_ambiente=Ambiente.objects.get(pk=object[i][1])). \
                             order_by('-id_localambiente')[:(-1 * object[i][0])]

                ambiente_local.objects.filter(pk__in=borrar).delete()

        return JsonResponse(list(object), safe=False)


@csrf_exempt
def get_funcionarioinei(request, id_per):
    funcionarios = list(FuncionariosINEI.objects.filter(id_per=id_per).values())

    return JsonResponse(funcionarios, safe=False)


@csrf_exempt
def update_peaaula(request, id_localambiente, id_instructor):
    PEA_AULA.objects.filter(id_localambiente=id_localambiente).update(id_instructor=id_instructor)

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def darBajaPea(request):
    id_pea = request.POST.getlist('id_peas[]')

    for i in id_pea:
        pea = PEA.objects.get(pk=i)
        pea.baja_estado = 1
        pea.save()

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def darAltaPea(request):
    id_pea = request.POST.getlist('id_peas[]')

    for i in id_pea:
        pea = PEA.objects.get(pk=i)
        pea.contingencia = 0
        pea.alta_estado = 1
        pea.save()

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def save_nota_final(request):
    if request.method == "POST" and request.is_ajax():
        data = json.loads(request.body)
        for i in data:
            try:
                pea = PeaNotaFinal.objects.get(id_pea=PEA.objects.get(pk=i['id_pea']),
                                               id_curso=Curso.objects.get(pk=i['id_curso']))
            except ObjectDoesNotExist:
                pea = None

            if pea is None:
                if float(i['nota_final']) >= 11:
                    aprobado = 1
                else:
                    aprobado = 0
                pea_nota_final = PeaNotaFinal(nota_final=i['nota_final'],
                                              id_pea=PEA.objects.get(pk=i['id_pea']),
                                              id_curso=Curso.objects.get(pk=i['id_curso']), aprobado=aprobado)
                pea_nota_final.save()
            else:
                if float(i['nota_final']) >= 11:
                    aprobado = 1
                else:
                    aprobado = 0
                pea.nota_final = i['nota_final']
                pea.aprobado = aprobado
                pea.save()

    return JsonResponse({'msg': True})


@csrf_exempt
def peaCurso6(request, ubigeo, grupo):
    pea_dia1 = PEA.objects.all().filter(id_cargofuncional__id_funcionario=901, is_grupo=grupo,
                                        ubigeo=ubigeo).values().order_by(
        'ape_paterno')
    pea_dia2 = PEA.objects.all().exclude(
        id_pea__in=PEA.objects.filter(id_cargofuncional__id_funcionario=901, ubigeo=ubigeo,
                                      asistio_dia=1).values_list('id_pea',
                                                                 flat=True)).filter(
        id_cargofuncional__id_funcionario=901, ubigeo=ubigeo, is_grupo=grupo).values().order_by(
        'ape_paterno')
    pea_dia3 = PEA.objects.all().exclude(
        id_pea__in=PEA.objects.filter(id_cargofuncional__id_funcionario=901, ubigeo=ubigeo,
                                      asistio_dia__in=[1, 2]).values_list('id_pea',
                                                                          flat=True)).filter(
        id_cargofuncional__id_funcionario=901, ubigeo=ubigeo, is_grupo=grupo).values().order_by(
        'ape_paterno')

    return JsonResponse({'pea_dia1': list(pea_dia1), 'pea_dia2': list(pea_dia2), 'pea_dia3': list(pea_dia3)})


@csrf_exempt
def saveAsistenciaCurso6(request):
    data = request.POST
    json_data = json.loads(data['json_data'])
    for i in json_data:
        pea = PEA.objects.get(pk=i['id'])

        if i['asistio'] == 1 or i['asistio'] == 2:
            pea.asistio_dia = i['asistio']
        else:
            pea.asistio_dia = None
        pea.save()

    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def saveAsistenciaCurso6Dia2(request):
    data = request.POST

    json_data = json.loads(data['json_data'])
    for i in json_data:
        pea = PEA.objects.get(pk=i['id'])
        if i['asistio'] == 2:
            pea.asistio_dia = 2
        else:
            pea.asistio_dia = None
        pea.save()
    return JsonResponse({'msg': True}, safe=False)


@csrf_exempt
def cerrarDia1Grupo6(request, ccdd, ccpp, ccdi):
    ubigeo = ccdd+ccpp+ccdi
    titulares=PEA.objects.filter(ubigeo = ubigeo,id_cargofuncional=901, is_grupo=6,asistio_dia__isnull=False)
    reserva = PEA.objects.filter(ubigeo = ubigeo,id_cargofuncional=901, is_grupo=6,asistio_dia__isnull=True)
    for i in titulares:
        ficha177 = Ficha177.objects.using('consecucion').get(id_per=i.id_per)        
        ficha177.sw_titu = 1
        ficha177.seleccionado = 1
        ficha177.capacita = 1
        ficha177.save()

    for i in reserva:
        ficha177 = Ficha177.objects.using('consecucion').get(id_per=i.id_per)        
        ficha177.sw_titu = 0
        ficha177.seleccionado = 1
        ficha177.capacita = 1
        ficha177.save()
    return JsonResponse({'msg': True})


@csrf_exempt
def save_aprobado_distrital(request):
    aprobados = request.POST.getlist('aprobados[]')
    desaprobados = request.POST.getlist('desaprobados[]')

    for i in aprobados:
        pea = PeaNotaFinal.objects.get(pk=i)
        pea.seleccionado = 1
        pea.save()

    return JsonResponse({'msg': True}, safe=False)


class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)


def restar(num, num2):
    return int(num2) - int(num)
