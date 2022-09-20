from rest_framework import serializers
from ..models import Diaria, Usuario
from ..hateoas import Hateoas
from django.urls import reverse


class AvaliacoesOportunidadeSerializer(serializers.BaseSerializer):
    def to_representation(self):
        return [
            {
                'descricao': 'lorem Ipsum ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut al',
                'nota': 4,
                'nome_avaliador': 'João',
                'foto_avaliador': 'joao.png'
            },
            {
                'descricao': 'lorem Ipsum ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut al',
                'nota': 5,
                'nome_avaliador': 'Maria',
                'foto_avaliador': 'maria.png'
            },
        ]


class ClienteOportunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nome_completo', 'telefone', 'nascimento', 'tipo_usuario', 'reputacao', 'foto_usuario')


class OportunidadeSerializer(serializers.ModelSerializer):
    nome_servico = serializers.SerializerMethodField()
    cliente = ClienteOportunidadeSerializer()
    links = serializers.SerializerMethodField()
    avaliacoes_clientes = serializers.SerializerMethodField()

    class Meta:
        model = Diaria
        fields = '__all__'

    
    def get_avaliacoes_clientes(self, obj):
        return AvaliacoesOportunidadeSerializer().to_representation()

    def get_nome_servico(self, obj):
        return obj.servico.nome

    def get_links(self, obj):
        usuario = self.context['request'].user
        links = Hateoas()
        if obj.status == 2:
            links.add_get('self', reverse('diaria-detail', kwargs={'diaria_id': obj.id}))
            candidatos = obj.candidatas.all()
            if usuario not in candidatos:
                links.add_post('candidatar_diaria', reverse('candidatar-diarista-diaria-list', kwargs={'diaria_id': obj.id}))
        return links.to_array()