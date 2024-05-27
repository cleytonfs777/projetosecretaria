import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Militar, Empenho
from indisponibilidade.models import IndispMilitar
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from re import sub
from json import loads
from django.forms.models import model_to_dict
from datetime import timedelta


def normaliza_duracao(datahora_final, datahora_inicial):
    # Calcula a diferença entre as datas
    duracao_timedelta = datahora_final - datahora_inicial

    # Converte timedelta para minutos
    minutos = duracao_timedelta.total_seconds() / 60

    return int(minutos)


def format_name(full_name):
    # Lista de exceções que devem ser mantidas em minúsculas
    exceptions = ['de', 'da', 'das', 'do', 'dos']

    # Separa o nome completo em palavras
    name_parts = full_name.split()

    # Converte cada palavra de acordo com as regras especificadas
    formatted_parts = []
    for part in name_parts:
        if part.lower() in exceptions:
            formatted_parts.append(part.lower())
        else:
            formatted_parts.append(part.capitalize())

    # Combina as palavras formatadas em um único nome completo
    formatted_name = ' '.join(formatted_parts)
    return formatted_name


def verificar_datas(datahora_inicio, datahora_fim):
    try:
        datahora_inicio = datetime.strptime(datahora_inicio, '%d/%m/%Y %H:%M')
        datahora_fim = datetime.strptime(datahora_fim, '%d/%m/%Y %H:%M')
    except Exception as e:
        print(f"Erro ao converter data: {e}")
        return e
    print(f"Data inicial maior que final?: {datahora_fim <= datahora_inicio}")

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


def filter_horas(datahorainicial, datahorafinal):
    pass


def verificar_sobreposicao(datainicial1, datafinal1, datainicial2, datafinal2):
    """
    Verifica se há sobreposição entre dois intervalos de datas.
    Retorna True se não houver sobreposição e False caso contrário.
    """
    # Convertendo para offset-naive
    if datainicial1.tzinfo is not None:
        datainicial1 = datainicial1.replace(tzinfo=None)
    if datafinal1.tzinfo is not None:
        datafinal1 = datafinal1.replace(tzinfo=None)
    if datainicial2.tzinfo is not None:
        datainicial2 = datainicial2.replace(tzinfo=None)
    if datafinal2.tzinfo is not None:
        datafinal2 = datafinal2.replace(tzinfo=None)

    print(f"""
    {'*' * 20}
    datafinal1: {datafinal1} tipo: {type(datafinal1)}
    datainicial1: {datainicial1} tipo: {type(datainicial1)}
    datafinal2: {datafinal2} tipo: {type(datafinal2)}
    datainicial2: {datainicial2} tipo: {type(datainicial2)}
    {'*' * 20}
    """)

    # Verificando sobreposição
    if datainicial1 >= datafinal2 or datafinal1 <= datainicial2:
        return True  # Não há sobreposição
    else:
        return False  # Há sobreposição


