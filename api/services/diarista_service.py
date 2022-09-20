from ..models import AvaliacaoDiaria
from ..services.usuario_service import atualizar_reputacao_usuario


def penalizar_diarista(diarista, diaria):
    AvaliacaoDiaria.objects.create(descricao="", nota=0, visibilidade=0, diaria=diaria, avaliador=None, avaliado=diarista)
    reputacao = AvaliacaoDiaria.avaliacao_objects.reputacao_usuario(diarista.id)
    atualizar_reputacao_usuario(diarista, reputacao['nota__avg'])