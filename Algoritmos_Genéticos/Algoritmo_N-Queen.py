#Problema: Dispor N rainhas em um tabuleiro de xadrez NxN de modo que nenhuma delas se ataquem.

#Alunos: Tiago Barbosa e Vitor Kawan

import random

class Algoritmo_Genetico():
    def __init__(self, tamanho_populacao, taxa_mutacao, taxa_cruzamento, numero_geracoes, tamanho_tabuleiro):
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_cruzamento = taxa_cruzamento
        self.numero_geracoes = numero_geracoes
        self.tamanho_tabuleiro = tamanho_tabuleiro
        self.populacao = []
        self.melhor_solucao = None
        self.melhor_fitness = None
        self.geracao_atual = 0
        self.historico = []

    def inicializar_populacao(self):
        for i in range(self.tamanho_populacao):
            valores = range(1, self.tamanho_tabuleiro + 1)
            cromossomo = random.sample(valores, self.tamanho_tabuleiro)
            self.populacao.append(cromossomo)

    def selecionar(self):
        #Método de Seleção por Torneio.
        torneio = random.sample(self.populacao, k=3)
        melhor = torneio[0]
        melhor_fitness = self.avaliar(melhor)
        for individuo in torneio[1:]:
            fitness_individuo = self.avaliar(individuo)
            if fitness_individuo < melhor_fitness:
                melhor = individuo
                melhor_fitness = fitness_individuo
        return melhor

    def cruzar(self, pai1, pai2):
        #Crossover de um ponto, preservando a permutação dos pais.
        tamanho = len(pai1)
        ponto_corte = tamanho // 2
        filho = []
        for i in range(ponto_corte):
            filho.append(pai1[i])
        for gene in pai2:
            if gene not in filho:
                filho.append(gene)
        return filho

    def mutar(self, individuo):
        #Preserva a permutação do indivíduo, trocando a posição de dois genes aleatórios.
        if random.random() < self.taxa_mutacao:
            tamanho = len(individuo)
            pos1 = random.randint(0, tamanho - 1)
            pos2 = random.randint(0, tamanho - 1)
            valor_temporario = individuo[pos1]
            individuo[pos1] = individuo[pos2]
            individuo[pos2] = valor_temporario
        return individuo

    def avaliar(self, cromossomo):
        #A ideia é avaliar apenas colisões diagonais, pois as colisões entre linhas e colunas são impossíveis por construção do cromossomo.
        tamanho = len(cromossomo)
        f1 = []
        f2 = []
        for i in range(tamanho):
            f1.append(cromossomo[i] - i)
            f2.append((tamanho + 1) - cromossomo[i] - i)
        f1_ordenado = sorted(f1)
        f2_ordenado = sorted(f2)
        t1 = 0
        t2 = 0
        for i in range(1, tamanho):
            if f1_ordenado[i] == f1_ordenado[i - 1]:
                t1 += 1
            if f2_ordenado[i] == f2_ordenado[i - 1]:
                t2 += 1
        fitness_value = t1 + t2
        return fitness_value

    def substituir(self, filhos):
        populacao_ordenada = sorted(self.populacao, key=self.avaliar)
        quantidade_filhos = len(filhos)
        quantidade_sobreviventes = self.tamanho_populacao - quantidade_filhos
        sobreviventes = []
        for i in range(quantidade_sobreviventes):
            sobreviventes.append(populacao_ordenada[i])
        self.populacao = sobreviventes + filhos

    def copiar_cromossomo(self, cromossomo):
        #Cria uma cópia independente, para que alterações posteriores não afetem o original.
        copia = []
        for gene in cromossomo:
            copia.append(gene)
        return copia

    def atualizar_melhor_solucao(self):
        #Guarda o melhor indivíduo já encontrado desde o início da execução.
        for individuo in self.populacao:
            fitness_individuo = self.avaliar(individuo)
            if self.melhor_fitness is None or fitness_individuo < self.melhor_fitness:
                self.melhor_fitness = fitness_individuo
                self.melhor_solucao = self.copiar_cromossomo(individuo)

    def registrar_geracao(self):
        #Guarda no histórico o melhor cromossomo da geração atual e as estatísticas de fitness.
        melhor_da_geracao = self.populacao[0]
        melhor_fitness_geracao = self.avaliar(melhor_da_geracao)
        soma_fitness = 0
        for individuo in self.populacao:
            fitness_individuo = self.avaliar(individuo)
            soma_fitness = soma_fitness + fitness_individuo
            if fitness_individuo < melhor_fitness_geracao:
                melhor_da_geracao = individuo
                melhor_fitness_geracao = fitness_individuo
        media_fitness = soma_fitness / len(self.populacao)

        registro = {}
        registro["geracao"] = self.geracao_atual
        registro["cromossomo"] = self.copiar_cromossomo(melhor_da_geracao)
        registro["fitness"] = melhor_fitness_geracao
        registro["fitness_medio"] = media_fitness
        self.historico.append(registro)

    def executar_geracao(self):
        #Executa uma única geração: seleção, cruzamento, mutação e substituição.
        quantidade_filhos = self.tamanho_populacao - 1
        filhos = []

        for i in range(quantidade_filhos):
            pai1 = self.selecionar()
            pai2 = self.selecionar()

            if random.random() < self.taxa_cruzamento:
                filho = self.cruzar(pai1, pai2)
            else:
                filho = self.copiar_cromossomo(pai1)

            filho = self.mutar(filho)
            filhos.append(filho)

        self.substituir(filhos)
        self.atualizar_melhor_solucao()
        self.geracao_atual = self.geracao_atual + 1
        self.registrar_geracao()

    def executar(self):
        #Laço principal do algoritmo genético. A condição de parada é o número de gerações.
        self.inicializar_populacao()
        self.atualizar_melhor_solucao()
        self.registrar_geracao()

        for geracao in range(self.numero_geracoes):
            self.executar_geracao()

        return self.melhor_solucao