@login_required
def cadastrar_militar(request):
    if request.method == 'POST':
        numero = request.POST.get('numbm', '')
        namebm = request.POST.get('namebm', '')
        postgrad = request.POST.get('postgradbm', '')
        localbm = request.POST.get('localbm', '')
        emp_mil_data = request.POST.getlist('emp_mil_data', '')
        empenhos_conv = loads(emp_mil_data[0])

        # Verifica se os campos não estão vazios
        if numero == '' or namebm == '' or postgrad == '' or localbm == '':
            messages.add_message(request, messages.ERROR,
                                 'Os campos não podem estar vazios!')
            return redirect(reverse('cadastrar_militar'))

        # Converter nome para format_name
        namebm = format_name(namebm)

        # Verifica se o militar já existe no banco de dados
        if Militar.objects.filter(numero=numero).exists():
            messages.add_message(request, messages.ERROR,
                                 'Militar já cadastrado!')
            return redirect(reverse('cadastrar_militar'))

        qtd_empenhos = 0
        empenhos_minutos_atipica = 0
        empenhos_minutos_tipica = 0

        militar = Militar.objects.create(numero=numero, nome=namebm, postgrad=postgrad, local=localbm,
                                         empenhos_minutos_atipica=empenhos_minutos_atipica, qtd_empenhos=qtd_empenhos, empenhos_minutos_tipica=empenhos_minutos_tipica)

        print(empenhos_conv['empenhos'])

        if len(empenhos_conv['empenhos']):

            for empenho in empenhos_conv['empenhos']:
                if empenho:
                    # Verifica se o id do empenho fornecido esta relacionado com o militar se não estiver ele adiciona o empenho ao militar e atualiza a quantidade de empenhos e a soma dos minutos
                    if Empenho.objects.filter(id=empenho).exists():
                        empenho_obj = Empenho.objects.get(id=empenho)
                        # Verifica se o miltar já possui esse id de empenho relacionado com ele
                        if not militar.empenhos.filter(id=empenho).exists():
                            militar.empenhos.add(empenho_obj)
                            militar.qtd_empenhos += 1
                            militar.empenhos_minutos_tipica += empenho_obj.duracao_em_minutos_tipica
                            militar.empenhos_minutos_atipica += empenho_obj.duracao_em_minutos_atipica

                    else:
                        print("Empenho não existe")
            # Salva as alterações no banco de dados
        militar.save()

        messages.add_message(request, messages.SUCCESS,
                             'Militar cadastrado com sucesso!')
        return redirect(reverse('cadastrar_militar'))
    else:
        empenhos = Empenho.objects.all()
        return render(request, 'cadastrar_militar.html', {'empenhos': empenhos})


@login_required
def cadastrar_empenho(request):

    if request.method == 'POST':
        namemp = request.POST.get('namemp', '')
        tipoemp = request.POST.get('tipoemp', '')
        datahorainicial_str = request.POST.get('datahorainicial')
        datahorafinal_str = request.POST.get('datahorafinal')
        datahorainicial = datetime.strptime(
            datahorainicial_str, '%d/%m/%Y %H:%M')
        datahorafinal = datetime.strptime(datahorafinal_str, '%d/%m/%Y %H:%M')
        hiddensei = request.POST.get('hiddensei', '')
        obsemp = request.POST.get('obsemp', '')
        hortip = request.POST.get('hortip', '')
        horatip = request.POST.get('horatip', '')
        all_militares = request.POST.get('emp_mil_data', '')
        all_militares_conv = [mil.strip() for mil in all_militares.split(',')]

        # Configuração de timezone

        datahorainicial -= timedelta(hours=3)
        datahorafinal -= timedelta(hours=3)

        # return HttpResponse(f"Recebido: \n namemp: {namemp} \n tipoemp: {tipoemp} \n datahorainicial: {datahorainicial} \n datahorafinal: {datahorafinal} \n hiddensei: {hiddensei} \n obsemp: {obsemp} \n hortip: {hortip} \n horatip: {horatip} \n all_militares_conv: {all_militares_conv}")

        # Verifica se os campos não estão vazios
        if namemp == '' or tipoemp == '' or datahorainicial_str == '' or datahorafinal_str == '':
            messages.add_message(request, messages.ERROR,
                                 'Os campos não podem estar vazios!')
            return redirect(reverse('cadastrar_empenho'))

        # Calcula a duração do empenho atraves da diferença entre a data e hora final e a data e hora inicial e converte para o formato HH:MM em string
        duracao = normaliza_duracao(datahorafinal, datahorainicial)

        # Verifica se o empenho já existe no banco de dados
        if Empenho.objects.filter(nome=namemp).exists():
            messages.add_message(request, messages.ERROR,
                                 'Empenho já cadastrado!')
            return redirect(reverse('cadastrar_empenho'))

        # Realiza o cadastro do empenho no banco de dados e posteriormente realiza um for na lista all_militares_conv e cadastra o empenho para cada militar, sendo que cada numero na lista corresponde ao numero do militar
        empenho = Empenho.objects.create(nome=namemp, tipo=tipoemp, datahorainicial=datahorainicial, datahorafinal=datahorafinal,
                                         duracao_em_minutos_atipica=horatip, duracao_em_minutos_tipica=hortip, documentacao=hiddensei, observacoes=obsemp)
        for militar in all_militares_conv:
            if militar:
                # Verifica se o militar existe no banco de dados
                if Militar.objects.filter(numero=militar).exists():
                    militar_obj = Militar.objects.get(numero=militar)
                    # Verifica se o empenho já existe no militar
                    if not militar_obj.empenhos.filter(nome=namemp).exists():
                        militar_obj.empenhos.add(empenho)
                        militar_obj.qtd_empenhos = int(
                            militar_obj.qtd_empenhos) + 1
                        militar_obj.empenhos_minutos_tipica = int(
                            militar_obj.empenhos_minutos_tipica) + int(hortip)
                        militar_obj.empenhos_minutos_atipica = int(
                            militar_obj.empenhos_minutos_atipica) + int(horatip)
                        militar_obj.save()
                else:
                    print("Militar não existe")
        # Salva as alterações no banco de dados
        empenho.save()

        messages.add_message(request, messages.SUCCESS,
                             'Empenho cadastrado com sucesso!')
        return redirect(reverse('cadastrar_empenho'))

    else:
        postos_grad = ['sd', '2sgt', 'cap', 'cb', '1sgt',
                       '2ten', 'maj', '3sgt', 'subten', '1ten']
        militares = Militar.objects.all()
        return render(request, 'cadastrar_empenho.html', {'militares': militares, 'postos_grad': postos_grad})


