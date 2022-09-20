import email
from django.db.models.signals import post_save
from .models import CidadesAtendimento
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver 
from django.urls import reverse
import environ

env = environ.Env()
env.read_env('./ediaristas/.env')


def usuario_cadastrado(sender, instance, created, **kwargs):
    if created:
        assunto = 'Cadastro realizado com sucesso'
        corpo = ''
        destino = [instance.email,]
        remetente = 'mickaelfelizardo2008@gmail.com'
        mensagem_html = render_to_string('email_cadastro.html', {'usuario': instance})
        send_mail(assunto, corpo, remetente, destino, html_message=mensagem_html)

def diarista_selecionada(sender, instance, **kwargs):
    if instance.status == 3:
        html_message_cliente = render_to_string('email_diarista_selecionada.html', {'usuario': instance.cliente, 'diaria': instance.diaria})
        html_message_diarista = render_to_string('email_diarista_selecionada.html', {'usuario': instance.diarista, 'diaria': instance.diaria})
        remetente = 'mickaelfelizardo2008@gmail.com'
        destino_cliente = [instance.cliente.email]
        destino_diarista = [instance.diarista.email]
        assunto = 'Diarista selecionado'
        corpo = ''
        send_mail(assunto, corpo, remetente, destino_cliente, html_message=html_message_cliente)
        send_mail(assunto, corpo, remetente, destino_diarista, html_message=html_message_diarista)

def nova_oportunidade(sender, instance, **kwargs):
    if instance.status == 3:
        cidade_atendimento = CidadesAtendimento.objects.get(codigo_ibge=instance.codigo_ibge)
        diaristas_emails = cidade_atendimento.usuario.all().values('email')
        html_message_diarista = render_to_string('email_nova_oportunidade.html', {'usuario': instance.diarista, 'diaria': instance.diaria})
        remetente = 'mickaelfelizardo2008@gmail.com'
        assunto = 'Nova oportunidade no E-diaristas'
        corpo = ''
        lista_email = []
        for email in diaristas_emails:
            lista_email.append(email)
        send_mail(assunto, corpo, remetente, lista_email, html_message=html_message_diarista)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    html_message_reset = render_to_string('email_resetar_senha.html',
                                            {'link': '{}{}?token={}'.format(
                                                env('URL_FRONTEND'),
                                                reverse('password_reset:reset-password-request'),
                                                reset_password_token.key
                                            )})
    remetente = 'mickaelfelizardo2008@gmail.com'
    assunto = 'Recuperar senha E-diaristas'
    corpo = ''
    email_destino = [reset_password_token.user.email]
    send_mail(assunto, corpo, remetente, email_destino, html_message=html_message_reset)


# post_save.connect(diarista_selecionada, sender=Diaria) #ALterar template HTML
# post_save.connect(nova_oportunidade, sender=Diaria) #ALterar template HTML
# post_save.connect(usuario_cadastrado, sender=Usuario)