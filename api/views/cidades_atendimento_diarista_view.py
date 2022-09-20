from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.relacionar_cidade_diarista_serializer import RelacionarCidadeDiaristaSerializer
from ..serializers.cidades_atendmento_diarista_serializer import CidadesAtendimentoDiaristaSerializer
from ..services import usuario_service, cidades_atendimento_service
from ..permissions.diarista_permission import DiaristaPermission
from ..models import CidadesAtendimento


class CidadesAtendimentoDiaristaID(APIView):
    permission_classes = [DiaristaPermission]

    def put(self, req, format=None):
        serializer_cidade_atendimento = RelacionarCidadeDiaristaSerializer(data=req.data)
        usuario = usuario_service.listar_usuario_id(req.user.id)
        if serializer_cidade_atendimento.is_valid():
            cidades = serializer_cidade_atendimento["cidades"]
            cidades_atendimento_service.relacionar_cidade_diarista(usuario, cidades)
            return Response(serializer_cidade_atendimento.data, status=status.HTTP_201_CREATED)
        return Response(serializer_cidade_atendimento.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        cidades_atendimento = CidadesAtendimento.objects.filter(usuario=request.user.id)
        serializer = CidadesAtendimentoDiaristaSerializer(cidades_atendimento, many=True)
        return Response(serializer.data, status.HTTP_200_OK)