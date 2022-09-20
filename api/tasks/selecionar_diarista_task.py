from datetime import timedelta
from django.db.models.aggregates import count
from ..models import Diaria
from ..services.candidatar_diarista_diaria_service import verificar_diferenca_data_contratacao
from ..services.selecionar_diarista_diaria_service import selecionar_diarista_diaria


def selecionar_diarista():
    diarias = Diaria.objects.annotate(candidatas_count=count('candidatas')
        ).filter(candidatas_count__gt=2).filter(status=2)

    for diaria in diarias:
        if(verificar_diferenca_data_contratacao(diaria.created_at) > timedelta(hours=24)):
            selecionar_diarista_diaria(diaria.id)