from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..permissions.cliente_permission import ClientePermission
from ..services.diaria_service import listar_diaria_id, confirmar_presenca_diarista


class ConfirmarPresencaDiaristaId(APIView):
    permission_classes = [ClientePermission]

    def patch(self, request, diaria_id, format=None):
        confirmar_presenca_diarista(diaria_id)
        diaria = listar_diaria_id(diaria_id)
        self.check_object_permissions(self.request, diaria)

        return Response('Presença confirmada com sucesso', status.HTTP_200_OK)