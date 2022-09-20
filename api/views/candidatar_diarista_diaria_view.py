from rest_framework.views import APIView
from ..permissions.diarista_permission import DiaristaPermission
from rest_framework import status
from rest_framework.response import Response
from ..services import candidatar_diarista_diaria_service


class CandidatarDiaristaDiaria(APIView):
    permission_classes=[DiaristaPermission]

    def post(self, req, diaria_id, format=None):
        candidatar_diarista_diaria_service.relacionar_candidato_diaria(diaria_id, req.user.id)
        return Response({"Candidatura realizada com sucesso"}, status.HTTP_201_CREATED)