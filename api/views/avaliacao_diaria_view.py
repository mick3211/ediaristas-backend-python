from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from ..serializers.avaliacao_diaria_serializer import AvaliacaoDiariaSerializer
from ..permissions.dono_permission import DonoPermission
from ..models import AvaliacaoDiaria
from ..services.diaria_service import listar_diaria_id, atualizar_status_diaria
from ..services.usuario_service import listar_usuario_id, atualizar_reputacao_usuario
from ..services.avaliacao_diaria_service import verificar_avaliacao_usuario, verificar_qtd_avaliacao


class AvaliacaoDiariaID(APIView):
    permission_classes = [DonoPermission]

    def patch(self, request, diaria_id, format=None):
        diaria = listar_diaria_id(diaria_id)
        if diaria.status != 4:
            raise serializers.ValidationError("Apenas diárias com status 4 podem ser avaliadas")
        usuario_logado = listar_usuario_id(request.user.id)
        self.check_object_permissions(self.request, diaria)
        serializer_avaliacao_diaria = AvaliacaoDiariaSerializer(data=request.data)
        if verificar_avaliacao_usuario(diaria_id, usuario_logado.id):
            raise serializers.ValidationError('O usuário já avaliou esta diária')
        if serializer_avaliacao_diaria.is_valid():
            if usuario_logado.tipo_usuario == 1:
                avaliado = diaria.diarista
            else:
                avaliado = diaria.cliente
            serializer_avaliacao_diaria.save(visibilidade=1, diaria=diaria, avaliador=usuario_logado, avaliado=avaliado)
            media_usuario = AvaliacaoDiaria.avaliacao_objects.reputacao_usuario(avaliado.id)
            atualizar_reputacao_usuario(avaliado, media_usuario)
            if verificar_qtd_avaliacao(diaria_id) == 2:
                atualizar_status_diaria(diaria_id, 6)
            return Response(serializer_avaliacao_diaria.data, status=status.HTTP_201_CREATED)
        return Response(serializer_avaliacao_diaria.errors, status=status.HTTP_400_BAD_REQUEST)