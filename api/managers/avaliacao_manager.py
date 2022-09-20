from django.db import models


class AvaliacaoManager(models.Manager):
    def reputacao_usuario(self, usuario_id):
        return self.get_queryset().filter(avaliado=usuario_id).aggregate(models.Avg('nota'))['nota__avg']