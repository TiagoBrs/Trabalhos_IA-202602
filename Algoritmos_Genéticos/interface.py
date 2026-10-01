#Interface gráfica para o Algoritmo Genético aplicado ao problema das N-Rainhas.

#Alunos: Tiago Barbosa e Vitor Kawan

import tkinter
from tkinter import ttk
from tkinter import messagebox

from algoritmo_n_rainha import Algoritmo_Genetico


#Limite de tamanho do tabuleiro para o desenho ser exibido.
LIMITE_DESENHO_TABULEIRO = 15

#Tamanho de cada casa do tabuleiro, em pixels.
TAMANHO_CASA = 50

COR_CASA_CLARA = "#f0d9b5"
COR_CASA_ESCURA = "#b58863"
COR_RAINHA = "#1f1f1f"


class Interface():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Algoritmo Genético - Problema das N-Rainhas")

        self.algoritmo = None
        self.historico = []

        self.construir_painel_parametros()
        self.construir_painel_resultado()
        self.construir_painel_tabuleiro()
        self.construir_painel_tabela()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------

    def construir_painel_parametros(self):
        painel = ttk.LabelFrame(self.janela, text="Parâmetros")
        painel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        rotulo_tabuleiro = ttk.Label(painel, text="Tamanho do tabuleiro (N):")
        rotulo_tabuleiro.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_tabuleiro = ttk.Entry(painel, width=10)
        self.entrada_tabuleiro.insert(0, "8")
        self.entrada_tabuleiro.grid(row=0, column=1, padx=5, pady=5)

        rotulo_populacao = ttk.Label(painel, text="Tamanho da população:")
        rotulo_populacao.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_populacao = ttk.Entry(painel, width=10)
        self.entrada_populacao.insert(0, "50")
        self.entrada_populacao.grid(row=1, column=1, padx=5, pady=5)

        rotulo_mutacao = ttk.Label(painel, text="Taxa de mutação (0 a 1):")
        rotulo_mutacao.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entrada_mutacao = ttk.Entry(painel, width=10)
        self.entrada_mutacao.insert(0, "0.2")
        self.entrada_mutacao.grid(row=2, column=1, padx=5, pady=5)

        rotulo_cruzamento = ttk.Label(painel, text="Taxa de cruzamento (0 a 1):")
        rotulo_cruzamento.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entrada_cruzamento = ttk.Entry(painel, width=10)
        self.entrada_cruzamento.insert(0, "0.9")
        self.entrada_cruzamento.grid(row=3, column=1, padx=5, pady=5)

        rotulo_geracoes = ttk.Label(painel, text="Número de gerações (parada):")
        rotulo_geracoes.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entrada_geracoes = ttk.Entry(painel, width=10)
        self.entrada_geracoes.insert(0, "200")
        self.entrada_geracoes.grid(row=4, column=1, padx=5, pady=5)

        self.botao_executar = ttk.Button(painel, text="Executar", command=self.executar)
        self.botao_executar.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    def construir_painel_resultado(self):
        painel = ttk.LabelFrame(self.janela, text="Resultado")
        painel.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.rotulo_resultado = ttk.Label(painel, text="Nenhuma execução realizada.", wraplength=280, justify="left")
        self.rotulo_resultado.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    def construir_painel_tabuleiro(self):
        self.painel_tabuleiro = ttk.LabelFrame(self.janela, text="Tabuleiro")
        self.painel_tabuleiro.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="n")

        self.area_tabuleiro = tkinter.Canvas(self.painel_tabuleiro, width=1, height=1, highlightthickness=0)
        self.area_tabuleiro.grid(row=0, column=0, padx=5, pady=5)

        self.rotulo_tabuleiro = ttk.Label(self.painel_tabuleiro, text="")
        self.rotulo_tabuleiro.grid(row=1, column=0, padx=5, pady=5)

    def construir_painel_tabela(self):
        painel = ttk.LabelFrame(self.janela, text="Cromossomos por geração")
        painel.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        colunas = ("geracao", "cromossomo", "fitness", "fitness_medio")
        self.tabela = ttk.Treeview(painel, columns=colunas, show="headings", height=14)

        self.tabela.heading("geracao", text="Geração")
        self.tabela.heading("cromossomo", text="Melhor cromossomo")
        self.tabela.heading("fitness", text="Fitness")
        self.tabela.heading("fitness_medio", text="Fitness médio")

        self.tabela.column("geracao", width=80, anchor="center")
        self.tabela.column("cromossomo", width=420, anchor="w")
        self.tabela.column("fitness", width=80, anchor="center")
        self.tabela.column("fitness_medio", width=110, anchor="center")

        self.tabela.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        barra_rolagem = ttk.Scrollbar(painel, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra_rolagem.set)
        barra_rolagem.grid(row=0, column=1, sticky="ns", pady=5)

        self.tabela.bind("<<TreeviewSelect>>", self.ao_selecionar_geracao)

    # ------------------------------------------------------------------
    # Leitura e validação dos parâmetros
    # ------------------------------------------------------------------

    def ler_parametros(self):
        #Converte o texto digitado e valida cada parâmetro. Retorna None se houver erro.
        try:
            tamanho_tabuleiro = int(self.entrada_tabuleiro.get())
            tamanho_populacao = int(self.entrada_populacao.get())
            numero_geracoes = int(self.entrada_geracoes.get())
            taxa_mutacao = float(self.entrada_mutacao.get())
            taxa_cruzamento = float(self.entrada_cruzamento.get())
        except ValueError:
            messagebox.showerror("Parâmetro inválido", "Verifique os valores digitados. Use números inteiros para N, população e gerações, e números decimais para as taxas.")
            return None

        if tamanho_tabuleiro < 4:
            messagebox.showerror("Parâmetro inválido", "O tamanho do tabuleiro deve ser no mínimo 4, pois não existe solução para N = 2 e N = 3.")
            return None

        if tamanho_populacao < 3:
            messagebox.showerror("Parâmetro inválido", "A população deve ter no mínimo 3 indivíduos, pois o torneio sorteia 3 competidores.")
            return None

        if numero_geracoes < 1:
            messagebox.showerror("Parâmetro inválido", "O número de gerações deve ser no mínimo 1.")
            return None

        if taxa_mutacao < 0 or taxa_mutacao > 1:
            messagebox.showerror("Parâmetro inválido", "A taxa de mutação deve estar entre 0 e 1.")
            return None

        if taxa_cruzamento < 0 or taxa_cruzamento > 1:
            messagebox.showerror("Parâmetro inválido", "A taxa de cruzamento deve estar entre 0 e 1.")
            return None

        parametros = {}
        parametros["tamanho_tabuleiro"] = tamanho_tabuleiro
        parametros["tamanho_populacao"] = tamanho_populacao
        parametros["numero_geracoes"] = numero_geracoes
        parametros["taxa_mutacao"] = taxa_mutacao
        parametros["taxa_cruzamento"] = taxa_cruzamento
        return parametros

    # ------------------------------------------------------------------
    # Execução do algoritmo
    # ------------------------------------------------------------------

    def executar(self):
        parametros = self.ler_parametros()
        if parametros is None:
            return

        self.algoritmo = Algoritmo_Genetico(
            parametros["tamanho_populacao"],
            parametros["taxa_mutacao"],
            parametros["taxa_cruzamento"],
            parametros["numero_geracoes"],
            parametros["tamanho_tabuleiro"]
        )

        melhor_solucao = self.algoritmo.executar()
        self.historico = self.algoritmo.historico

        self.mostrar_resultado(melhor_solucao)
        self.preencher_tabela()
        self.atualizar_tabuleiro(melhor_solucao)

    def mostrar_resultado(self, melhor_solucao):
        fitness = self.algoritmo.melhor_fitness

        if fitness == 0:
            situacao = "Solução válida encontrada (nenhuma rainha se ataca)."
        else:
            situacao = "Nenhuma solução perfeita encontrada dentro do número de gerações."

        texto = situacao
        texto = texto + "\n\nMelhor cromossomo: " + self.formatar_cromossomo(melhor_solucao)
        texto = texto + "\nFitness (colisões diagonais): " + str(fitness)
        texto = texto + "\nGerações executadas: " + str(self.algoritmo.numero_geracoes)

        self.rotulo_resultado.configure(text=texto)

    def formatar_cromossomo(self, cromossomo):
        #Monta uma representação em texto do cromossomo, sem usar recursos implícitos do Python.
        texto = "["
        for i in range(len(cromossomo)):
            texto = texto + str(cromossomo[i])
            if i < len(cromossomo) - 1:
                texto = texto + ", "
        texto = texto + "]"
        return texto

    # ------------------------------------------------------------------
    # Tabela de gerações
    # ------------------------------------------------------------------

    def preencher_tabela(self):
        #Limpa a tabela e insere uma linha por geração registrada no histórico.
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        for registro in self.historico:
            geracao = registro["geracao"]
            cromossomo = self.formatar_cromossomo(registro["cromossomo"])
            fitness = registro["fitness"]
            fitness_medio = round(registro["fitness_medio"], 2)

            valores = (geracao, cromossomo, fitness, fitness_medio)
            self.tabela.insert("", "end", values=valores)

    def ao_selecionar_geracao(self, evento):
        #Ao clicar em uma linha da tabela, desenha o tabuleiro daquela geração.
        selecionados = self.tabela.selection()
        if len(selecionados) == 0:
            return

        linha = selecionados[0]
        indice = self.tabela.index(linha)

        if indice >= len(self.historico):
            return

        registro = self.historico[indice]
        self.atualizar_tabuleiro(registro["cromossomo"], registro["geracao"])

    # ------------------------------------------------------------------
    # Desenho do tabuleiro
    # ------------------------------------------------------------------

    def atualizar_tabuleiro(self, cromossomo, geracao=None):
        tamanho = len(cromossomo)

        if tamanho > LIMITE_DESENHO_TABULEIRO:
            self.area_tabuleiro.delete("all")
            self.area_tabuleiro.configure(width=1, height=1)
            texto = "O tabuleiro é exibido somente até N = " + str(LIMITE_DESENHO_TABULEIRO) + "."
            texto = texto + "\nPara N = " + str(tamanho) + ", consulte a tabela de cromossomos."
            self.rotulo_tabuleiro.configure(text=texto)
            return

        self.desenhar_tabuleiro(cromossomo)

        if geracao is None:
            self.rotulo_tabuleiro.configure(text="Melhor solução encontrada")
        else:
            self.rotulo_tabuleiro.configure(text="Melhor cromossomo da geração " + str(geracao))

    def desenhar_tabuleiro(self, cromossomo):
        tamanho = len(cromossomo)
        lado = tamanho * TAMANHO_CASA

        self.area_tabuleiro.delete("all")
        self.area_tabuleiro.configure(width=lado, height=lado)

        #Desenha as casas do tabuleiro, alternando as cores.
        for linha in range(tamanho):
            for coluna in range(tamanho):
                x1 = coluna * TAMANHO_CASA
                y1 = linha * TAMANHO_CASA
                x2 = x1 + TAMANHO_CASA
                y2 = y1 + TAMANHO_CASA

                if (linha + coluna) % 2 == 0:
                    cor = COR_CASA_CLARA
                else:
                    cor = COR_CASA_ESCURA

                self.area_tabuleiro.create_rectangle(x1, y1, x2, y2, fill=cor, outline=cor)

        #Posiciona as rainhas: o índice do cromossomo é a coluna e o valor é a linha.
        for indice in range(tamanho):
            coluna = indice
            linha = cromossomo[indice] - 1

            centro_x = coluna * TAMANHO_CASA + TAMANHO_CASA / 2
            centro_y = linha * TAMANHO_CASA + TAMANHO_CASA / 2

            self.area_tabuleiro.create_text(
                centro_x,
                centro_y,
                text="♛",
                font=("Arial", int(TAMANHO_CASA * 0.6)),
                fill=COR_RAINHA
            )


def main():
    janela = tkinter.Tk()
    interface = Interface(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()