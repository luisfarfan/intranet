from .models import *
from rest_framework import routers, serializers, viewsets


class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambiente


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local


class LocalAulasSerializer(serializers.ModelSerializer):
    ambientes = AmbienteSerializer(many=True, read_only=True)

    class Meta:
        model = Local


class LocalAmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalAmbiente


class PEA_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PEA


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso


class CriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criterio


class CursoCriterioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CursoCriterio


class TipoFuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario


class PEASerializer(serializers.ModelSerializer):
    id_cargofuncional = TipoFuncionarioSerializer()

    class Meta:
        model = PEA


class PEA_BY_AULASerializer(serializers.ModelSerializer):
    pea = PEASerializer(many=True, read_only=True)

    class Meta:
        model = LocalAmbiente


class PEA_ASISTENCIASerializer(serializers.ModelSerializer):
    class Meta:
        model = PEA_ASISTENCIA


class PEA_CURSOCRITERIOSerializer(serializers.ModelSerializer):
    class Meta:
        model = PEA_CURSOCRITERIO


class PEA_AULASerializer(serializers.ModelSerializer):
    peaaulas = PEA_ASISTENCIASerializer(many=True, read_only=True)
    id_pea = PEASerializer()

    class Meta:
        model = PEA_AULA
