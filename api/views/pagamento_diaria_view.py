from os import stat
from rest_framework.views import APIView
from ..services.pagamento_diaria_service import realizar_pagamento
from ..services import diaria_service
from ..serializers.pagamento_diaria_serializer import PagamentoDiariaSerializer
from rest_framework.response import Response
from rest_framework import status
from ..permissions.cliente_permission import ClientePermission


class PagamentoDiaria(APIView):
    permission_classes = [ClientePermission, ]
    def post(self, req, diaria_id, format=None):
        diaria = diaria_service.listar_diaria_id(diaria_id)
        self.check_object_permissions(self.request, diaria)
        serializer_pagamento = PagamentoDiariaSerializer(data=req.data)
        if serializer_pagamento.is_valid():
            card_hash = serializer_pagamento.validated_data['card_hash']
            if diaria.status == 1:
                realizar_pagamento(diaria, card_hash)
                return Response({'Diária paga com sucesso'}, status=status.HTTP_200_OK)
            return Response({'Não é possível pagar esta diária'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer_pagamento.errors, status=status.HTTP_400_BAD_REQUEST)