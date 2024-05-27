from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import IndispMilitar, DiaZero
from cadastros.models import Militar
from django.contrib import messages
from django.urls import reverse
from datetime import datetime
from cadastros.models import Militar, Empenho
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from django.views import View
from .models import DiaZero
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware, get_default_timezone


def formatdatetime(value):
    if value:
        return value.strftime("%d/%m/%Y %H:%M")
    else:
        return None


def verif_indisp(id_mil, data_i_ind, data_f_ind):

    # filtrar todos os empenhos que perteçam ao militar, conforme model e relação ManytoMany
    empenhos = Empenho.objects.filter(militares__id=id_mil)

    for empenho in empenhos:
        em_ini = empenho.datahorainicial
        fin_em_ini = em_ini.strftime("%d/%m/%Y %H:%M")
        em_ini = datetime.strptime(fin_em_ini, '%d/%m/%Y %H:%M')

        em_end = empenho.datahorafinal
        fin_em_end = em_end.strftime("%d/%m/%Y %H:%M")
        em_end = datetime.strptime(fin_em_end, '%d/%m/%Y %H:%M')

        print(f"Data inicial do empenho: {em_ini}")
        print(f"Do tipo: {type(em_ini)}")
        print(f"Data final do empenho: {em_end}")
        print(f"Do tipo: {type(em_end)}")
        print(f"Data inicial da indisponibilidade: {data_i_ind}")
        print(f"Do tipo: {type(data_i_ind)}")
        print(f"Data final da indisponibilidade: {data_f_ind}")
        print(f"Do tipo: {type(data_f_ind)}")
        if data_i_ind <= em_ini <= data_f_ind or data_i_ind <= em_end <= data_f_ind:
            return True, empenho
    return False, None

# Início Indisponibilidade


@login_required
def registrar_indisp(request):
    militares = Militar.objects.all()
    if request.method == 'POST':

        typeindisp = request.POST.get('typeindisp', '')
        descindisp = request.POST.get('descindisp', '')
        datahorainitindisp = request.POST.get('datahorainitindisp', None)
        datahorafinalindisp = request.POST.get('datahorafinalindisp', None)
        datainitindisp = request.POST.get('datainitindisp', None)
        datafinalindisp = request.POST.get('datafinalindisp', None)
        militar_id = request.POST.get('militarindisp', '')

        if not datainitindisp and not datahorainitindisp:
            messages.add_message(request, messages.ERROR,
                                 'Nenhum campo de data deve estar em branco!')
            return redirect(reverse('registrar_indisp'))

        if datainitindisp:

            datainit = datetime.strptime(
                datainitindisp + " 00:00", '%d/%m/%Y %H:%M')
            # Configuração de timezone

            if datafinalindisp:
                datafinal = datetime.strptime(
                    datafinalindisp + " 23:59", '%d/%m/%Y %H:%M')
                # Configuração de timezone
            else:
                datafinal = None  # ou algum valor padrão, caso necessário

        else:
            if datahorainitindisp:
                datainit = datetime.strptime(
                    datahorainitindisp, '%d/%m/%Y %H:%M')
            else:
                datainit = None  # ou algum valor padrão, caso necessário

            if datahorafinalindisp:
                datafinal = datetime.strptime(
                    datahorafinalindisp, '%d/%m/%Y %H:%M')
            else:
                datafinal = None  # ou algum valor padrão, caso necessário

        # Verifica se algum dos campo estão em branco
        if not typeindisp or not datainit or not datafinal or not militar_id:
            messages.add_message(request, messages.ERROR,
                                 'Nenhum campo deve estar em branco!')
            return redirect(reverse('registrar_indisp'))

        # Verifica se não existe para o militar cadastrado uma indisponibilidade no mesmo período
        indisps = IndispMilitar.objects.filter(militar_id=militar_id)
        if indisps:
            for indisp in indisps:

                indisp_ini = indisp.datainicial
                fin_em_ini = indisp_ini.strftime("%d/%m/%Y %H:%M")
                indisp_ini = datetime.strptime(fin_em_ini, '%d/%m/%Y %H:%M')

                indisp_end = indisp.datafinal
                fin_em_end = indisp_end.strftime("%d/%m/%Y %H:%M")
                indisp_end = datetime.strptime(fin_em_end, '%d/%m/%Y %H:%M')

                if indisp_ini <= datainit <= indisp_end or indisp_ini <= datafinal <= indisp_end:
                    messages.add_message(
                        request, messages.ERROR, 'Já existe uma indisponibilidade para o militar neste período!')
                    return redirect(reverse('registrar_indisp'))

        # Verifica se o militar possui empenho no mesmo periodo
        empenho = verif_indisp(militar_id, datainit, datafinal)
        if empenho[0]:
            messages.add_message(request, messages.ERROR, f'O militar possui o empenho de {empenho[1].nome} para o periodo de {
                                 formatdatetime(empenho[1].datahorainicial)} até {formatdatetime(empenho[1].datahorafinal)}')

            return redirect(reverse('registrar_indisp'))

        # Verifica se a data inicial é menor que a data final
        if datainit > datafinal:
            messages.add_message(
                request, messages.ERROR, 'A data inicial não pode ser maior que a data final!')
            return redirect(reverse('registrar_indisp'))
        print(f"Data inicial: {datainit}")
        print(f"Data final: {datafinal}")
        # Faz o cadastro da indisponibilidade
        indispmilitar = IndispMilitar.objects.create(
            tipo=typeindisp,
            descricao=descindisp,
            datainicial=datainit,
            datafinal=datafinal,
            militar_id=militar_id
        )
        indispmilitar.save()
        request.session['limpar_localstorage'] = True
        messages.add_message(request, messages.SUCCESS,
                             'Indisponibilidade cadastrada com sucesso!')
        return redirect(reverse('registrar_indisp'))

    else:
        context = {
            'militares': militares,
        }

        limpar_localstorage = request.session.pop('limpar_localstorage', None)

        if limpar_localstorage:
            # Aqui, você pode passar um contexto para a função render que indica que o localStorage deve ser limpo
            context['limpar_localstorage'] = True

        return render(request, 'registrar_indisp.html', context)