@login_required
def editar_empenho(request, id_empenho):
    if request.method == 'POST':

        namemp = request.POST.get('namemp', '')
        tipoemp = request.POST.get('tipoemp', '')
        datahorainicial_str = request.POST.get('datahorainicial')
        datahorafinal_str = request.POST.get('datahorafinal')
        datahorainicial = datetime.strptime(
            datahorainicial_str, '%d/%m/%Y %H:%M')
        datahorafinal = datetime.strptime(datahorafinal_str, '%d/%m/%Y %H:%M')
        hiddensei = request.POST.get('hiddensei', '')
        obsemp = request.POST.get('obsemp', '')
        hortip = request.POST.get('hortip', '')
        horatip = request.POST.get('horatip', '')
        all_militares = request.POST.get('emp_mil_data', '')
        # Vem na lista o numero de BM do militar
        all_militares_conv = [mil.strip() for mil in all_militares.split(',')]

        print(f"all_militares_conv: {all_militares_conv}")

        empenho_main = Empenho.objects.get(id=id_empenho)

        datahorainicial -= timedelta(hours=3)
        datahorafinal -= timedelta(hours=3)

        # Faz uma comparação de cada valor e verifica se o que foi postado é diferente dos itens de empenho_main
        if namemp != empenho_main.nome:
            empenho_main.nome = namemp
        if tipoemp != empenho_main.tipo:
            empenho_main.tipo = tipoemp
        if datahorainicial != empenho_main.datahorainicial:
            empenho_main.datahorainicial = datahorainicial
        if datahorafinal != empenho_main.datahorafinal:
            empenho_main.datahorafinal = datahorafinal
        if hiddensei != empenho_main.documentacao:
            empenho_main.documentacao = hiddensei
        if obsemp != empenho_main.observacoes:
            empenho_main.observacoes = obsemp

        empenho_main.save()

        # Verifica se algum militar que esta relacionado com o empenho mas não está em all_militares_conv. Se não estiver deve ser desvinculado. Deve se subtrair a quantidade de empenhos do militar e abater os minutos típicos e atípicos

        for militar_exist in empenho_main.militares.all():
            if militar_exist:
                if not all_militares_conv.__contains__(militar_exist.numero):
                    empenho_main.militares.remove(militar_exist)
                    militar_exist.qtd_empenhos -= 1
                    militar_exist.empenhos_minutos_tipica -= int(hortip)
                    militar_exist.empenhos_minutos_atipica -= int(horatip)
                    militar_exist.save()
                    empenho_main.save()

        # Adiciona todos os militares que estão em all_militares_conv. Se o Militar não estiver no empenho, deve ser adicionado. Se o militar já existir para o empenho nada deve ser feito. Deve ser somado a quantidade de empenhos do militar e somar os minutos de atípicos e titipicos

        for militar_numero in all_militares_conv:
            if militar_numero:
                if not empenho_main.militares.filter(numero=militar_numero).exists():
                    militar_new = Militar.objects.get(numero=militar_numero)
                    empenho_main.militares.add(militar_new)
                    militar_new.qtd_empenhos += 1
                    militar_new.empenhos_minutos_tipica += int(hortip)
                    militar_new.empenhos_minutos_atipica += int(horatip)
                    militar_new.save()
                    empenho_main.save()

        messages.add_message(request, messages.SUCCESS,
                             'Empenho editado com sucesso!')
        return redirect(reverse('registrar_empenho'))

    else:
        # Injetar na pagina todos os militares
        context = {
            'militares': Militar.objects.all(),
            'postos_grad': ['sd', '2sgt', 'cap', 'cb', '1sgt', '2ten', 'maj', '3sgt', 'subten', '1ten'],
            'empenho': get_object_or_404(Empenho, id=id_empenho),
        }
        return render(request, 'editar_empenho.html', context)


