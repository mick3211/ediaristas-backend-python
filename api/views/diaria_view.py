from rest_framework.views import APIView
from ..serializers.diaria_serializer import DiariaSerializer
from rest_framework.response import Response
from rest_framework import status as status_http, permissions, serializers
from ..services.diaria_service import listar_diarias_usuario, listar_diaria_id
from ..permissions.dono_permission import DonoPermission


class DiariaView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, req, format=None):
        diarias = listar_diarias_usuario(req.user.id)
        serializer_diaria = DiariaSerializer(diarias, many=True, context={'request': req})
        return Response(serializer_diaria.data, status=status_http.HTTP_200_OK)

    def post(self, req, format=None):
        serializer_diaria = DiariaSerializer(data=req.data, context={'request': req})
        if(req.user.tipo_usuario == 2):
            raise serializers.ValidationError('Apenas clientes podem solicitar diárias')
        if(serializer_diaria.is_valid()):
            serializer_diaria.save()
            return Response(serializer_diaria.data, status=status_http.HTTP_201_CREATED)
        return Response(serializer_diaria.errors, status=status_http.HTTP_400_BAD_REQUEST)


class DiariaId(APIView):
    permission_classes = [DonoPermission]
    
    def get(self, req, diaria_id, format=None):
        diaria = listar_diaria_id(diaria_id)
        self.check_object_permissions(req, diaria)
        serializer_diaria = DiariaSerializer(diaria, context={'request': req})
        return Response(serializer_diaria.data, status=status_http.HTTP_200_OK)