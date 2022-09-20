from ..models import Diaria
from ..services.pagamento_diaria_service import cancelar_pagamento
from ..services.cancelar_diaria_service import verificar_diferenca_data_diaria
import datetime


def cancelar_diaria_task():
    diarias = Diaria.objects.filter(status=2)
    for diaria in diarias:
        if not diaria.candidatas.exists():
            if verificar_diferenca_data_diaria(diaria.data_atendimento) <= datetime.timedelta(hours=24):
                cancelar_pagamento(diaria.id, False)
                diaria.status = 5
                diaria.save()