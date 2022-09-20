from multiprocessing import context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..permissions.diarista_permission import DiaristaPermission
from ..serializers.endereco_diarista_serializer import EnderecoDiaristaSerializer
from ..models import EnderecoDiarista as EnderecoDiaristaModel


class EnderecoDiarista(APIView):
    permission_classes= [DiaristaPermission]

    def put(self, req, format=None):
        serializer_endereco_diarista = EnderecoDiaristaSerializer(data=req.data, context={'request': req})
        if serializer_endereco_diarista.is_valid():
            serializer_endereco_diarista.save()
            return Response(serializer_endereco_diarista.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer_endereco_diarista.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        endereco = EnderecoDiaristaModel.objects.get(usuario=request.user.id)
        serializer_endereco_diarista = EnderecoDiaristaSerializer(endereco, context={'request': request})
        return Response(serializer_endereco_diarista.data, status.HTTP_200_OK)