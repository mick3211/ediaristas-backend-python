import requests
from rest_framework import serializers
import json
from .usuario_service import listar_usuario_id
from ..models import CidadesAtendimento

def cadastrar_cidade(codigo_ibge, cidade, estado):
    return CidadesAtendimento.objects.get_or_create(codigo_ibge=codigo_ibge,
        defaults=dict(cidade=cidade, estado=estado))

def buscar_cidade_cep(cep):
    request = requests.get(f"https://viacep.com.br/ws/{cep}/json/")

    if request.status_code == 400:
        raise serializers.ValidationError({"detail": "Erro ao buscar o CEP"})

    cidade_api = json.loads(request.content)

    if 'erro' in cidade_api:
        raise serializers.ValidationError({'detail': 'O CEP informado não foi encontrado'})

    return cidade_api

def buscar_cidade_ibge(codigo_ibge):
    req = requests.get(f'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{codigo_ibge}')
    if len(req.content) == 2:
        raise serializers.ValidationError('A cidade não existe')
    cidade = json.loads(req.content)
    return cidade

def relacionar_cidade_diarista(usuario, cidades):
    usuario_relacionar = listar_usuario_id(usuario.id)
    usuario_relacionar.cidades_atendidas.clear()
    for cidade in cidades.value:
        dados_api = buscar_cidade_ibge(cidade['codigo_ibge'])
        cidade_nova, create = cadastrar_cidade(cidade['codigo_ibge'], dados_api['nome'],
            dados_api['microrregiao']['mesorregiao']['UF']['sigla'])
        usuario_relacionar.cidades_atendidas.add(cidade_nova.id)

def listar_diaristas_cidade(cep):
    codigo_ibge = buscar_cidade_cep(cep)['ibge']
    try:
        cidade = CidadesAtendimento.objects.get(codigo_ibge=codigo_ibge)
        return cidade.usuario.filter(tipo_usuario=2).order_by('-reputacao')
    except CidadesAtendimento.DoesNotExist:
        return []

def verificar_disponibilidade_cidade(cep):
    codigo_ibge = buscar_cidade_cep(cep)['ibge']
    return CidadesAtendimento.objects.filter(codigo_ibge=codigo_ibge).exists()