@login_required
def registrar_empenho(request):
    # Injetar na pagina todos os militares e todos os empenhos
    militares = Militar.objects.all()
    empenhos = Empenho.objects.all()
    return render(request, 'registrar_empenho.html', {'militares': militares, 'empenhos': empenhos})


@login_required
def listar_cadastros(request):
    # Injetar na pagina todos os militares e todos os empenhos
    militares = Militar.objects.all()
    empenhos = Empenho.objects.all()
    return render(request, 'listar_cadastros.html', {'militares': militares, 'empenhos': empenhos})


@login_required
def delete_militar(request, id_militar):
    if request.method == 'POST':
        militar = Militar.objects.get(id=id_militar)
        try:
            militar.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Militar excluido com sucesso')
            return redirect(reverse('registrar_empenho'))
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f'Erro ao deletar pacote: {e}')
            return redirect(reverse('registrar_empenho'))

    else:
        return HttpResponse(f"Você não tem autorização para acessar essa pagina: {e}", status=401)


@login_required
def delete_empenho(request, id_empenho):
    if request.method == 'POST':
        empenho = Empenho.objects.get(id=id_empenho)
        # Verifica se o empenho possui algum militar relacionado. Se tiver ele deve ser removido do militar e os campos empenhos_em_minutos e qtd_empenhos serem atualizados
        if empenho.militares.all():
            militares = empenho.militares.all()
            for militar in militares:
                militar.empenhos.remove(empenho)
                militar.qtd_empenhos = int(militar.qtd_empenhos) - 1
                militar.empenhos_minutos_atipica = int(
                    militar.empenhos_minutos_atipica) - empenho.duracao_em_minutos_atipica
                militar.empenhos_minutos_tipica = int(
                    militar.empenhos_minutos_tipica) - empenho.duracao_em_minutos_tipica
                militar.save()
        try:
            empenho.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Empenho excluido com sucesso')
            return redirect(reverse('registrar_empenho'))
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f'Erro ao deletar pacote: {e}')
            return redirect(reverse('registrar_empenho'))

    else:
        return HttpResponse("Você não tem autorização para acessar essa pagina", status=401)


@login_required
def edit_militar(request, id_militar):
    if request.method == 'POST':
        id_ = id_militar
        numero = request.POST.get('numbmform', '')
        nome = request.POST.get('namebmform', '')
        postgrad = request.POST.get('postgradbmform', '')
        local = request.POST.get('localbmform', '')
        empenhos = request.POST.getlist('all_data', '')
        empenhos_conv = loads(empenhos[0])
        # Busca os dados do militar pelo id
        militar = Militar.objects.get(id=id_)
        # Confere se os dados de numero, nome, postgrad e local são diferentes dos dados atuais do militar se for diferente ele atualiza os dados
        if numero != militar.numero:
            militar.numero = numero
        if nome != militar.nome:
            militar.nome = nome
        if postgrad != militar.postgrad:
            militar.postgrad = postgrad
        if local != militar.local:
            militar.local = local

        print(f"Esse é o resultado de EMpenhos conv: {empenhos_conv}")
        for empenho in empenhos_conv['empenhos']:
            if empenho:
                # Verifica se o id do empenho fornecido esta relacionado com o militar se não estiver ele adiciona o empenho ao militar e atualiza a quantidade de empenhos e a soma dos minutos
                if Empenho.objects.filter(id=empenho).exists():
                    empenho_obj = Empenho.objects.get(id=empenho)
                    # Verifica se o miltar já possui esse id de empenho relacionado com ele
                    if not militar.empenhos.filter(id=empenho).exists():
                        militar.empenhos.add(empenho_obj)
                        militar.qtd_empenhos += 1
                        militar.empenhos_minutos_atipica += empenho_obj.duracao_em_minutos_atipica
                        militar.empenhos_minutos_tipica += empenho_obj.duracao_em_minutos_tipica
                else:
                    print("Empenho não existe")
        # Verifica se tem algum id de empenho do militar que não está na lista empenhos_conv['empenhos']. Se não estiver deve ser deletado do militar e atualizar a quantidade de empenhos e a soma dos minutos
        for empenho in militar.empenhos.all():
            if str(empenho.id) not in empenhos_conv['empenhos']:
                militar.empenhos.remove(empenho)
                militar.qtd_empenhos -= 1
                militar.empenhos_minutos_atipica -= empenho.duracao_em_minutos_atipica
                militar.empenhos_minutos_tipica -= empenho.duracao_em_minutos_tipica

        # Salva as alterações no banco de dados
        militar.save()
        messages.add_message(request, messages.SUCCESS,
                             'Militar editado com sucesso!')
        return redirect(reverse('registrar_empenho'))
    else:
        return HttpResponse("Você não tem autorização para acessar essa pagina", status=401)


