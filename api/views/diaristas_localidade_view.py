from rest_framework.views import APIView
from api.services.cidades_atendimento_service import listar_diaristas_cidade
from ..serializers.diaristas_localidade_serializer import DiaristasLocalidadesSerializer
from ..paginations.diaristas_localidade_pagination import DiaristasLocalidadePagination

class DiaristasLocalidades(APIView, DiaristasLocalidadePagination):
    def get(self, request, format=None):
        cep = request.query_params.get('cep', None)
        diaristas = listar_diaristas_cidade(cep)
        resultado = self.paginate_queryset(diaristas, request)
        serializer_diaristas_localidade = DiaristasLocalidadesSerializer(resultado, many=True, context={"requet": request})
        return self.get_paginated_response(serializer_diaristas_localidade.data)