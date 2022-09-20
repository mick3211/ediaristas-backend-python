from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.foto_usuario_serializer import FotoUsuarioSerializer
from rest_framework import status
from ..services.usuario_service import listar_usuario_id


class FotoUsuairo(APIView):
    def post(self, request, format=None):
        usuario = listar_usuario_id(request.user.id)
        foto_serializer = FotoUsuarioSerializer(data=request.data)
        if foto_serializer.is_valid():
            foto = foto_serializer.validated_data['foto_usuario']
            usuario.foto_usuario = foto
            usuario.save()
            return Response('Foto alterada com sucesso', status.HTTP_200_OK)
        return Response(foto_serializer.errors, status.HTTP_400_BAD_REQUEST)