@login_required
def edit_empenho(request, id_empenho):
    return HttpResponse("Editando empenho...")


@login_required
def get_empenhos(request, militar_id):
    militar = Militar.objects.get(id=militar_id)
    print(f"militar: {militar}")
    empenhos = list(militar.empenhos.values())  # militar.empenhos.values()
    print(f"empenhos: {militar.empenhos}")
    # Convert QuerySet to a list of dicts
    return JsonResponse(empenhos, safe=False)


@login_required
def listar_automate_empenho(request):
    if request.method == 'POST':
        print("entrou no post")
        body_unicode = request.body.decode('utf-8')
        all_objects = json.loads(body_unicode)
        print(f"Valor de all_objects: {all_objects}")

        # Inicialmente pega todos os militares
        militares = Militar.objects.all()

        datahorainicial = None
        datahorafinal = None

        # Itera sobre cada critério e aplica filtros ou ordenações
        for criterio in all_objects:
            for key, values in criterio.items():
                if key == 'data_hora_all':
                    datahorainicial = values[0]
                    datahorafinal = values[1]
                    print(datahorainicial)
                    print(datahorafinal)
                elif key == 'pg':
                    filtered_militares = militares.filter(postgrad__in=values)
                    if filtered_militares.exists():
                        militares = filtered_militares
                elif key == 'loc':
                    filtered_militares = militares.filter(local__in=values)
                    if filtered_militares.exists():
                        militares = filtered_militares
                elif key == 'num_emp':
                    if 'max_emp' in values:
                        militares = militares.order_by('-qtd_empenhos')
                    elif 'min_emp' in values:
                        militares = militares.order_by('qtd_empenhos')
                elif key == 'num_hti':
                    if 'max_hti' in values:
                        militares = militares.order_by(
                            '-empenhos_minutos_tipica')
                    elif 'min_hti' in values:
                        militares = militares.order_by(
                            'empenhos_minutos_tipica')
                elif key == 'num_hat':
                    if 'max_hat' in values:
                        militares = militares.order_by(
                            '-empenhos_minutos_atipica')
                    elif 'min_hat' in values:
                        militares = militares.order_by(
                            'empenhos_minutos_atipica')

        # Filtra militares que não possuem indisponibilidade ou empenho conflitante
        if datahorainicial and datahorafinal:
            try:
                datahorainicial = datetime.strptime(
                    datahorainicial, '%d/%m/%Y %H:%M')
                datahorafinal = datetime.strptime(
                    datahorafinal, '%d/%m/%Y %H:%M')
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)

            militares_filtrados = []
            for militar in militares:
                # Verifica conflitos com indisponibilidades
                indisponibilidades = IndispMilitar.objects.filter(
                    militar=militar)
                conflitos_indisponibilidade = any(
                    not verificar_sobreposicao(
                        datahorainicial, datahorafinal, ind.datainicial, ind.datafinal
                    ) for ind in indisponibilidades
                )

                # Verifica conflitos com empenhos
                empenhos = militar.empenhos.all()
                conflitos_empenhos = any(
                    not verificar_sobreposicao(
                        datahorainicial, datahorafinal, emp.datahorainicial, emp.datahorafinal
                    ) for emp in empenhos
                )

                # Adiciona militar à lista se não houver conflitos
                if not conflitos_indisponibilidade and not conflitos_empenhos:
                    militares_filtrados.append(militar)

            militares = Militar.objects.filter(
                pk__in=[m.pk for m in militares_filtrados])

        # Serializa os militares para retornar como JSON
        militares_data = list(militares.values(
            'numero', 'nome', 'postgrad', 'local', 'qtd_empenhos',
            'empenhos_minutos_atipica', 'empenhos_minutos_tipica'
        ))

        return JsonResponse(militares_data, safe=False)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


