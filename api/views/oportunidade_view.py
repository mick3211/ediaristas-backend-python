from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.oportunidade_serializer import OportunidadeSerializer
from ..permissions.diarista_permission import DiaristaPermission
from ..services.oportunidade_service import listar_oportunidades


class Oportunidade(APIView):
    permission_classes = [DiaristaPermission]

    def get(self, req, format=None):
        oportunidades = listar_oportunidades(req.user.id)
        serializer_oportunidade = OportunidadeSerializer(oportunidades, many=True, context={'request': req})

        return Response(serializer_oportunidade.data, status=status.HTTP_200_OK)