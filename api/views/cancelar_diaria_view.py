from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..permissions.dono_permission import DonoPermission
from ..serializers.cancelar_diaria_serializer import CancelarDiariaSerializer
from ..services.diaria_service import listar_diaria_id, atualizar_status_diaria
from ..services.cancelar_diaria_service import cancelar_diaria


class CancelarDiariaID(APIView):
    permission_classes = [DonoPermission]
    
    def patch(self, req, diaria_id, format=None):
        serializer_cancelar_diaria = CancelarDiariaSerializer(data=req.data)
        diaria = listar_diaria_id(diaria_id)
        self.check_object_permissions(self.request, diaria)
        if serializer_cancelar_diaria.is_valid():
            cancelar_diaria(diaria_id, req.user.id)
            atualizar_status_diaria(diaria_id, 5)
            return Response('Diária cancelada com sucesso', status=status.HTTP_200_OK)
        return Response(serializer_cancelar_diaria.errors, status=status.HTTP_400_BAD_REQUEST)