@login_required
def is_permited_empenho(request, militar_id, empenho_id):

    empenho = Empenho.objects.get(id=empenho_id)
    militar = Militar.objects.get(id=militar_id)
    empenhos_do_militar = militar.empenhos.all()

    # Recupera todas as indisponibilidades do militar usando o militar_id
    indisponibilidades = IndispMilitar.objects.filter(militar=militar)

    # Verifica se a datahorainicial ou datahorafinal do empenho são coencidentes com a datainicial e a datafinal da indisponibilidade
    data_hora_inicial_empenho = empenho.datahorainicial
    data_hora_final_empenho = empenho.datahorafinal
    # TODO Fazer uma verificação da função já criada em teste
    if indisponibilidades:

        for indisponibilidade in indisponibilidades:
            print("Tem indisponibilidades")
            data_hora_inicial_indisponibilidade = indisponibilidade.datainicial
            data_hora_final_indisponibilidade = indisponibilidade.datafinal
            is_permited = verificar_sobreposicao(
                data_hora_inicial_empenho, data_hora_final_empenho, data_hora_inicial_indisponibilidade, data_hora_final_indisponibilidade)
            tipo = indisponibilidade.tipo
            descricao = indisponibilidade.descricao
            obj_indisp = [tipo, descricao, data_hora_inicial_indisponibilidade,
                          data_hora_final_indisponibilidade]
            if not is_permited:
                return JsonResponse({'is_permited': is_permited, 'typepermited': 'indisponibilidade', 'obj_indisp': obj_indisp}, safe=False)

    if emp_militar:

        for emp_militar in empenhos_do_militar:
            print("Tem empenhos")
            datah_init = emp_militar.datahorainicial
            datah_end = emp_militar.datahorafinal
            nome_emp = emp_militar.nome
            is_permited = verificar_sobreposicao(
                data_hora_inicial_empenho, data_hora_final_empenho, datah_init, datah_end)
            obj_emp = [nome_emp, datah_init, datah_end]
            if not is_permited:
                return JsonResponse({'is_permited': is_permited, 'typepermited': 'empenho', 'obj_emp': obj_emp}, safe=False)

    is_permited = True

    return JsonResponse({'is_permited': is_permited, 'typepermited': None}, safe=False)


@login_required
def generate_scale(request):
    return JsonResponse({'message': 'Funcionalidade em desenvolvimento...'})


