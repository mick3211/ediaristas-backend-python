from rest_framework.response import Response
from rest_framework.views import APIView
from ..services.cidades_atendimento_service import buscar_cidade_cep
from ..serializers.endereco_cep_serializer import EnderecoCepSerializer
from rest_framework import status as status_http

class EnderecoCep(APIView):
    def get(self, request, format=None):
        cep = self.request.query_params.get('cep', None)
        endereco = buscar_cidade_cep(cep)
        serializer_endereco_cep = EnderecoCepSerializer(endereco)
        return Response(serializer_endereco_cep.data, status=status_http.HTTP_200_OK)