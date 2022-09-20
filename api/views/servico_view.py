from rest_framework.views import APIView
from rest_framework import status as status_http
from rest_framework.response import Response
from administracao.services import servico_service
from ..serializers.servico_serializer import ServicoSerializer

class Servico(APIView):
    def get(self, request, format=None):
        servicos = servico_service.listar_servicos()
        serializer_servico = ServicoSerializer(servicos, many=True)
        return Response(serializer_servico.data, status=status_http.HTTP_200_OK)