@login_required
def get_mil_data(request, militar_id):
    militar = Militar.objects.get(id=militar_id)
    # Convert QuerySet to a list of dicts
    empenhos = list(militar.empenhos.values())
    indisponibilidades = list(IndispMilitar.objects.filter(
        militar_id=militar_id))  # Convert QuerySet to a list of dicts
    # Verifica se o militar existe. Se não existir retorna json com o error 'notfound'
    if not militar:
        return JsonResponse({'error': 'notfound'}, safe=False)

    # Recebe os argumento datainicial e datafinal enviado via get pela url no formato ?datainicial=dd/mm/yyyy&datafinal=dd/mm/yyyy
    datainicial = request.GET.get('datainicial', '')
    datafinal = request.GET.get('datafinal', '')

    # Transforma datainicial e datafinal de str para datetime com horas e minutos
    datainicial = datetime.strptime(datainicial, '%d/%m/%Y %H:%M')
    datafinal = datetime.strptime(datafinal, '%d/%m/%Y %H:%M')

    # Se já houver algum empenho para o militar deve retornar um json informado o erro
    if empenhos:

        print(f"empenhos: {empenhos}")

        # Cria uma lista que irá receber os empenhos que coincidem com a datainicial e a datafinal
        empenhos_data = []

        # Percorre todos os empenhos do militar
        for empenho in empenhos:
            # Insere o valor nas variaveis datahorainicial e datahorafinal
            datahorainicial: datetime = empenho['datahorainicial']
            datahorafinal: datetime = empenho['datahorafinal']

            # Converte a datainicial e a datafinal para o formato str no formato '%d/%m/%Y %H:%M' e depois para datetime nesse formato
            datahorainicial = datetime.strptime(
                datahorainicial.strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
            datahorafinal = datetime.strptime(
                datahorafinal.strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')

            datahorainicial = datahorainicial.replace(tzinfo=None)
            datahorafinal = datahorafinal.replace(tzinfo=None)

            print(f"datahorainicial: {datahorainicial}")
            print(f"Tipo de datahorainicial: {type(datahorainicial)}")
            print(f"datahorafinal: {datahorafinal}")
            print(f"Tipo de datahorafinal: {type(datahorafinal)}")
            print(f"datainicial: {datainicial}")
            print(f"Tipo de datainicial: {type(datainicial)}")
            print(f"datafinal: {datafinal}")
            print(f"Tipo de datafinal: {type(datafinal)}")

            # Verifica se a datainicial e a datafinal coincidem com a data do empenho

            if max(datahorainicial, datainicial) < min(datahorafinal, datafinal):
                # Se coincidir adiciona o empenho a lista empenhos_data
                return JsonResponse({'error': 'empfordate', 'empenho': empenho}, safe=False)

    # Se já houver alguma indisponibilidade para o militar deve retornar um json informado o erro
    if indisponibilidades:

        # Percorre todas as indisponibilidades do militar
        for indisponibilidade in indisponibilidades:

            # Converte a datainicial e a datafinal para o formato datetime
            datahorainicial = indisponibilidade.datainicial
            datahorafinal = indisponibilidade.datafinal

            # Converte a datainicial e a datafinal para o formato str no formato '%d/%m/%Y %H:%M' e depois para datetime nesse formato
            datahorainicial = datetime.strptime(
                datahorainicial.strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')
            datahorafinal = datetime.strptime(
                datahorafinal.strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')

            datahorainicial = datahorainicial.replace(tzinfo=None)
            datahorafinal = datahorafinal.replace(tzinfo=None)

            # Verifica se a datainicial e a datafinal coincidem com a data da indisponibilidade

            if datainicial >= datahorainicial and datainicial <= datahorafinal or datafinal >= datahorainicial and datafinal <= datahorafinal or datainicial <= datahorainicial and datafinal >= datahorafinal:
                # Se coincidir adiciona a indisponibilidade a lista indisponibilidades_data
                return JsonResponse({'error': 'indfordate', 'indisponibilidade': model_to_dict(indisponibilidade)}, safe=False)

    # Se não houver nenhum empenho ou indisponibilidade para o militar deve retornar os dados do militar em json
    militar_dict = model_to_dict(militar, exclude=['empenhos'])
    return JsonResponse({'militar': militar_dict}, safe=False)

# Registrar um Empenho para um Militar específico


def add_empenho_to_militar(request, militar_id, empenho_id):
    militar = get_object_or_404(Militar, id=militar_id)
    empenho = get_object_or_404(Empenho, id=empenho_id)

    if request.method == 'POST':
        militar.empenhos.add(empenho)
        # Redirecionar para a página desejada após o registro (ajuste conforme necessário)
        return redirect('nome_da_url_destino')

    # Renderizar o template desejado (ajuste conforme necessário)
    return render(request, 'seu_template.html', {'militar': militar, 'empenho': empenho})

# Registrar um Militar para um Empenho específico


def add_militar_to_empenho(request, empenho_id, militar_id):
    empenho = get_object_or_404(Empenho, id=empenho_id)
    militar = get_object_or_404(Militar, id=militar_id)

    if request.method == 'POST':
        empenho.militares.add(militar)
        # Redirecionar para a página desejada após o registro (ajuste conforme necessário)
        return redirect('nome_da_url_destino')