@login_required
def delete_indisp(request, id_indisp):
    if request.method == 'POST':
        # Verifica se existe a indisponibilidade
        try:
            indispmilitar = IndispMilitar.objects.get(id=id_indisp)
            indispmilitar.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Indisponibilidade deletada com sucesso!')
            return redirect(reverse('listar_indisp'))
        except IndispMilitar.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 'Indisponibilidade não existe!')
            return redirect(reverse('listar_indisp'))
    else:
        return redirect(reverse('listar_indisp'))


@login_required
def edit_indisp(request, id_indisp):
    if request.method == 'POST':
        typeindispedit = request.POST.get('typeindispedit')
        datainitindispedit = request.POST.get('datainitindispedit')
        datafinalindispedit = request.POST.get('datafinalindispedit')
        descindispedit = request.POST.get('descindispedit')

        # Recuperando a indisponibilidade
        indispmilitar = IndispMilitar.objects.get(id=id_indisp)

        # Formantando as datas
        datainit = datetime.strptime(datainitindispedit, '%d/%m/%Y')
        datafinal = datetime.strptime(datafinalindispedit, '%d/%m/%Y')

        # Convertendo para date
        datainit_date = datainit.date()
        datafinal_date = datafinal.date()

        # Verifica se algum dos campo estão em branco
        if not typeindispedit or not descindispedit or not datainit_date or not datafinal_date:
            messages.add_message(request, messages.ERROR,
                                 'Preencha todos os campos!')
            return redirect(reverse('edit_indisp', args=[id_indisp]))

        # Verifica se a data inicial é menor que a data final
        if datainit_date > datafinal_date:
            messages.add_message(
                request, messages.ERROR, 'A data inicial não pode ser maior que a data final!')
            return redirect(reverse('edit_indisp', args=[id_indisp]))

        # Verifica se os campos retornados são iguais aos da indisponibilidade. Se sim não faz nada, se não atualiza
        if indispmilitar.tipo != typeindispedit:
            indispmilitar.tipo = typeindispedit
        if indispmilitar.descricao != descindispedit:
            indispmilitar.descricao = descindispedit
        if indispmilitar.datainicial != datainit_date:
            indispmilitar.datainicial = datainit_date
        if indispmilitar.datafinal != datafinal_date:
            indispmilitar.datafinal = datafinal_date

        indispmilitar.save()
        messages.add_message(request, messages.SUCCESS,
                             'Indisponibilidade atualizada com sucesso!')
        return redirect(reverse('listar_indisp'))
    else:
        return redirect(reverse('listar_indisp'))


@login_required
def listar_indisp(request):
    insisponibilidades = IndispMilitar.objects.all()
    # lista com anos de 2023 a 2030
    anos = [ano for ano in range(2023, 2031)]
    # lista de meses do ano
    meses = [mes for mes in range(1, 13)]

    return render(request, 'listar_indisp.html', {'indisponibilidades': insisponibilidades, 'anos': anos, 'meses': meses})

# Fim indisponibilidade

# Iníncio Feriado e Liberações


