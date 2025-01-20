Estou construindo a seguinte função em minha view no django:
Essa função recebe através de um post uma lista de dicionários conforme a seguir:
@login_required
def listar_automate_empenho(request):
    if request.method == 'POST':
        print("entrou no post")
        body_unicode = request.body.decode('utf-8')
        all_objects = json.loads(body_unicode)
        criterios = all_objects  # `all_objects` já é a lista de critérios

Veja um exemplo da lista de dicionarios:
[{'pg': ['3sgt', 'cap']}, {'num_emp': ['max_emp']}]

cada objeto terá uma unica chave e uma lista referente a ela. As possiveis chaves são:
pg
loc
num_emp
num_hti
num_hat

Essas chaves deverão se relacionar a um model de militares conforme a seugir:
class Militar(models.Model):
    numero = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=100)
    postgrad = models.CharField(max_length=10, choices=postgrad_choices, blank=True, null=True)
    local = models.CharField(max_length=10, choices=local_choices, blank=True, null=True)
    qtd_empenhos = models.IntegerField(blank=True, null=True)
    empenhos_minutos_atipica = models.IntegerField(blank=True, null=True)
    empenhos_minutos_tipica = models.IntegerField(blank=True, null=True)
    empenhos = models.ManyToManyField(
        'Empenho', related_name='militares')

    def __str__(self):
        return f"{self.postgrad} {self.nome}"
a chave pg se relaciona a postgrad
a chave loc se relaciona a local
a chave num_emp se relaciona a qtd_empenhos
a chave num_hti se relaciona a empenhos_minutos_tipica
a chave num_hat se relaciona a empenhos_minutos_atipica

como havia falado cada chave recebida terá uma lista, vamos pegar o exemplo passado:
[{'pg': ['3sgt', 'cap']}, {'num_emp': ['max_emp']}]
pg se relaciona com o postgrad do model militar, repare que os valores dentro da lista, o primeiro é: 3sgt e o segund é cap, ou seja, deverá ser feito a busca por todos os militares do banco sendo organizados primeira mente por postgrad=3sgt e segundo por postgrad=cap.  Com essa lista já filtrada entra o proximo objeto num_emp que tem na lista apenas max_emp, que significa que dentro dessa lista que já passou pelo primeiro filtro deve filtrar por ordem descrescente de qtd_empenhos, se fosse ao inves de max_emp, min_emp, então seria em ordem crescente. e sempre assim, primeiro pega-se a lista completa e vai fazendo filtros por objeto recebido. Veja um outor exemplo:

[{'loc': ['acf2', 'sdts2', 'nts']}, {'num_hti': ['max_hti'], 'num_hat': ['min_hat']}]

Nesse caso primeiro se retornaria a lista completa de militares, como o primeiro objeto é loc, teremos que filtrar apenas os militares que possuem esse loc: 'acf2', 'sdts2', 'nts'. A partir dessa lista resultante passaremos para o segundo dict que tem como chave 'num_hti' como 'max_hti' ou seja quero que os militares sejam ordenados em ordem descrescente de empenhos_minutos_tipica, se fosse ai no lugar de 'min_hti' seria em ordem crescente. por fim temos num_hat que se relaciona com empenhos_minutos_atipica e temos na lista o valor min_hat, ou seja, quermos que essa lista já filtrata por loc e ordenada porempenhos_minutos_tipica, agora seja filtrada por empenhos_minutos_atipica ordenada por ordem crescente. se fosse 'max_hat' seria em ordem decrescente. em resumo temos:

O model Militar deve ser filtrado ou ordenado a cada dicionario da lista sendo:
se a chave for loc ou pg ele deve ser filtrado pelos valores existentes na lista
se a chave for num_emp ou num_hti ou num_hat ele deve ser ordenado de acordo o valor dentro da lista, se for max será ordem decrescente se min por ordem crescente. Ao final retornar a lista gerada pelo tratamento no padrão:

@login_required
def listar_automate_empenho(request):
    if request.method == 'POST':
        print("entrou no post")
        body_unicode = request.body.decode('utf-8')
        all_objects = json.loads(body_unicode)
        criterios = all_objects  # `all_objects` já é a lista de critérios
        print(f"Valor de all_objects: {all_objects}")
        
        # LOGICA DE TRATAMENTO CONFORME SOLICITADO

        return JsonResponse(criterios, safe=False)
    return JsonResponse({'error': 'Método não permitido'}, status=405)


# TODO

- REVER O USO DO NOME "PAINEL" NO MODO VISUALIZAÇÃO DE MILITARES E EMPENHOS
- ESCOLHER UM NOME FORTE PARA O SISTEMA
- EDITAR NA OPÇÃO FERIADO E LIBERAÇÃO
- MODO VISULALIZAÇÃO NO "PAINEL"
- SOLICITAR DADOS DOS USUARIOS CONDENSADOS NO NTS
- PRODUÇÃO A PESQUISA OPERACIONAL
- PESQUISA OPERACIONAL - 200 PROBLEMAS RESOLVIDOS... 