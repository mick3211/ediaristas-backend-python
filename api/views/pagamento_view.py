from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Diaria, Pagamento as PagamentoModel
from ..serializers.pagamento_serializer import PagamentoSerializer
from ..permissions.diarista_permission import DiaristaPermission


class Pagamento(APIView):
    permission_classes = [DiaristaPermission]

    def get(self, request, format=None):
        diarias_pagamento = Diaria.objects.filter(diarista=request.user.id).filter(status__in=[4, 6, 7])
        pagamentos = PagamentoModel.objects.filter(diaria__in=diarias_pagamento)
        serializer_pagamento = PagamentoSerializer(pagamentos, many=True)
        return Response(serializer_pagamento.data, status=status.HTTP_200_OK)