@login_required
def registrar_ferlib(request):
    if request.method == 'POST':
        nomeferlib = request.POST.get('nomeferlib', '')
        descferlib = request.POST.get('descferlib', '')
        classferlib = request.POST.get('classferlib', '')
        dataferlib = request.POST.get('dataferlib', '')
        horainicial = request.POST.get('horainicial', None)
        horafinal = request.POST.get('horafinal', None)
        only_date = request.POST.get('has_datahora', '')

        if not only_date and (not horainicial or not horafinal):
            messages.add_message(
                request, messages.ERROR, 'Informe a Hora inicial / final ou marque a opção "Especificar Apenas Data"')
            return redirect(reverse('registrar_ferlib'))

        if only_date:
            horainicial = '00:00'
            horafinal = '23:59'

        # Não permitir que os campos nomeferlib, classferlib ou dataferlib estejam em  branco
        if nomeferlib == '' or classferlib == '' or dataferlib == '':
            messages.add_message(
                request, messages.ERROR, 'Campos obrigatórios não podem ficar em branco: Nome, Classe e Data')
            return redirect(reverse('registrar_ferlib'))

        # Converte data no formato correto
        if dataferlib:
            datainit = datetime.strptime(dataferlib, '%d/%m/%Y')
            dataferlib = datainit.date()

        print(f"Hora inicial: {horainicial}")
        print(f"Tipo de Hora inicial: {type(horainicial)}")
        print(f"Hora final: {horafinal}")
        print(f"Tipo de Hora final: {type(horafinal)}")

        # Formata hora inicial e final para o formato Timefield do model
        if horainicial:
            horainicial = datetime.strptime(horainicial, '%H:%M')
            horainicial = horainicial.time()
        if horafinal:
            horafinal = datetime.strptime(horafinal, '%H:%M')
            horafinal = horafinal.time()

        # Verifica se a data inicial é menor que a data final
        if horainicial and horafinal:
            if horainicial > horafinal:
                messages.add_message(
                    request, messages.ERROR, 'A hora inicial não pode ser maior que a hora final!')
                return redirect(reverse('registrar_ferlib'))

        # Verifica se já existe um feriado ou liberação com a mesma data com o mesmo nome
        ferlib = DiaZero.objects.filter(nome=nomeferlib, data=dataferlib)
        if ferlib:
            messages.add_message(
                request, messages.ERROR, 'Já existe um feriado ou liberação com o mesmo nome e data!')
            return redirect(reverse('registrar_ferlib'))

        # Verifica se only_date é igual a on ou é vazio e atribui o valor True ou False
        only_date = True if only_date == 'on' else False

        # Registra o feriado ou liberação
        diazero = DiaZero.objects.create(
            nome=nomeferlib,
            descricao=descferlib,
            classe=classferlib,
            data=dataferlib,
            horainicial=horainicial,
            horafinal=horafinal,
            all_day=only_date
        )

        diazero.save()
        messages.add_message(request, messages.SUCCESS,
                             'Feriado ou Liberação cadastrado com sucesso!')
        return redirect(reverse('registrar_ferlib'))

    else:
        return render(request, 'registrar_ferlib.html')


@login_required
def listar_ferlib(request):
    feriadolib = DiaZero.objects.all()
    # lista com anos de 2023 a 2030
    anos = [ano for ano in range(2023, 2031)]
    # lista de meses do ano
    meses = [mes for mes in range(1, 13)]

    return render(request, 'listar_ferlib.html', {'feriadolib': feriadolib, 'anos': anos, 'meses': meses})


@login_required
def delete_ferlib(request, id_ferlib):
    if request.method == 'POST':
        # Verifica se existe o feriado ou liberação
        try:
            diazero = DiaZero.objects.get(id=id_ferlib)
            diazero.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Feriado ou Liberação deletado com sucesso!')
            return redirect(reverse('listar_ferlib'))
        except DiaZero.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 'Feriado ou Liberação não existe!')
            return redirect(reverse('listar_ferlib'))


@login_required
def verificar_datas(request):
    if request.method == 'POST':
        datahora_inicio = request.POST.get('datahorainicio')
        datahora_fim = request.POST.get('datahorafim')

        print(f"Data inicial: {datahora_inicio}")
        print(f"Data final: {datahora_fim}")
        # Verificar se as datas são válidas
        try:
            datahora_inicio = datetime.strptime(
                datahora_inicio, '%d/%m/%Y %H:%M')
            datahora_fim = datetime.strptime(datahora_fim, '%d/%m/%Y %H:%M')
        except ValueError:
            return JsonResponse({'erro': 'f_dat_inv'}, status=400)

        print(f"Data inicial maior que final?: {
              datahora_fim <= datahora_inicio}")

        # Verificar se datahora_fim é maior que datahora_inicio
        if datahora_fim <= datahora_inicio:
            return JsonResponse({'erro': 'datainitnot'}, status=400)

        minutos_tipicos = 0
        minutos_atipicos = 0

        delta = timedelta(minutes=1)
        try:
            while datahora_inicio < datahora_fim:
                dia_da_semana = datahora_inicio.weekday()
                hora = datahora_inicio.time()

                # Verificar se está em um DiaZero
                dia_zero = DiaZero.objects.filter(data=datahora_inicio.date(),
                                                  horainicial__lte=hora,
                                                  horafinal__gte=hora).exists()

                if dia_zero:
                    minutos_atipicos += 1
                elif (dia_da_semana in [0, 1, 3, 4] and time(8, 30) <= hora < time(17, 0)) or \
                        (dia_da_semana == 2 and time(8, 30) <= hora < time(13, 0)):
                    minutos_tipicos += 1
                else:
                    minutos_atipicos += 1

                datahora_inicio += delta

            return JsonResponse({
                'minutos_tipicos': minutos_tipicos,
                'minutos_atipicos': minutos_atipicos}, status=200)
        except:

            return JsonResponse({'erro': 'errocomum'}, status=400)


# Fim Feriado e Liberações
