from datetime import datetime, timedelta
from ..services import diaria_service, usuario_service, pagamento_diaria_service, diarista_service
from rest_framework.serializers import ValidationError


def cancelar_diaria(diaria_id, usuario_id):
    diaria = diaria_service.listar_diaria_id(diaria_id)
    usuario = usuario_service.listar_usuario_id(usuario_id)
    if diaria.status not in [2, 3]:
        raise ValidationError("Esta diária não pode ser cancelada")
    verificar_data_cancelamento(diaria.data_atendimento)
    penalidade = verificar_penalizacao_cancelamento(diaria.data_atendimento)
    if usuario.tipo_usuario == 1:
        pagamento_diaria_service.cancelar_pagamento(diaria_id, penalidade)
        return
    pagamento_diaria_service.cancelar_pagamento(diaria_id, False)
    diarista_service.penalizar_diarista(usuario, diaria)

def verificar_penalizacao_cancelamento(data_diaria):
    return verificar_diferenca_data_diaria(data_diaria) <= timedelta(hours=24)

def verificar_data_cancelamento(data_diaria):
    data_atual = datetime.now()
    data_diaria_cancelar = data_diaria.replace(tzinfo=None)
    if data_atual > data_diaria_cancelar:
        raise ValidationError("Esta diária não pode ser cancelada. Entre em contato com o nosso suporte.")
    return data_diaria

def verificar_diferenca_data_diaria(data_diaria):
    data_atual = datetime.now()
    data_diaria_contratacao = data_diaria.replace(tzinfo=None)
    diferenca = data_diaria_contratacao - data_atual 
    return abs(diferenca)