from datetime import datetime
from django.urls import reverse
from rest_framework.serializers import ModelSerializer, DecimalField, ValidationError, SerializerMethodField
from ..models import Diaria, Usuario
from administracao.services.servico_service import listar_servico_id
from ..services.cidades_atendimento_service import verificar_disponibilidade_cidade, buscar_cidade_ibge
from ..hateoas import Hateoas
from django.utils import timezone
from ..services.avaliacao_diaria_service import verificar_avaliacao_usuario


class UsuarioDiariaSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nome_completo', 'nascimento', 'telefone', 'tipo_usuario', 'reputacao', 'foto_usuario')


class DiariaSerializer(ModelSerializer):
    cliente = UsuarioDiariaSerializer(read_only=True)
    diarista = UsuarioDiariaSerializer(read_only=True)
    valor_comissao = DecimalField(read_only=True, max_digits=5, decimal_places=2)
    links = SerializerMethodField(required=False)
    nome_servico = SerializerMethodField(required=False)
    status = SerializerMethodField()

    class Meta:
        model = Diaria
        fields = '__all__'

    
    def validate(self, attrs):
        if not verificar_disponibilidade_cidade(attrs['cep']):
            raise ValidationError('Não há diaristas para o CEP informado')
        qtd_comodos = attrs['quantidade_quartos'] + attrs['quantidade_salas'] + attrs['quantidade_cozinhas'] + \
            attrs['quantidade_banheiros'] + attrs['quantidade_outros']
        if qtd_comodos == 0:
            raise ValidationError('A diária deve ter, pelo menos, um cômodo')
        return attrs

    def validate_codigo_ibge(self, codigo_ibge):
        buscar_cidade_ibge(codigo_ibge)
        return codigo_ibge

    def validate_preco(self, preco):
        servico = listar_servico_id(self.initial_data['servico'])
        if servico is None:
            raise ValidationError('Servico não existe')
        valor_total = 0
        valor_total += servico.valor_quarto * self.initial_data['quantidade_quartos']
        valor_total += servico.valor_sala * self.initial_data['quantidade_salas']
        valor_total += servico.valor_banheiro * self.initial_data['quantidade_banheiros']
        valor_total += servico.valor_cozinha * self.initial_data['quantidade_cozinhas']
        valor_total += servico.valor_quintal * self.initial_data['quantidade_quintais']
        valor_total += servico.valor_outros * self.initial_data['quantidade_outros']
        if preco >= servico.valor_minimo:
            if preco == valor_total or valor_total <= servico.valor_minimo:
                return preco
            raise ValidationError('Valor não corresponde ao serviço contratado')
        raise ValidationError('Valor abaixo do valor mínimo do serviço')
    
    def validate_tempo_atendimento(self, tempo_atendimento):
        print(self.initial_data)
        servico = listar_servico_id(self.initial_data['servico'])
        if servico is None:
            raise ValidationError('Servico não existe')
        horas_total = 0
        horas_total += servico.horas_quarto * self.initial_data['quantidade_quartos']
        horas_total += servico.horas_sala * self.initial_data['quantidade_salas']
        horas_total += servico.horas_banheiro * self.initial_data['quantidade_banheiros']
        horas_total += servico.horas_cozinha * self.initial_data['quantidade_cozinhas']
        horas_total += servico.horas_quintal * self.initial_data['quantidade_quintais']
        horas_total += servico.horas_outros * self.initial_data['quantidade_outros']
        if tempo_atendimento != horas_total:
            raise ValidationError('Valores não correspondem')
        return tempo_atendimento

    def validate_data_atendimento(self, data_atendimento):
        if data_atendimento.hour < 6:
            raise ValidationError('Horário de início não pode ser menor que 06:00')
        if (data_atendimento.hour + self.initial_data['tempo_atendimento']) > 22:
            raise ValidationError('Horário de atendimento não pode passar das 22:00')
        if data_atendimento <= (timezone.now() + timezone.timedelta(hours=48)):
            ValidationError('A data de atendimento deve ser, no mínimo, 48h da hora atual')
        return data_atendimento
    
    def create(self, validated_data):
        servico = listar_servico_id(validated_data['servico'].id)
        valor_comissao = validated_data['preco'] * servico.porcentagem_comissao / 100
        cliente_id = self.context['request'].user.id
        diaria = Diaria.objects.create(cliente_id=cliente_id, valor_comissao=valor_comissao, **validated_data)
        return diaria

    def get_links(self, obj):
        links = Hateoas()
        data_atual = datetime.now()
        data_atendimento = obj.data_atendimento.replace(tzinfo=None)
        usuario = self.context['request'].user

        if obj.status == 1:
            if usuario.tipo_usuario == 1:
                links.add_post('pagar_diaria', reverse('pagamento-diaria-list', kwargs={'diaria_id': obj.id}))
        elif obj.status == 2:
            if data_atual < data_atendimento:
                links.add_patch('cancelar_diaria', reverse('cancelar-diaria-detail', kwargs={'diaria_id': obj.id}))
            if usuario.tipo_usuario == 2:
                links.add_post('candidatar_diaria', reverse('candidatar-diarista-diaria-list', kwargs={'diaria_id': obj.id}))
        elif obj.status == 3:
            if data_atual < data_atendimento:
                links.add_patch('cancelar_diaria', reverse('cancelar-diaria-detail', kwargs={'diaria_id': obj.id}))
            if usuario.tipo_usuario == 1:
                if(data_atual >= data_atendimento):
                    links.add_patch('confirmar_diarista', reverse('confirmar-presenca-diaria-detail', kwargs={'diaria_id': obj.id}))
        elif obj.status == 4:
            avaliacoes_diaria = obj.avaliacao_diaria.filter(avaliador__isnull=False) or None
            if avaliacoes_diaria is None:
                links.add_patch('avaliar_diaria', reverse('avaliacao-diaria-detail', kwargs={'diaria_id': obj.id}))
            else:
                for avaliacao in avaliacoes_diaria:
                    if usuario.id != avaliacao.avaliador.id:
                        links.add_patch('avaliar_diaria', reverse('avaliacao-diaria-detail', kwargs={'diaria_id': obj.id}))
        if obj.status != 1:
            links.add_get('self', reverse('diaria-detail', kwargs={'diaria_id': obj.id}))
        return links.to_array()

    def get_status(self, obj):
        usuario = self.context['request'].user
        if verificar_avaliacao_usuario(obj.id, usuario.id):
            return 6
        return obj.status

    def get_nome_servico(self, obj):
        return obj.servico.nome