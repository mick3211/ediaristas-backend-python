from rest_framework.views import APIView
from ..serializers.usuario_serializer import UsuarioSerializer
from rest_framework.response import Response
from rest_framework import status as status_http, permissions


class Me(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer_usuario = UsuarioSerializer(request.user, context={"request": request})

        return Response(serializer_usuario.data, status_http.HTTP_200_OK)