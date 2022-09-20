from ..models import Usuario, Diaria


def listar_oportunidades(diarista_id):
    cidades_atendidas_usuario = Usuario.diarista_objects.cidades_atendidas(diarista_id)
    oportunidades_cidades = Diaria.diaria_objects.oportunidades_cidade(
        cidades_atendidas_usuario).filter(numero_diarista__lt=3).exclude(
            candidatas=diarista_id)

    return oportunidades_cidades