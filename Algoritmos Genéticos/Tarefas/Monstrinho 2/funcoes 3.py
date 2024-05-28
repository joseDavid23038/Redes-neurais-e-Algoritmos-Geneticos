import random


###############################################################################
#                                  População                                  #
###############################################################################


def gene_senha(letras_possiveis):
    """Sorteia uma letra.

    Args:
      letras: letras possíveis de serem sorteadas.

    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_senha(tamanho_min_senha, tamanho_max_senha, letras_possiveis):
    """Cria um candidato para o problema da senha

    Args:
      tamanho_min_senha: inteiro representando o tamanho mínimo da senha.
      tamanho_max_senha: inteiro representando o tamanho máximo da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    tamanho_senha = random.randint(tamanho_min_senha, tamanho_max_senha)
    candidato = []

    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))

    return candidato


def populacao_senha(tamanho_populacao, tamanho_min_senha, tamanho_max_senha, letras_possiveis):
    """Cria população inicial no problema da senha

    Args
      tamanho_populacao: tamanho da população.
      tamanho_min_senha: inteiro representando o tamanho mínimo da senha.
      tamanho_max_senha: inteiro representando o tamanho máximo da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_senha(tamanho_min_senha, tamanho_max_senha, letras_possiveis))

    return populacao


def funcao_objetivo_senha(candidato, senha_verdadeira):
    """Computa a funcao objetivo de um candidato no problema da senha

    Args:
      candidato: um palpite para a senha que você quer descobrir
      senha_verdadeira: a senha que você está tentando descobrir

    """
    distancia = 0

    for letra_candidato, letra_senha in zip(candidato, senha_verdadeira):
        num_letra_candidato = ord(letra_candidato)
        num_letra_senha = ord(letra_senha)
        distancia += abs(num_letra_candidato - num_letra_senha)

    dif_tamanho = abs(len(senha_verdadeira) - len(candidato)) ** 3 #arbitraijajdis oi

    score = distancia + dif_tamanho

    return score


def funcao_objetivo_pop_senha(populacao, senha_verdadeira):
    """Computa a funcao objetivo de uma populaçao no problema da senha.

    Args:
      populacao: lista contendo os individuos do problema
      senha_verdadeira: a senha que você está tentando descobrir

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_senha(individuo, senha_verdadeira))

    return fitness


###############################################################################
#                                   Seleção                                   #
###############################################################################


def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema
      fitness: lista contendo os valores computados da funcao objetivo
      tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados


###############################################################################
#                                  Cruzamento                                 #
###############################################################################


def cruzamento_ponto_simples_variavel(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto simples

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    if random.random() < chance_de_cruzamento:
        if len(mae) < len(pai):
            corte = random.randint(1, len(mae))
        else:
            corte = random.randint(1, len(pai))
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2
    else:
        return pai, mae


###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]


def mutacao_simples_valor(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação simples

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            valores_sorteio = set(valores_possiveis) - set([valor_gene])
            individuo[gene] = random.choice(list(valores_sorteio))


def mutacao_simples_tamanho(populacao, chance_de_mutacao, valores_possiveis, tamanho_min_senha, tamanho_max_senha):
    """Realiza mutação simples

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            tamanho_maior = random.randint(0, 1)
            if tamanho_maior and len(individuo) < tamanho_max_senha:
                individuo.append(gene_senha(valores_possiveis))
            elif len(individuo) > tamanho_min_senha:
                individuo.pop()