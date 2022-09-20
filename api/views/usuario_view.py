from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.editar_usuario_permission import EditarUsuarioPermission
from ..serializers.editar_usuario_serializer import EditarUsuarioSerializer
from ..serializers import usuario_serializer
from rest_framework import status
from ..models import Usuario as UsuarioModel


class Usuario(APIView):
    permission_classes = [EditarUsuarioPermission]

    def post(self, request, format=None):
        serializer_usuario = usuario_serializer.UsuarioSerializer(data=request.data, context={"request": request})

        if serializer_usuario.is_valid():
            usuario_criado = serializer_usuario.save()
            serializer_usuario = usuario_serializer.UsuarioSerializer(usuario_criado)
            return Response(serializer_usuario.data, status.HTTP_200_OK)
        return Response(serializer_usuario.errors, status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        usuario_antigo = UsuarioModel.objects.get(id=request.user.id)
        serializer_usuario = EditarUsuarioSerializer(usuario_antigo, request.data, context={'request': request})
        if serializer_usuario.is_valid():
            serializer_usuario.save()
            return Response(serializer_usuario.data, status.HTTP_200_OK)
        return Response(serializer_usuario.errors, status.HTTP_400_BAD_REQUEST)