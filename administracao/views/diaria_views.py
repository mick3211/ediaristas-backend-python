from django.shortcuts import render, redirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from api.models import Diaria


@login_required
def listar_diarias(request):
    status = request.GET.get('status', None)
    if status is None:
        status_diaria = [1, 2, 3, 4, 5, 6, 7]
    elif status == 'pendentes':
        status_diaria = [3, 2]
    elif status == 'nao-avaliadas':
        status_diaria = [4]
    elif status == 'concluidas':
        status_diaria = [6, 7]
    elif status == 'canceladas':
        status_diaria = [5, 1]
        

    diarias = Diaria.objects.filter(status__in=status_diaria)
    return render(request, 'diarias/lista_diarias.html', {'diarias': diarias})


def transferir_pagamento_diaria(request, diaria_id):
    diaria = Diaria.objects.get(id=diaria_id)
    if diaria.status == 6:
        diaria.status = 7
        diaria.save()
    return redirect(reverse('listar_diarias'))