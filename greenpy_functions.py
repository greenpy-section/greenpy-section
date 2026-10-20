# --------------------------------------------------------------- #
# ----------------------- GreenPy Section ----------------------- #
# --------------------------------------------------------------- #

# Programa para cálculo de propriedades geométricas de seções.
# Utiliza o Teorema de Green em sua formulação.

# Durante processo de submissão à revista RENOTE (outubro de 2026):
# Desenvolvido por XXX (Autores mantidos em sigilo) XXX
# XXX (Instituição mantida em sigilo) XXX

# Data da última revisão: 20/10/2026

# --------------------------------------------------------------- #

# importa bibliotecas:
import numpy as np
import math as m
import re
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

# Podem ser importadas durante a execução do código, se necessárias (lazy import):
# scipy, pandas, ipywidgets, IPython.display 

# ----------------------------------- #
# -------- Função principal --------- #
# ----------------------------------- #

def main():
    """
    Função principal que executa o código.

    Ações:
    Solicita informações do usuário via input na tela, recebe dados de entrada,
    executa funções internas, imprime resultados na tela e salva figuras.     

    Obs.: essa função só é chamada quando o código é rodado diretamente por linha de comando.
    Caso o código seja importado como pacote, a função não é chamada.

    Returns
    -------
    None.

    """
    print("""
# --------------------------------------------------------------------- #
# -------------------------- GreenPy Section -------------------------- #
# --------------------------------------------------------------------- #

  Programa para o cálculo de propriedades geométricas de seções planas.

  Durante processo de submissão à revista RENOTE:
  Desenvolvido por XXX (Autores mantidos em sigilo) XXX
  XXX (Instituição mantida em sigilo) XXX

# --------------------------------------------------------------------- #
""")
    
    # --- 1. Entrada de dados --- #
    
    # Escolhe forma de entrada de dados:
    while True:
        try:
            e = int(input(
                "\nQual a forma de entrada de dados?\n"
                "  1 = Ler arquivo de texto (.txt)\n"
                "  2 = Digitar dados manualmente\n\n"
                "Escolha (1 ou 2): "
            ))
            if e not in [1, 2]:
                raise ValueError
            break
        except ValueError:
            print("\nEntrada inválida. Digite apenas 1 ou 2.")

    # Recebe nome do arquivo de dados:
    if e == 1:
        t = "a ser lido é"
    elif e == 2:
        t = "em que os dados serão escritos pode ser"
                      
    nome_do_arquivo = confirmar_valor(
        f'O nome do arquivo {t} "dados_green.txt"?',
        'dados_green.txt',
        'Nome do arquivo?',
        validar_nome=True,
        validar_extensao=True,
        extensao='.txt'
    )
    
    # Recebe nome pasta onde os arquivos serão salvos:
    nome_da_secao = confirmar_valor(
        'O nome da seção a ser analisada é "exemplo"?',
        'exemplo',
        'Nome da seção? Será também o nome da pasta onde os resultados serão salvos.',
        validar_nome=True,
        validar_extensao=False
    )
    
    # Se e=1, realiza testes preliminares no arquivo .txt. Se e=2 ou e=3, recebe dados:
    escolha_dados(e, nome_do_arquivo, pasta_destino = nome_da_secao)
    
    # Recebe unidades:
    unidades = dict_unidades(recebe_unidade())
    
    # --- 2. Leitura e conferência de dados --- #
    
    # Armazena os dados:
    ntot, ncc, nf, ncf, n_sup, c = leitura_de_dados(nome_do_arquivo)

    # Desenha os caminhos para conferência:
    desenha_caminhos(ntot, c, size=10, fator_fontsize=1.2, fator_title=1.4, fator_axis=1, fator_offset=1,
                     texto_caminho=True, color='royalblue', espessura=1, markersize=5, grid=True,
                     pasta_destino = nome_da_secao,
                     outer_fill_color='royalblue', fill_section=True, n_sup=n_sup)

    # Imprime dados na tela para conferência:
    imprime_dados(ntot, n_sup, c, sep_dec=",", sep_milhar=".")

    # Salva dados de entrada conferidos em arquivo .txt
    salva_saida_txt(imprime_dados, ntot, n_sup, c, pasta_destino = nome_da_secao,
                    nome_do_arquivo="dados_lidos.txt", sep_dec=',', sep_milhar='.')
    
    # Salva uma cópia do arquivo original de dados dentro da pasta do exemplo
    copia_arquivo_txt(nome_do_arquivo, pasta_destino = nome_da_secao)
    
    # Validação do usuário
    while True:
        user_check = input('\nOs dados de entrada estão corretos? (s/n) ').strip().lower()
        if user_check == 'n':
            print('\nEncerrando o programa. Revise os dados de entrada e rode novamente.')
            sys.exit()
        elif user_check == 's':
            print('\nOs resultados serão calculados a partir dos dados fornecidos.')
            break
        else:
            print('\nEntrada inválida. Digite "s" para sim ou "n" para não.')
    
    # --- 3. Geração de resultados e figuras --- #
    
    # Imprime resultados na tela
    imprime_resultados(*propriedades_geometricas(c),
                       unidades, sep_dec=',', sep_milhar='.')
    
    # Salva resultados em arquivo .txt
    salva_saida_txt(imprime_resultados, *propriedades_geometricas(c), unidades, pasta_destino = nome_da_secao,
                    nome_do_arquivo="resultados_green.txt", sep_dec=',', sep_milhar='.')
    
    # Salva resultados parciais (separados em contorno e furos) em arquivo .txt
    salva_saida_txt(imprime_resultados_parciais, c, n_sup, unidades, pasta_destino = nome_da_secao,
                    nome_do_arquivo="resultados_parciais.txt", sep_dec=',', sep_milhar='.')   
    
    # Desenha seção limpa
    desenha_caminhos(ntot, c, size=6, texto_caminho=False, markersize=0, grid=False, jupyter=True,
                     section_clean=True, pasta_destino = nome_da_secao, color = 'black', espessura = 0.5,
                     outer_fill_color='gainsboro', fill_section=True, n_sup=n_sup)

    # Desenha seção com eixos
    desenha_caminhos(ntot, c, size=12, texto_caminho=False, markersize=0, eixos_principais=True,
                     fator_eixos_principais=2, pasta_destino = nome_da_secao, color = 'royalblue',
                     outer_fill_color='aliceblue', fill_section=True, n_sup=n_sup)
    
# ----------------------------------- #
# --- Funções de entrada de dados --- #
# ----------------------------------- #

def confirmar_valor(pergunta_confirmacao, valor_padrao, pergunta_alternativa,
                    validar_nome=True, validar_extensao=False, extensao='.txt'):
    """
    Pergunta ao usuário se deseja usar um valor padrão ou informar um novo,
    com validações opcionais de nome e extensão.
    
    Usado para entrada de nomes de arquivos e pastas.

    Parameters
    ----------
    pergunta_confirmacao : str
        Pergunta inicial sobre o uso do valor padrão.
    valor_padrao : str
        Valor a ser utilizado caso o usuário responda 's'.
    pergunta_alternativa : str
        Pergunta exibida caso o usuário opte por informar outro valor.
    validar_nome : bool, optional
        Se True, verifica se o nome informado contém caracteres inválidos.
    validar_extensao : bool, optional
        Se True, exige que o nome termine com a extensão fornecida.
    extensao : str, optional
        Extensão obrigatória (caso validar_extensao=True). Ex: '.txt', '.csv'.

    Returns
    -------
    str
        Valor confirmado ou informado pelo usuário, com validações aplicadas.
    """
    while True:
        resposta = input(f'\n{pergunta_confirmacao} (s/n) ').strip().lower()
        
        if resposta == 's':
            return valor_padrao
        elif resposta == 'n':
            while True:
                valor = input(f'\n{pergunta_alternativa} ').strip()

                if not valor:
                    print('\nO valor não pode estar vazio.')
                    continue

                if validar_nome:
                    if re.search(r'[<>:"/\\|?*]', valor):
                        print('\nNome inválido! Evite caracteres como: < > : " / \\ | ? *')
                        continue

                if validar_extensao and not valor.lower().endswith(extensao.lower()):
                    print(f'\nO nome deve terminar com "{extensao}".')
                    continue

                return valor
        else:
            print('\nEntrada inválida. Por favor, digite apenas "s" para sim ou "n" para não.')

            
def recebe_unidade():
    """
    Solicita ao usuário a unidade de comprimento via input na tela.

    O usuário pode escolher se deseja informar ('s') ou não informar ('n') a unidade de comprimento.
    Caso escolha não informar ('n'), a função retornará uma string vazia ('').
    Caso escolha informar ('s') e depois forneça uma unidade válida, a função retorna a string fornecida em letra minúscula e sem espaços.
    Unidades válidas: 'mm', 'cm', 'dm', 'm', 'dam', 'hm', 'km', 'pol', 'in', 'ft'.

    Returns
    -------
    str
        A unidade de comprimento informada pelo usuário em formato minúsculo e sem espaços,
        ou uma string vazia ('') caso o usuário escolha não informar a unidade.

    Examples
    --------
    Exemplo 1: O usuário fornece a unidade de comprimento 'M':

    >>> recebe_unidade()
    Deseja informar unidade de comprimento? (s/n)
    >>> s
    Qual é a unidade de comprimento utilizada?
    >>> M
    'm'

    Exemplo 2: O usuário opta por não informar unidade:

    >>> recebe_unidade()
    Deseja informar unidade de comprimento? (s/n)
    >>> n
    ''
    """

    # Pergunta se o usuário quer informar unidade
    while True:
        informar_unidade = input(
            '\nDeseja informar unidade de comprimento? (s/n) ')
        if informar_unidade.strip().lower() == 'n':
            # caso o usuário opte por não informar unidade, já retorna '' e encerra a função:
            unidade = ''
            return unidade
        elif informar_unidade.strip().lower() == 's':
            break

    # caso o usuário opte por informar a unidade, pergunta qual é:
    while True:
        unidade = input("Qual é a unidade de comprimento utilizada? ")
        if unidade.lower().strip() in ['mm', 'cm', 'dm', 'm', 'dam', 'hm', 'km', 'pol', 'in', 'ft']:
            break
        else:
            print(
                "Informe uma unidade válida (mm, cm, dm, m, dam, hm, km, pol, in ou ft).")

    return unidade.lower().strip()


def dict_unidades(unidade):
    """
    Transforma uma unidade de comprimento em um dicionário com a unidade nas potências 1, 2, 3 e 4.
    Se a unidade fornecida for uma string vazia (''), o dicionário terá quatro valores vazios.

    Parameters
    ----------
    unidade : str
        Uma unidade de comprimento válida ('mm','cm','dm','m','dam','hm','km','pol','in' ou 'ft'),
        ou uma string vazia ('').

    Raises
    ------
    ValueError
        Se a unidade fornecida for inválida ou não for uma string.

    Returns
    -------
    unidades : dict
        Um dicionário contendo as unidades nas potências 1, 2, 3 e 4.
        Se unidade = '', retorna um dicionário com quatro valores vazios.

    Examples
    --------
    >>> dict_unidades('m')
    {1: 'm', 2: 'm²', 3: 'm³', 4: 'm⁴'}

    >>> dict_unidades('')
    {1: '', 2: '', 3: '', 4: ''}
    """
    if unidade.strip() == '':
        unidades = {1: '', 2: '', 3: '', 4: ''}
    elif unidade.lower().strip() in ['mm', 'cm', 'dm', 'm', 'dam', 'hm', 'km', 'pol', 'in', 'ft']:
        unidades = {}
        unidades[1] = unidade.lower().strip()
        unidades[2] = unidades[1]+"²"
        unidades[3] = unidades[1]+"³"
        unidades[4] = unidades[1]+"⁴"
    else:
        raise ValueError("Unidade inválida.")

    return unidades


def escolha_dados(e, nome_do_arquivo, pasta_destino, jupyter=False):
    """
    Define o modo de entrada dos dados: manual, via arquivo de dados ou via tabela interativa.

    Parameters
    ----------
    e : int
        Tipo de entrada:
        1 - Leitura de arquivo .txt 
        2 - Entrada manual guiada (perguntas via input)
        3 - Tabela interativa (apenas no Jupyter)
    nome_do_arquivo : str
        Nome do arquivo de entrada de dados.
    pasta_destino : str
        Nome da pasta onde os resultados serão salvos.
    jupyter : bool
        Indica se o ambiente é Jupyter (True) ou terminal/script/outros (False).

    Returns
    -------
    None
    """
    if e == 1:
        if teste_leitura_de_dados(nome_do_arquivo):
            print(f"\nOs dados serão lidos do arquivo '{nome_do_arquivo}' do diretório atual.")
            print(f"Os resultados serão salvos na pasta '{pasta_destino}'.")
        else:
            print("\nRevise o arquivo de dados e rode o programa novamente.")
            sys.exit()
    elif e == 2:
        escrita_de_dados(nome_do_arquivo)
    elif e == 3 and jupyter:
        montar_tabela_interativa(nome_do_arquivo)
    else:
        print("Valor de 'e' inválido.")
        if jupyter:
            print("Escolha um número: 1, 2 ou 3.")
        else:
            print("Escolha um número: 1 ou 2.")


def teste_leitura_de_dados(nome_do_arquivo):
    """
    Testa a existência e a formatação básica de um arquivo de dados.

    A formatação de cada linha é considerada válida se pelo menos uma das condições for atendida:
        - Atender ao padrão de dados definido pela função `verifica_padrao`;
        - Estar vazia ou conter apenas espaços em branco;
        - Começar com um comentário (linha iniciando com '#').

    **Obs.** O teste não garante que os dados estejam de acordo com o conteúdo esperado,
    mas apenas verifica se a formatação básica do arquivo está adequada.

    Parameters
    ----------
    nome_do_arquivo : str
        O nome do arquivo .txt a ser lido. O arquivo deve estar salvo no mesmo diretório do
        script. Caso contrário, é necessário fornecer o caminho completo ou relativo.
        O nome padrão é 'dados_green.txt'.

    Returns
    -------
    bool
        Retorna `True` se o arquivo estiver corretamente formatado e `False` caso contrário.
    """
    try:
        with open(nome_do_arquivo, "r") as file:
            teste = file.readlines()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        sys.exit()

    dados_check = True

    for line in teste:
        if line.isspace() or line.lstrip().startswith("#") or verifica_padrao(line.strip()):
            pass
        else:
            dados_check = False

    return dados_check


def leitura_de_dados(nome_do_arquivo):
    """
    Realiza a leitura de dados de um arquivo de texto e retorna os dados processados em uma lista.

    A função tenta abrir e processar um arquivo de dados.
    Primeiramente ela valida a formatação dos dados.
    Depois, organiza as informações em uma lista (dados) e a retorna.
    dados = [ntot, ncc, nf, ncf, n_sup, c]

    Se o arquivo não for encontrado ou os dados não estiverem em conformidade com o formato esperado,
    a função retornará `None` e imprimirá mensagens de erro.

    Parameters
    ----------
    nome_do_arquivo : str
        O nome do arquivo .txt a ser lido. O arquivo deve estar salvo no mesmo diretório do script.
        Caso contrário, é necessário fornecer o caminho completo ou relativo.
        O nome padrão é 'dados_green.txt'.

    Returns
    -------
    dados = [ntot, ncc, nf, ncf, n_sup, c] : list
        Uma lista contendo os seguintes dados, caso a leitura seja bem-sucedida:
        - ntot : int
            Número total de caminhos.
        - ncc : int
            Número de caminhos de contorno.
        - nf : int
            Número de furos.
        - ncf : list of int
            Lista com o número de caminhos de cada furo.
        - n_sup : list of int
            Lista contendo os números dos caminhos finais de contorno e furos.
        - c : dict
            Dicionário com objetos da classe `Caminho`, cada um representando um caminho com suas propriedades, 
            como tipo, coordenadas, ângulos, etc.(para mais detalhes, ver a definição da classe Caminho).
        **Obs.** Retorna `None` caso haja erro durante a leitura ou formatação dos dados.

    Raises
    ------
    ValueError
        Se algum dado não estiver no formato esperado durante o processamento.

    """
    # Tenta abrir e ler arquivo de dados:
    try:
        with open(nome_do_arquivo, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return

    # Salva número de caminhos e índices de caminhos/furos:

    ntot = 0  # inicializa a variável que irá conter o número total de caminhos
    ntot2 = 0  # inicializa a variável que só conta caminhos que estejam com dados de entrada corretos
    n = []     # inicializa lista n provisória contendo paradas a cada linha em branco

    # Laço que conta número de caminhos e em cada linha em branco armazena na lista n o número de caminhos até ali:
    for line in lines:

        # conta linhas que não estão em branco e que não são comentadas
        ntot += count_line(line)

        # se a linha de dados corresponde a algum padrão correto de dados de entrada
        if verifica_padrao(line.strip()):
            ntot2 += 1                        # conta linha

        if ntot > 0 and line.isspace():
            n.append(ntot)

    # caso não tenha linha em branco ao final do arquivo, adiciona ntot final em n
    n.append(ntot)

    # Finaliza a função se o ntot for diferente de ntot2,
    # pois nesse caso há pelo menos uma linha que:
    # não esteja em branco, não seja comentada e não atenda a um padrão correto de entrada de dados
    if ntot != ntot2:
        print("Reveja arquivo de entrada de dados. (1)")
        return

    # Limpa dados repetidos da lista n e armazena na lista n_sup
    # A lista n_sup contém os números dos caminhos finais de contorno e furos
    n_sup = [n[0]]
    for i in range(1, len(n)):
        if n[i] != n[i-1]:
            n_sup.append(n[i])

    ncc = n_sup[0]  # número de caminhos de contorno (ncc)
    # inicializa lista contendo número de caminhos dos furos (ncf)
    ncf = []

    # Loop que salva na lista ncf os números de caminhos de cada furo
    for i in range(len(n_sup)-1):
        ncf.append(n_sup[i+1]-n_sup[i])

    # === Tratamento de dados: === #

    # Lista lines_clean armazena apenas as linhas com dados de entrada válidos já sem espaços antes ou depois
    lines_clean = []
    for line in lines:
        if verifica_padrao(line.strip()):
            lines_clean.append(line.strip())

    # Inicializa dicionário c onde serão armazenados os caminhos
    c = {}

    # Inicializa contadores
    # contador do caminho considerado (número da linha:  1, 2, ...)
    i = 1
    # contador se está no contorno (0) ou em algum furo (1, 2, ...)
    m = 0

    # Trata dados e tenta salvá-los
    for line in lines_clean:

        # Limpa espaços repetidos:
        line = re.sub(r"\s+", " ", line)

        # Divide dados da linha a cada espaço:
        dados_caminho = line.split(" ")
        
        # Limpa números dos dados do caminho (retira separadores de milhar, deixa "." como separador decimal):
        j = 0
        for n in dados_caminho:
            dados_caminho[j] = limpar_numero(n)
            j += 1
            
        # Tenta armazenar dados tipo, xi e yi na classe Caminho
        try:
            c[i] = Caminho(i)

            c[i].tipo = int(float(dados_caminho[0]))
            c[i].xi = float(dados_caminho[1])
            c[i].yi = float(dados_caminho[2])

            if c[i].tipo == 2:
                c[i].angulo_i = float(dados_caminho[3])
                c[i].angulo_f = float(dados_caminho[4])
                c[i].raio = float(dados_caminho[5])

            if c[i].tipo == 3 or c[i].tipo == 4:
                c[i].xp = float(dados_caminho[3])
                c[i].yp = float(dados_caminho[4])

        except ValueError:
            print("Reveja arquivo de entrada de dados. (2)")
            return

        # Armazena coordanadas xf e yf na classe:

        # A condição abaixo relaciona caminhos i-1 e i, portanto precisar iniciar só a partir de i = 2
        if i > 1:
            # Se o caminho i-1 for o último do contorno ou o último do furo:
            if i-1 in n_sup:
                if i-1 == n_sup[0]:
                    c[i-1].xf = c[1].xi
                    c[i-1].yf = c[1].yi
                else:
                    c[i-1].xf = c[n_sup[m]+1].xi
                    c[i-1].yf = c[n_sup[m]+1].yi
                    m += 1

            # caso contrário (se caminho i-1 não for o último do contorno ou furo):
            else:
                c[i-1].xf = c[i].xi
                c[i-1].yf = c[i].yi

            # obs: acima precisamos relacionar i-1 e i ao invés de i e i+1 pois ainda não armazenamos i+1

        # se o caminho i é o primeiro e único (esse caso não é contemplado pela condição anterior pois nunca chega a i = 2):
        # ex: um único círculo de contorno, sem furos
        elif ntot == 1:
            c[1].xf = c[1].xi
            c[1].yf = c[1].yi

        # se o caminho i é o último geral (esse caso não é contemplado nas relações anteriores pois só i-1 recebe novos valores):
        if i == ntot:
            if i == n_sup[0]:                # se o último geral é o último do contorno
                c[i].xf = c[1].xi
                c[i].yf = c[1].yi
            else:                            # se o último geral é o último de algum furo
                c[i].xf = c[n_sup[m]+1].xi
                c[i].yf = c[n_sup[m]+1].yi

        i += 1

    # Fim do laço for para armazenar dados nos dicionários
    
    # Número de furos
    nf = len(ncf)
    
    # Diagnóstico e pequenos ajustes nos arcos
    for caminho in c.values():
        if caminho.tipo == 2:
            caminho.diagnosticar_arco(tol_ang=5.0)
            if caminho.status_arco == 'pequeno_ajuste':
                caminho.consolidar_arco(tol_ang=5.0)
    
    dados = [ntot, ncc, nf, ncf, n_sup, c]

    return(dados)


def count_line(linha):
    """
    Função auxiliar para contagem do número de linhas com dados de um arquivo.   
    Conta a linha apenas se ela não estiver em branco e não for um comentário (#...).

    Parameters
    ----------
    linha : str
        Linha do arquivo de dados a ser analisada.

    Returns
    -------
    int
        Retorna 0 se a linha estiver em branco ou for comentário. Caso contrário retorna 1.
    """
    if linha.lstrip().startswith("#") or linha.isspace():
        return 0
    else:
        return 1


def verifica_padrao(linha):
    """
    Verifica se a linha corresponde a um padrão de entrada válido.

    A verificação é feita utilizando a biblioteca expressões regulares (re), considerando
    o padrão de dados esperado para cada tipo de caminho (segmento de reta, arco ou parábola).

    Parameters
    ----------
    linha : str
        Linha a ser verificada.

    Returns
    -------
    bool
        Retorna True se a linha corresponder a um dos padrões, caso contrário, False.
    """
    # Define os padrões de entrada para segmento, arco e parábola usando expressões regulares
    padrao_segmento = r"^1([.,]0*)?(\s+-?\d{1,3}([.,]?\d{3})*([.,]\d+)?){2}$"
    padrao_arco     = r"^2([.,]0*)?(\s+-?\d{1,3}([.,]?\d{3})*([.,]\d+)?){5}$"
    padrao_parabola = r"^(3|4)([.,]0*)?(\s+-?\d{1,3}([.,]?\d{3})*([.,]\d+)?){4}$"

    # Combina os padrões
    padrao_aceito = f"{padrao_segmento}|{padrao_arco}|{padrao_parabola}"

    # Verifica se a linha corresponde a algum dos padrões definidos
    if re.match(padrao_aceito, linha):
        return True
    else:
        return False


def limpar_numero(n):
    """
    Limpa e formata um número representado como string, removendo separadores de milhar e ajustando o separador decimal.
    
    A função analisa a string de entrada para identificar se há vírgulas ou pontos sendo usados como separadores 
    de milhar ou separadores decimais, e a formata corretamente para garantir que o separador decimal seja sempre um ponto.
    
    Obs.: se n for um número inteiro (sem ponto e sem vírgula), retorna o próprio número.

    Parameters
    ----------
    n : str
        Uma string representando o número, que pode incluir vírgulas e pontos como separadores de milhar e decimal.

    Returns
    -------
    str
        A string com o número formatado, com separador decimal como ponto e sem separadores de milhar.

    Raises
    ------
    ValueError
        Se a string de entrada contiver mais de um separador decimal ou de milhar de forma inconsistente.
    
    Examples
    --------
    >>> limpar_numero(" 9.456.789,34")
    '9456789.34'
    
    >>> limpar_numero("9,456.789,34")
    'ValueError("Erro: Dados inconsistentes nos separadores decimal e de milhar.")'
    """
    # Limpar espaços em branco antes e depois do número
    n = n.strip()
    
    # Contar quantas vírgulas e quantos pontos
    nv = n.count(',')
    np = n.count('.')
    
    # Caso 1: Se tiver apenas um separador (vírgula ou ponto), considera como separador decimal.
    if nv + np == 1:
        # Se for vírgula, considera como separador decimal e substitui por ponto
        return n.replace(',', '.')
    
    # Caso 2: Se tiver mais de um separador (pode ser milhar e decimal)
    elif nv + np > 1:
        
        # Caso 2.1: Se tiver mais de um ponto e mais de uma vírgula, os dados são inválidos
        if nv > 1 and np > 1:
            raise ValueError("Erro: Dados inconsistentes com mais de um separador decimal e de milhar.")
        
        # Caso 2.2: se um dos dois (ponto ou vírgula) não existir, então são só separadores de milhar - remover
        elif nv==0 or np==0:
            n = n.replace('.', '')  # remover separadores de milhar (no caso ".")
            n = n.replace(',', '')  # remover separadores de milhar (no caso ",")
            return n
        
        # Caso 2.3: Se há ambos, analisar o último separador
        else:
            # Vamos verificar qual é o último separador
            if n.rfind(',') > n.rfind('.') and nv == 1:
                # Se a vírgula está depois do ponto e só tem uma vírgula, ela é o separador decimal
                n = n.replace('.', '')  # remover separadores de milhar (nesse caso ".")
                n = n.replace(',', '.') # depois, substituir vírgula por ponto, que passa a ser separador decimal
                return n
            elif n.rfind('.') > n.rfind(',') and np == 1:
                # Se o ponto está depois da vírgula e só tem um ponto, ele é o separador decimal
                n = n.replace(',', '') # remove separadores de milhar (nesse caso ",")
                return n
            else:
                raise ValueError("Erro: Dados inconsistentes nos separadores decimal e de milhar.")
    
    # Caso 3: Número inteiro sem separador algum (nv + np == 0):
    else:
        return n # retorna o próprio número, sem alterações


def escrita_de_dados(nome_do_arquivo):
    """
    Solicita dados do usuário sobre caminhos de contorno e furos e escreve essas informações em um arquivo.

    Parameters
    ----------
    nome_do_arquivo : str
        Nome do arquivo onde os dados serão salvos. Se o arquivo já existir, ele será sobrescrito.

    Returns
    -------
    None.
    """
    while True:
        try:
            ncc = int(float(limpar_numero(input("\nNúmero de caminhos de contorno? "))))
            nf  = int(float(limpar_numero(input("Número de furos? "))))

            if ncc <= 0:
                raise ValueError("O número de caminhos deve ser um inteiro positivo (> 0).")
            if nf < 0:
                raise ValueError("O número de furos deve ser um inteiro não negativo (≥ 0).")

            break

        except ValueError:
            print("\nOs valores devem ser números inteiros válidos. Responda novamente.")
            print("→ O número de caminhos de contorno deve ser um inteiro positivo (> 0).")
            print("→ O número de furos deve ser um inteiro não negativo (≥ 0).\n")   

    ntot = ncc
    ncf = []
    for i in range(nf):
        while True:
            try:
                n = int(float(limpar_numero(input(f"Número de caminhos do furo {i+1}? "))))
                if n <= 0:
                    raise ValueError
                break
            except ValueError:
                print("O número de caminhos deve ser um inteiro positivo. Responda novamente.")
        
        ncf.append(n)
        ntot += n
        
    n_sup = [ncc]
    n_acum = ncc
    for i in range(nf):
        n_acum += ncf[i]
        n_sup.append(n_acum)

    try:
        with open(nome_do_arquivo, 'w') as file:
            m = 1
            for i in range(1, ntot+1):

                if i == 1:
                    print("\n=== Caminhos de Contorno: ===")
                elif i-1 in n_sup:
                    print(f"\n=== Caminhos do Furo {m}: ===")
                    m += 1

                tipo = recebe_tipo(i)
                if tipo == 1:
                    file.write(
                        f"{tipo} {recebe_valor(i,'Coordenada xi')} {recebe_valor(i,'Coordenada yi')}\n")
                elif tipo == 2:
                    file.write(f"{tipo} {recebe_valor(i,'Coordenada xi')} {recebe_valor(i,'Coordenada yi')} "
                               f"{recebe_valor(i,'Ângulo inicial (em graus)')} {recebe_valor(i,'Ângulo final (em graus)')} "
                               f"{recebe_valor(i,'Raio')}\n")
                elif tipo == 3 or tipo == 4:
                    file.write(f"{tipo} {recebe_valor(i,'Coordenada xi')} {recebe_valor(i,'Coordenada yi')} "
                               f"{recebe_valor(i,'Coordenada xp')} {recebe_valor(i,'Coordenada yp')}\n")

                if i in n_sup:
                    file.write("\n")

    except IOError:
        print(
            f"Um erro ocorreu ao tentar escrever o arquivo {nome_do_arquivo}.")


def recebe_tipo(número_do_caminho):
    """
    Função auxiliar para receber o tipo do caminho.
    Solicita ao usuário o tipo de um caminho via input na tela e valida a entrada.
    
    Parameters
    ----------
    número_do_caminho : int
        Número do caminho do qual será informado o tipo.
    
    Returns
    -------
    int
        Tipo do caminho, sendo:
        1 (segmento de reta), 2 (arco), 3 (parábola y=f(x)) ou 4 (parábola x=f(y)).
    """
    # lista de tipos aceitos:
    lista = [1, 2, 3, 4]
    while True:
        try:
            pergunta = (
                f"\nTipo do caminho {número_do_caminho}?"
                "\nOpções:"
                "\n 1 - segmento de reta"
                "\n 2 - arco"
                "\n 3 - parábola y=f(x)"
                "\n 4 - parábola x=f(y)"
            )

            tipo = int(float(limpar_numero(input(pergunta+'\nTipo escolhido:'))))
            if tipo in lista:
                return tipo
            else:
                raise ValueError
        except ValueError:
            print("Tipo inválido. Responda novamente (1, 2, 3 ou 4).")
            pass


def recebe_valor(número_do_caminho, propriedade):
    """
    Função auxiliar para receber o valor numérico de um dado de entrada.
    Solicita ao usuário um valor numérico para uma propriedade de um caminho via input na tela e valida a entrada.

    Parameters
    ----------
    número_do_caminho : int
        Número do caminho do qual será informada a propriedade.
    propriedade : str
        Nome da propriedade a ser solicitada (ex: 'Coordenada xi', 'Raio', ...)
    
    Returns
    -------
    float
        Valor numérico fornecido pelo usuário.
    """
    while True:
        try:
            valor = float(
                limpar_numero(input(f"{propriedade} do caminho {número_do_caminho}? ")))
            return valor
        except ValueError:
            print("Valor inválido. Informe um número real.")
            pass

# ----------------------------------------------------------------- #
# --- Funções de impressão preliminar de dados para conferência --- #
# ----------------------------------------------------------------- #

def imprime_dados(ntot, n_sup, caminhos, sep_dec=',', sep_milhar='.'):
    '''
    Imprime os dados dos caminhos armazenados para conferência.
     
    Os caminhos são classificados como de contorno ou de furos, e cada um 
    é apresentado com suas propriedades geométricas, como tipo, coordenadas 
    e parâmetros adicionais (ex: raio ou coeficientes de parábolas).
     
    Parameters
    ----------
    ntot : int
        Número total de caminhos.
    n_sup : list of int
        Lista contendo os índices dos caminhos finais de cada contorno ou furo.
    caminhos : dict
        Dicionário com os objetos representando os caminhos, indexados de 1 a ntot.
    sep_dec : str, optional
        Separador decimal utilizado na formatação dos números. O padrão é ','.
    sep_milhar : str, optional
        Separador de milhar utilizado na formatação dos números. O padrão é '.'.
     
    Returns
    -------
    None
        A função apenas imprime os dados na tela, sem retornar nenhum valor.
    '''
    # Imprime texto inicial
    print("\nDados de entrada lidos pelo programa:")
    
    
    # Notação mais enxuta dos separadores
    sd = sep_dec
    sm = sep_milhar
    
    # Calcula as áreas parciais de cada grupo
    props_parciais = propriedades_parciais(caminhos, n_sup)

    m = 1
    for i in range(1, ntot+1):

        # Recebe em "caminho" o objeto guardado no índice i do dicionário caminhos
        caminho = caminhos[i]

        # Títulos de contorno ou furo m
        if i == 1:
            print("\n=== Caminhos de contorno: ===")
            area_contorno = props_parciais['area'][0]
            if area_contorno < 0:
                print("\n⚠️  Atenção! A área do contorno resultou negativa, mas deveria ser positiva.")
                print("     → Isso indica que os seus caminhos não foram inseridos no sentido anti-horário.")
            
        elif i-1 in n_sup:
            print(f"\n\n=== Caminhos do furo {m}: ===")
            area_furo = props_parciais['area'][m]
            if area_furo > 0:
                print(f"\n⚠️  Atenção! A área do furo {m} resultou positiva, mas deveria ser negativa.")
                print("     → Isso indica que os seus caminhos não foram inseridos no sentido horário.")
            m += 1

        # Títulos de caminho
        print(f"\n--- Caminho {i}: ---")

        # Dados dos caminhos
        print(f"Tipo: {nome_tipo(caminho.tipo)}")
        print("Coordenadas (x;y):")
        print(
            f"Ponto inicial  = ({format_e(caminho.xi,sd,sm)}; {format_e(caminho.yi,sd,sm)})")
        print(
            f"Ponto final    = ({format_e(caminho.xf,sd,sm)}; {format_e(caminho.yf,sd,sm)})")
        if caminho.tipo == 2:
            print(f"Centro         = ({format_e(round(caminho.xc,7),sd,sm,n=4)}; {format_e(round(caminho.yc,7),sd,sm,n=4)})")
            print(f"Raio           = {format_e(caminho.raio,sd,sm)}")
            # Formatação dinâmica dos ângulos
            casas_i = _casas_decimais(caminho._angulo_i_user)
            casas_f = _casas_decimais(caminho._angulo_f_user)
            #casas = max(casas_i, casas_f)  # maior precisão fornecida pelo usuário
            casas_fmt_i = max(2, casas_i)
            casas_fmt_f = max(2, casas_f)
            print(f"Ângulo inicial = {format_e(round(caminho.angulo_i,casas_fmt_i), sd, sm, m=2)}°")
            print(f"Ângulo final   = {format_e(round(caminho.angulo_f,casas_fmt_f), sd, sm, m=2)}°")
            if caminho.status_arco is not None:
                print(f"Status = {caminho.status_arco}")
                print(f"{caminho.mensagem_arco}")
        elif caminho.tipo == 3 or caminho.tipo == 4:
            print(
                f"Ponto intermediário = ({format_e(caminho.xp,sd,sm)}; {format_e(caminho.yp,sd,sm)})")
            
            # Recebe os coeficientes a, b e c da parábola do objeto caminho
            ai, bi, ci = caminho.coeficientes()
            # Armazena os sinais de b e c
            s_b, s_c = [sinal(bi), sinal(ci)]
            # Armazena os valores de b e c em módulo pois o sinal já foi salvo antes
            bi, ci = [abs(bi), abs(ci)]

            if caminho.tipo == 3:
                print(
                    f"Equação: y = {format_e(ai,sd,'',m=0,n=4)}·x² {s_b} {format_e(bi,sd,'',m=0,n=4)}·x {s_c} {format_e(ci,sd,'',m=0,n=4)}")
            elif caminho.tipo == 4:
                print(
                    f"Equação: x = {format_e(ai,sd,'',m=0,n=4)}·y² {s_b} {format_e(bi,sd,'',m=0,n=4)}·y {s_c} {format_e(ci,sd,'',m=0,n=4)}")

    print("\n\nVerifique se os dados estão corretos!")


def sinal(number):
    '''
    Função auxiliar que retorna o sinal de um número como string.

    Parameters
    ----------
    number : float or int
        Número do qual se deseja obter o sinal.

    Returns
    -------
    str
        '+' se o número for maior ou igual a zero, '-' caso contrário.
    '''
    if number >= 0:
        return '+'
    elif number < 0:
        return '-'


def nome_tipo(i):
    '''
    Função auxiliar que retorna o nome correspondente ao tipo de caminho.
    
    Parameters
    ----------
    i : int
        Código numérico do tipo de caminho.
    
    Returns
    -------
    str
        Nome do tipo de caminho associado ao código.
    '''
    if i == 1:
        return "Segmento de Reta"
    if i == 2:
        return "Arco de Circunferência"
    if i == 3:
        return "Parábola do tipo y = f(x)"
    if i == 4:
        return "Parábola do tipo x = f(y)"
    else:
        return "Caminho inválido"

# ----------------------------------------------------------------------------- #
# --- Funções para avaliação e ajustes nos dados de Arcos de Circunferência --- #
# ----------------------------------------------------------------------------- #

# Funções auxiliares para avaliação de arcos (helpers)

def _clean_num(x, eps=1e-12):
    """Zera resíduos numéricos muito pequenos e cola próximos arredondamentos até 6 casas."""
    if abs(x) < eps:
        return 0.0
    r = round(x,6)
    if abs(x - r) < eps:
        return float(r)
    return x

def _norm360(a_deg: float, eps=1e-12) -> float:
    """Normaliza ângulo para [0, 360); nunca retorna 360 exatamente."""
    a = a_deg % 360.0
    if abs(a) < eps or abs(a - 360.0) < eps:
        return 0.0
    return a

def _short_delta_deg(delta: float) -> float:
    """Ajusta delta (graus) para o menor deslocamento angular em (-180, 180]."""
    d = ((delta + 180.0) % 360.0) - 180.0
    if d == -180.0:
        d = 180.0
    return d

def _ang_diff_deg(a: float, b: float) -> float:
    """Diferença angular mínima (em graus): a - b, trazida para (-180, 180]."""
    d = ((a - b + 180.0) % 360.0) - 180.0
    return 180.0 if d == -180.0 else d

def _close_ang(a: float, b: float, tol_deg: float) -> bool:
    """Compara ângulos absolutos considerando equivalência por múltiplos de 360°."""
    return abs(_ang_diff_deg(a, b)) <= tol_deg

def _close_delta(delta_user: float, delta_ref: float, tol_deg: float) -> bool:
    """Compara deltas angulares considerando equivalência por múltiplos de 360°."""
    return abs(_ang_diff_deg(delta_user, delta_ref)) <= tol_deg

def _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f):
    """
    Centro médio estimado a partir de (xi,yi),(xf,yf), raio e ângulos fornecidos (graus).
    Mesma ideia do critério simples já usado na classe.
    """
    ti = m.radians(ang_i)
    tf = m.radians(ang_f)
    cx1 = xi - raio * m.cos(ti); cy1 = yi - raio * m.sin(ti)
    cx2 = xf - raio * m.cos(tf); cy2 = yf - raio * m.sin(tf)
    return _clean_num((cx1 + cx2) / 2.0), _clean_num((cy1 + cy2) / 2.0)


# Funções principais para avaliação de arcos

def possibilidades_arco(xi, yi, xf, yf, raio, tol_dist=1e-9):
    """
    Retorna possibilidades geométricas para o arco.
    
    Para as informações recebidas (Pi,Pf,raio), se status = 'arco', existem:
        - Duas possibilidades de centro do arco;
        - Para cada possibilidade de centro, duas possibilidades de ângulo final:
            - sentido anti-horário (anf_f > ang_i);
            - sentido horário (anf_f < ang_i).

    Esta função tem por objetivo fazer testes de consistência iniciais, e, se configurada
    a possibilidade de existência do arco, devolver 'candidatos' possíveis a centro e ângulos,
    consistentes com (Pi,Pf,raio) fornecidos.

    Parâmetros:
      xi, yi, xf, yf : coordenadas dos pontos inicial e final
      raio           : raio (>0)
      tol_dist       : tolerância de distância para Pi≈Pf

    Retorno (dict):
      {
        'status': 'arco' | 'circunferencia' | 'inconsistente',
        'mensagem': str,
        'candidatos': [
          {
            'id': 1,
            'xc': ..., 'yc': ...,
            'angulo_i': ...,          # em graus, normalizado em [0,360)
            'angulo_f': ...,          # em graus, maior que angulo_i (CCW - sentido anti-horário)
            'angulo_f_alt': ...,      # em graus, menor que angulo_i (CW - sentido horário)
            'delta_angulo': ...,      # maior que 0 (até 360)
            'delta_angulo_alt': ...,  # menor que 0 (até -360)
            'delta_geom': ...         # |Δθ| geométrico
          },
          {
            'id': 2, ... (outro centro possível)
          }
        ]
        'semicircunferencia': bool 
      }
    """
    tol_dist = abs(tol_dist)

    # 1) raio válido
    if not (isinstance(raio, (int, float)) and m.isfinite(raio) and raio > 0.0):
        return {'status': 'inconsistente', 'mensagem': 'Raio inválido (<=0 ou não finito).', 'candidatos': []}

    # 2) cálculo de d (distância entre Pi e Pf)
    dx, dy = xf - xi, yf - yi
    d = m.hypot(dx, dy)

    # 3) condição geométrica d(Pi,Pf) <= 2R (com tolerância)
    if d > 2.0 * raio + raio/1000.0:
        # distância entre Pi e Pf claramente superior a 2R → inconsistente
        return {
            'status': 'inconsistente',
            'mensagem': (
                'Distância entre Pi e Pf maior que o diâmetro (d(Pi,Pf) > 2R).\n'
                'Revise os dados fornecidos.'
            ),
            'candidatos': []
        }

    elif d > 2.0 * raio + tol_dist:
        # acima de 2R mas sem muita folga  → inconsistente, mas sinalizando proximidade
        return {
            'status': 'inconsistente',
            'mensagem': (
                'Distância entre Pi e Pf ligeiramente maior que o diâmetro (d(Pi,Pf) > 2R).\n'
                'Verifique possíveis erros de arredondamento nos dados fornecidos.'
            ),
            'candidatos': []
        }
    
    # Avalia se é uma semicircunferência (bool, retorna True or False)
    semi = (abs(d - 2.0 * raio) <= tol_dist)
    
    # 4) caso especial: circunferência completa (Pi ~ Pf)
    if d <= tol_dist:
        return {'status': 'circunferencia', 'mensagem': 'Pontos inicial e final coincidem (circunferência completa).', 'candidatos': []}

    # 5) ponto médio
    mx, my = (xi + xf) / 2.0, (yi + yf) / 2.0

    # 6) cálculo de h (distância entre o centro do arco e o ponto médio do segmento Pi-Pf)
    half = 0.5 * d
    rad2 = raio * raio - half * half
    if rad2 < 0 and abs(rad2) <= tol_dist * raio: # quase zero
        rad2 = 0.0
    elif rad2 < 0:
        return {'status': 'inconsistente', 'mensagem': 'Inconsistência numérica: R^2 < (d/2)^2.', 'candidatos': []}
    h = m.sqrt(rad2)

    # 7) vetores unitários
    ux, uy = dx / d, dy / d  # na direção de Pi-Pf 
    nx, ny = -uy, ux         # normal ao segmento Pi-Pf   

    # 8) centros candidatos
    xc1, yc1 = mx + h * nx, my + h * ny
    xc2, yc2 = mx - h * nx, my - h * ny

    # 9) delta geométrico (módulo) — igual para ambos centros
    delta_geom = 180.0 if _clean_num(h) == 0.0 else m.degrees(2.0 * m.atan(d / (2.0 * h)))
    delta_geom_c = _clean_num(delta_geom)

    candidatos = []
    for cid, (xc, yc) in enumerate([(xc1, yc1), (xc2, yc2)], start=1):
        # Ângulos base
        ai = _norm360(m.degrees(m.atan2(yi - yc, xi - xc)))
        af_base = _norm360(m.degrees(m.atan2(yf - yc, xf - xc)))

        # Delta curto (em (-180,180])
        delta_raw = af_base - ai
        delta_curto = _short_delta_deg(delta_raw)

        # Construir ângulos finais CCW (> ai) e CW (< ai), conforme regra:
        if delta_curto > 0:
            af_ccw = ai + delta_curto               # curto CCW (sempre > ai)
            af_cw  = ai - (360.0 - delta_curto)     # longo CW  (sempre < ai)
        else:
            af_ccw = ai + (360.0 + delta_curto)     # longo CCW (sempre > ai)
            af_cw  = ai + delta_curto               # curto CW  (sempre < ai)

        dth_ccw = af_ccw - ai   # > 0
        dth_cw  = af_cw  - ai   # < 0

        # Limpezas
        xc_c, yc_c = _clean_num(xc), _clean_num(yc)
        ai_c       = _clean_num(ai)
        af_ccw_c   = _clean_num(af_ccw)
        af_cw_c    = _clean_num(af_cw)
        dth_ccw_c  = _clean_num(dth_ccw)
        dth_cw_c   = _clean_num(dth_cw)

        candidatos.append({
            'id': cid,
            'xc': xc_c, 'yc': yc_c,
            'angulo_i': ai_c,                 # [0,360)
            'angulo_f': af_ccw_c,             # SEMPRE > angulo_i (CCW)
            'angulo_f_alt': af_cw_c,          # SEMPRE < angulo_i (CW)
            'delta_angulo': dth_ccw_c,        # > 0  e <= 360
            'delta_angulo_alt': dth_cw_c,     # < 0  e >= -360
            'delta_geom': delta_geom_c,       # |Δθ| geométrico
        })

    return {'status': 'arco', 'mensagem': '', 'candidatos': candidatos, 'semicircunferencia': semi}


def avaliar_arco(xi, yi, xf, yf, raio, ang_i, ang_f, tol_ang=5.0):
    """
    Avalia consistência dos dados fornecidos para um arco e, se consistentes,
    escolhe o centro coerente e pode propor pequenos ajustes nos ângulos, se dentro da tolerância.
    
    Preserva o sentido do arco fornecido pelo usuário:
      - se ang_f > ang_i  -> anti-horário (CCW)
      - se ang_f < ang_i  -> horário (CW)

    Retorna dict:
      {
        'status': 'ok' | 'pequeno_ajuste' | 'inconsistente',
        'mensagem': str,
        'xc': float | None, 'yc': float | None,
        'ang_i': float, 'ang_f': float  # graus (ajustados se necessário, preservando sentido e a "banda" do usuário)
      }
    """
    poss = possibilidades_arco(xi, yi, xf, yf, raio)
    status_poss = poss.get('status')
    msg_poss = poss.get('mensagem', '')

    # -------- Circunferência (Pi ≈ Pf) --------
    if status_poss == 'circunferencia':
        tol_circ = 1e-5
        delta_user = ang_f - ang_i
        if abs(abs(delta_user) - 360.0) <= tol_circ:
            # se ângulos final e inicial estão distanciados em 360º, ok. 
            xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
            return {
                'status': 'ok',
                'mensagem': (
                    'Circunferência completa. Dados consistentes.\n'
                    'Confirme no gráfico se corresponde à circunferência pretendida.'
                ),
                'xc': _clean_num(xc), 'yc': _clean_num(yc),
                'ang_i': ang_i, 'ang_f': ang_f
            }
        else:
            xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
            return {
                'status': 'inconsistente',
                'mensagem': (
                    'Para Pi≈Pf (circunferência completa), |ang_f - ang_i| deve ser exatamente 360°.\n'
                    'Revise os dados fornecidos.'
                ),
                'xc': _clean_num(xc), 'yc': _clean_num(yc),
                'ang_i': ang_i, 'ang_f': ang_f
            }

    # -------- Geometria básica inconsistente --------
    if status_poss == 'inconsistente':
        xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
        return {
            'status': 'inconsistente',
            'mensagem': msg_poss,
            'xc': _clean_num(xc), 'yc': _clean_num(yc),
            'ang_i': ang_i, 'ang_f': ang_f
        }
    
    # -------- Arco (2 centros candidatos) --------
    candidatos = poss['candidatos']  # sempre 2 se status=='arco'
    
    delta_u = ang_f - ang_i     # delta angular fornecido pelo usuário

    # -------- Delta angular inconsistente --------
    if abs(delta_u) > 360.0 + 1e-5:
        xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
        return {
            'status': 'inconsistente',
            'mensagem': (
                    'Ângulos inconsistentes. Delta angular fornecido é maior que 360°.\n'
                    'Revise os dados fornecidos.'
                ),
            'xc': _clean_num(xc), 'yc': _clean_num(yc),
            'ang_i': ang_i, 'ang_f': ang_f
        }
    
    # Sentido fornecido pelo usuário (deve ser preservado)
    if ang_f > ang_i:
        sentido_user = 'anti-horario'
    elif ang_f < ang_i:
        sentido_user = 'horario'
    else:
        # ang_f == ang_i não faz sentido (arco de comprimento zero)
        xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
        return {
            'status': 'inconsistente',
            'mensagem': (
                    'Ângulo inicial e final devem ser distintos (indicam o sentido do arco).\n'
                    'Revise os dados fornecidos.'
                ),
            'xc': _clean_num(xc), 'yc': _clean_num(yc),
            'ang_i': ang_i, 'ang_f': ang_f
        }
    
    # Escolha do melhor candidato a centro e ângulos
    melhor = None  # (score, xc, yc, ai_sel, af_sel)
    for cand in candidatos:
        xc, yc = cand['xc'], cand['yc']
        ai_c   = cand['angulo_i']
        af_ccw = cand['angulo_f']       # > ai_c (CCW)
        af_cw  = cand['angulo_f_alt']   # < ai_c (CW)
        d_ccw  = cand['delta_angulo']       # > 0
        d_cw   = cand['delta_angulo_alt']   # < 0

        if sentido_user == 'anti-horario':
            # testes de comparação de dados fornecidos com dados dos candidatos: 
            ok_i = _close_ang(ang_i, ai_c, tol_ang)         # ângulos iniciais 
            ok_f = _close_ang(ang_f, af_ccw, tol_ang)       # ângulos finais
            ok_d = _close_delta(delta_u, d_ccw, 2*tol_ang)  # deltas angulares
            if ok_i and ok_f and ok_d:
                # se passar nos três testes
                score = abs(_ang_diff_deg(ang_i, ai_c)) + abs(_ang_diff_deg(ang_f, af_ccw)) # soma das diferenças, critério de escolha 
                item = (score, xc, yc, ai_c, af_ccw)                                        # item com dados que podem ser selecionados
                if (melhor is None) or (score < melhor[0]):
                    # se ainda não havia candidato escolhido ou se a soma das diferenças foi inferior do que as anteriores, escolhe o item
                    melhor = item
        else:  # 'horario'
            # testes de comparação de dados fornecidos com dados dos candidatos: 
            ok_i = _close_ang(ang_i, ai_c, tol_ang)       # ângulos iniciais 
            ok_f = _close_ang(ang_f, af_cw, tol_ang)      # ângulos finais
            ok_d = _close_delta(delta_u, d_cw, 2*tol_ang) # deltas angulares
            if ok_i and ok_f and ok_d:
                # se passar nos três testes
                score = abs(_ang_diff_deg(ang_i, ai_c)) + abs(_ang_diff_deg(ang_f, af_cw)) # soma das diferenças, critério de escolha
                item = (score, xc, yc, ai_c, af_cw)                                        # item com dados que podem ser selecionados
                if (melhor is None) or (score < melhor[0]):
                    # se ainda não havia candidato escolhido ou se a soma das diferenças for inferior às anteriores, escolhe o item
                    melhor = item
    
    # Se após os testes nenhum item foi selecionado, significa que os dados fornecidos são inconsistentes
    if melhor is None:
        xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
        return {
            'status': 'inconsistente',
            'mensagem': (
                    'Para o raio fornecido, os ângulos estão inconsistentes ou imprecisos.\n'
                    'Revise os dados fornecidos.'
                ),
            'xc': _clean_num(xc), 'yc': _clean_num(yc),
            'ang_i': ang_i, 'ang_f': ang_f
        }

    # ----- Recebe dados da melhor escolha -----
    
    score, xc, yc, ai_sel, af_sel = melhor
    
    # Se dados fornecidos já estão ok (score muito pequeno):
    if score < 1e-10:
        return {
            'status': 'ok',
            'mensagem': (
                    'Dados do arco estão consistentes.\n'
                    'Confirme no gráfico se correspondem ao arco pretendido.'
                ),
            'xc': _clean_num(xc), 'yc': _clean_num(yc),
            'ang_i': ang_i, 'ang_f': ang_f
        }
    
    # Se dados fornecidos estão quase ok mas cabe um pequeno ajuste:
    else:
        # ajustes mínimos necessários (em graus) para colar nos valores coerentes
        # (se testes passaram, essas diferenças já devem ser <= tol_ang)
        ang_i_ajuste = _ang_diff_deg(ai_sel, ang_i)   # alvo - usuário, na faixa (-180,180]
        ang_f_ajuste = _ang_diff_deg(af_sel, ang_f)

        # verificação extra de segurança
        if (abs(ang_i_ajuste) > tol_ang) or (abs(ang_f_ajuste) > tol_ang):
            # Se por algum motivo os ajustes superarem a tolerância, assume-se que os dados são imprecisos 
            return {
                'status': 'inconsistente',
                'mensagem': (
                    'Para o raio fornecido, os ângulos estão inconsistentes ou imprecisos.\n'
                    'Não foi possível realizar ajuste automático.\n'
                    'Revise os dados fornecidos.'
                ),
                'xc': _clean_num(xc), 'yc': _clean_num(yc),
                'ang_i': ang_i, 'ang_f': ang_f
            } 

        # aplica ajustes (preserva banda original do usuário)
        ang_i_out = ang_i + ang_i_ajuste
        ang_f_out = ang_f + ang_f_ajuste
        
        # --- checagem extra para semicircunferência ---
        if poss.get('semicircunferencia'):
            if abs(abs(ang_f_out - ang_i_out) - 180.0) > tol_ang/10.0:
                xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
                return {
                    'status': 'inconsistente',
                    'mensagem': (
                        'Para d(Pi,Pf)≈2R (semicircunferência), |ang_f - ang_i| deve ser aproximadamente 180°.\n'
                        'Revise os dados fornecidos.'
                    ),
                    'xc': _clean_num(xc), 'yc': _clean_num(yc),
                    'ang_i': ang_i, 'ang_f': ang_f
                }
        
        # check de sentido
        if (sentido_user == 'anti-horario' and not (ang_f_out > ang_i_out)) or (sentido_user == 'horario' and not (ang_f_out < ang_i_out)):
            # se por algum motivo os ajustes inverteram o sentido, retoma ângulos inicalmente fornecidos e aponta possível imprecisão
            ang_f_out = ang_f
            ang_i_out = ang_i
            xc, yc = _centro_medio(xi, yi, xf, yf, raio, ang_i, ang_f)
            return {
                'status': 'inconsistente',
                'mensagem': (
                    'Para o raio fornecido, os ângulos estão inconsistentes ou imprecisos.\n'
                    'Não foi possível realizar ajuste automático.\n'
                    'Revise os dados fornecidos.'
                ),
                'xc': _clean_num(xc), 'yc': _clean_num(yc),
                'ang_i': ang_i, 'ang_f': ang_f
            } 
        
        else:
            
            # diferença real dos ajustes aplicados
            dif_i = abs(ang_i_out - ang_i)
            dif_f = abs(ang_f_out - ang_f)

            # limiar para exibir detalhes na tela (ex.: 1e-4 = 4ª casa decimal)
            limiar = 1e-4  

            if dif_i >= limiar or dif_f >= limiar:
                # diferença visível → mostra setas e números
                msg = (
                    "Dados do arco coerentes, porém levemente imprecisos.\n"
                    "Para garantir a consistência geométrica, sugere-se a realização dos ajustes:"
                    f"\nÂngulo inicial: {ang_i:.4f}° → {ang_i_out:.4f}°"
                    f"\nÂngulo final:   {ang_f:.4f}° → {ang_f_out:.4f}°"
                )
                
            else:
                # diferença mínima
                msg = (
                    "Dados do arco coerentes.\n"
                    "Há uma pequena imprecisão, provavelmente insignificante.\n"
                    "Confirme no gráfico se os dados correspondem ao arco pretendido."
                )
                
            return {
                'status': 'pequeno_ajuste',
                'mensagem': msg,
                'xc': _clean_num(xc), 'yc': _clean_num(yc),
                'ang_i': _clean_num(ang_i_out),
                'ang_f': _clean_num(ang_f_out)
            }
    
    
# -------------------------------------- #
# --- Funções para desenhar caminhos --- #
# -------------------------------------- #

def desenha_caminhos(ntot, caminhos, size=10, fator_fontsize=1.2, fator_title=1.4, fator_axis=1, fator_offset=1,
                     texto_caminho=True, color='royalblue', espessura=1, markersize=4, grid=True,
                     jupyter=False, st=False, eixos_principais=False, eixos_ref=False, section_clean=False,
                     fator_eixos_principais=2, savepng=True, savesvg=True, pasta_destino=None,
                     # --- preenchimento com recorte de furos ---
                     fill_section=False,
                     outer_fill_color='gainsboro',
                     fill_alpha_main=0.4,
                     # --- divisão de grupos (contorno + furos) ---
                     n_sup=None):
    """
    Desenha os caminhos (retas, arcos e parábolas) e, se desejado, preenche a seção.

    Regras de preenchimento:
    - Polígonos em sentido CCW (anti-horário) contam como área POSITIVA (preenchida).
    - Polígonos adicionais em sentido CW (horário) contam como área NEGATIVA (recorte/furo, não preenchida).
    - Se um “furo” for fornecido em CCW, ele NÃO será recortado (aparecerá preenchido).
    - Se um “furo” for fornecido em CCW fora do contorno, será interpretado como "ilha" (aparecerá preenchido).

    O preenchimento é feito com um único PathPatch (regra de winding padrão do Matplotlib),
    portanto os “furos” são recortes transparentes quando orientados em CW.
    
    Parameters
    ----------
    ntot : int
        Número total de caminhos a serem desenhados.
    caminhos : dict[int, Caminho]
        Dicionário contendo todos os caminhos, onde a chave é o número do caminho e o valor é o objeto do caminho.
        Ex.: caminhos[2] é o objeto da classe Caminho que representa o caminho de número 2.
    size : int, opcional
        Tamanho da figura (padrão é 10).
    fator_fontsize : float, opcional
        Fator para o tamanho da fonte (padrão é 1.2).
    fator_title : float, opcional
        Fator para o tamanho da fonte do título (padrão é 1.4).
    fator_axis : float, opcional
        Fator para o tamanho da fonte dos eixos (padrão é 1).
    fator_offset : float, opcional
        Fator de afastamento dos identificadores dos caminhos (padrão é 1).
    texto_caminho : bool, opcional
        Se True, exibe a identificação de cada caminho (Ci) no desenho (padrão é True).
    color : tuple of float, opcional
        Cor dos caminhos no formato RGB normalizado (padrão é (100/255, 100/255, 240/255)).
    espessura : int, opcional
        Espessura das linhas dos caminhos (padrão é 1).
    markersize : int, opcional
        Tamanho dos pontos (padrão é 4, colocar 0 para não mostrar pontos).
    grid : bool, opcional
        Se True, exibe a grade no gráfico (padrão é True).
    jupyter : bool, opcional
        Se True, exibe o gráfico diretamente na tela do Jupyter Notebook (padrão é False).
    st : bool, opcional
        Se True, prepara figura para aparecer no streamlit (padrão é False).
    savepng : bool, opcional
        Se True, salva figura em formato .png (padrão é True).
    savesvg : bool, opcional
        Se True, salva figura vetorizada em formato .svg (padrão é False).
    eixos_ref : bool, opcional
        Se True, grafica eixos de referÊncia em linha tracejada (padrão é False).
    eixos_principais : bool, opcional
        Se True, altera padrão de graficação para aparecer eixos principais, entre outras questões (padrão é False).
    section_clean : bool, opcional
        Se True, altera padrão de graficação para deixar desenho mais limpo e com o mínimo de informações (padrão é False).
    fator_eixos_principais : float, opcional
        Fator de comprimento do desenho dos eixos principais (padrão é 2).
    pasta_destino : str or None
        Pasta base onde a subpasta 'figuras' será criada para salvar as figuras geradas. Se None, usa o diretório atual.
    fill_section : bool
        Se True, preenche a figura formada pelos caminhos e com recorte de furos.
    outer_fill_color : tuple|str
        Cor de preenchimento da figura.
    fill_alpha_main : float
        Opacidade do preenchimento da figura delimitada pelo contorno externo [0..1].  
    n_sup : list[int] | None
        Lista dos "números do último caminho" de cada grupo na ordem:
        - n_sup[0] = número do último caminho do contorno externo
        - n_sup[1] = último caminho do furo 1
        - n_sup[2] = último caminho do furo 2
        Se None, assume um único contorno (sem furos).
    
    Returns
    -------
    None
        A função não retorna nenhum valor, apenas exibe o gráfico e salva os arquivos no formato .jpeg e .svg.
    """

    # --- figura/eixos base ---
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # grade por baixo de tudo
    if grid:
        ax.grid(True, color="lightgray", linewidth=0.5) 
        ax.set_axisbelow(True)

    # --- CAMADAS/Z-ORDER ---
    Z_FILL_MAIN        = 1   # patch principal (com furos recortados, se houver)
    Z_PATHS            = 2   # linhas por cima do fill
    Z_POINTS           = 3   # marcadores
    Z_LABELS           = 4   # rótulos "Ci"
    Z_AXES_REF         = 0   # eixos de referência
    Z_AXES_C           = 5   # eixos centrais
    Z_EIXOS_PRINCIPAIS = 6   # eixos principais u,v
    Z_CG               = 7   # centróide

    # --- cálculo do offset de texto (para rótulos Ci) ---
    fontsize = fator_fontsize * size
    offset_dx, offset_dy = calculate_text_offsets(fig, ax, "C01", fontsize)  # tua função utilitária
    d_offset = max(offset_dx, offset_dy)

    # --- preparação para grupos (contorno/furos) ---
    if n_sup is None or len(n_sup) == 0:
        grupos_sup = [ntot]
    else:
        grupos_sup = list(n_sup)

    # inicializa buffers de pontos para o grupo corrente
    contorno_x, contorno_y = [], []
    idx_grupo = 0  # 0 = contorno externo; 1.. = furos (ou outros contornos, conforme o usuário)

    # inicializa polígonos discretizados: polys[0]=contorno externo; polys[1:]=furos/ilhas
    polys = [[] for _ in range(len(grupos_sup))]

    # --- loop principal: desenha e acumula pontos ---
    for i in range(1, ntot + 1):
        caminho = caminhos[i]
        markersize_relativo = 0.1 * markersize * size

        # ====== Desenho / discretização ======
        if caminho.tipo == 1:
            # segmento de reta
            x_seg = np.linspace(caminho.xi, caminho.xf, 2)
            y_seg = np.linspace(caminho.yi, caminho.yf, 2)
            ax.plot([caminho.xi, caminho.xf], [caminho.yi, caminho.yf],
                    linestyle='-', color=color, linewidth=espessura, zorder=Z_PATHS)
            if markersize > 0:
                ax.plot([caminho.xi, caminho.xf], [caminho.yi, caminho.yf],
                        linestyle='None', marker='o', color=color,
                        markersize=markersize_relativo, zorder=Z_POINTS)
            contorno_x.extend(x_seg.tolist())
            contorno_y.extend(y_seg.tolist())

        elif caminho.tipo == 2:
            # arco
            xc, yc = caminho.xc, caminho.yc
            theta_i, theta_f = caminho.angulo_i_rad, caminho.angulo_f_rad
            raio = caminho.raio
            num_segmentos = 100
            theta = np.linspace(theta_i, theta_f, num_segmentos)
            x_arco = xc + raio * np.cos(theta)
            y_arco = yc + raio * np.sin(theta)
            ax.plot(x_arco, y_arco, color=color, linewidth=espessura, zorder=Z_PATHS)
            if markersize > 0:
                ax.plot([caminho.xi, caminho.xf], [caminho.yi, caminho.yf],
                        linestyle='None', marker='o', color=color,
                        markersize=markersize_relativo, zorder=Z_POINTS)
            contorno_x.extend(x_arco.tolist())
            contorno_y.extend(y_arco.tolist())

        elif caminho.tipo == 3:
            # parábola y = f(x)
            a, b, ccoef = caminho.coeficientes()
            num_segmentos = 100
            x = np.linspace(caminho.xi, caminho.xf, num_segmentos)
            y = a * x**2 + b * x + ccoef
            ax.plot(x, y, color=color, linewidth=espessura, zorder=Z_PATHS)
            if markersize > 0:
                ax.plot([caminho.xi, caminho.xf], [caminho.yi, caminho.yf],
                        linestyle='None', marker='o', color=color,
                        markersize=markersize_relativo, zorder=Z_POINTS)
            contorno_x.extend(x.tolist())
            contorno_y.extend(y.tolist())

        elif caminho.tipo == 4:
            # parábola x = f(y)
            a, b, ccoef = caminho.coeficientes()
            num_segmentos = 100
            y = np.linspace(caminho.yi, caminho.yf, num_segmentos)
            x = a * y**2 + b * y + ccoef
            ax.plot(x, y, color=color, linewidth=espessura, zorder=Z_PATHS)
            if markersize > 0:
                ax.plot([caminho.xi, caminho.xf], [caminho.yi, caminho.yf],
                        linestyle='None', marker='o', color=color,
                        markersize=markersize_relativo, zorder=Z_POINTS)
            contorno_x.extend(x.tolist())
            contorno_y.extend(y.tolist())

        # ====== Rótulo Ci ======
        dist = m.sqrt((caminho.xf - caminho.xi)**2 + (caminho.yf - caminho.yi)**2)
        if dist != 0:
            dx = (caminho.xf - caminho.xi) / dist
            dy = (caminho.yf - caminho.yi) / dist
            perp_dx, perp_dy = -dy, dx
        else:
            perp_dx = perp_dy = 0

        offset_x = (d_offset * perp_dx) * fator_offset
        offset_y = (d_offset * perp_dy) * fator_offset

        if caminho.tipo == 1:
            xt = (caminho.xi + caminho.xf) / 2
            yt = (caminho.yi + caminho.yf) / 2
        elif caminho.tipo == 2:
            if round(abs(caminho.angulo_f - caminho.angulo_i), 1) == 360:
                xt, yt = caminho.xc, caminho.yc
                offset_x = offset_y = 0
            else:
                theta_t = (caminho.angulo_i_rad + caminho.angulo_f_rad) / 2
                xt = caminho.xc + caminho.raio * m.cos(theta_t)
                yt = caminho.yc + caminho.raio * m.sin(theta_t)
        elif caminho.tipo == 3:
            a, b, ccoef = caminho.coeficientes()
            xt = (caminho.xi + caminho.xf) / 2
            yt = a * xt**2 + b * xt + ccoef
        elif caminho.tipo == 4:
            a, b, ccoef = caminho.coeficientes()
            yt = (caminho.yi + caminho.yf) / 2
            xt = a * yt**2 + b * yt + ccoef

        if texto_caminho:
            ax.annotate(f"C{i}", (xt, yt), xytext=(offset_x, offset_y),
                        textcoords='offset points', ha='center', va='center',
                        fontsize=fontsize, zorder=Z_LABELS)

        # ====== Fechamento do grupo ======
        if i == grupos_sup[idx_grupo]:
            if len(contorno_x) >= 3:
                polys[idx_grupo] = list(zip(contorno_x, contorno_y))
            contorno_x, contorno_y = [], []
            if idx_grupo < len(grupos_sup) - 1:
                idx_grupo += 1

    # === Preenchimento (um único Path; furos = CW; ilhas = CCW) ===
    if fill_section and len(polys) > 0 and len(polys[0]) >= 3:
        # 'verts' e 'codes' vão armazenar, respectivamente:
        # - todos os vértices (x, y) de todos os polígonos/grupos
        # - os comandos do tipo "começar aqui", "ligar até ali", "fechar polígono"
        verts, codes = [], []

        # percorre cada polígono acumulado em 'polys'
        # (polys[0] = contorno externo, polys[1:] = furos ou ilhas)
        for poly in polys:
            if not poly:
                # se não há pontos (lista vazia), ignora
                continue

            # começa um novo subcaminho no primeiro ponto do polígono
            verts.append(poly[0])
            codes.append(Path.MOVETO)

            # conecta todos os pontos seguintes com segmentos de reta
            for v in poly[1:]:
                verts.append(v)
                codes.append(Path.LINETO)

            # fecha o polígono: liga o último ponto de volta ao primeiro
            # Obs.: CLOSEPOLY exige receber um vértice, mas ele é "ignorado".
            # Por convenção, repete-se o primeiro ponto.
            verts.append(poly[0])
            codes.append(Path.CLOSEPOLY)

        # cria o objeto Path com todos os subcaminhos (contorno + furos/ilhas)
        path = Path(verts, codes)

        # cria um patch (área preenchida) a partir do Path
        patch = PathPatch(path,
                          facecolor=outer_fill_color,  # cor de preenchimento
                          edgecolor='none',            # sem contorno extra
                          alpha=fill_alpha_main,       # transparência
                          zorder=Z_FILL_MAIN)          # ordem de sobreposição

        # adiciona o patch ao gráfico
        ax.add_patch(patch)


    # --- ajustes de janela ---
    ax.relim(); ax.autoscale_view()
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    margin = 0.1
    x_range = x_max - x_min
    y_range = y_max - y_min
    ax.set_xlim(x_min - margin * x_range, x_max + margin * x_range)
    ax.set_ylim(y_min - margin * y_range, y_max + margin * y_range)

    # tamanho proporcional à janela
    mod_range = m.sqrt(max(x_range, 1e-12)**2 + max(y_range, 1e-12)**2)
    x_janela = x_range / mod_range if mod_range != 0 else 1.0
    y_janela = y_range / mod_range if mod_range != 0 else 1.0
    fig.set_size_inches((x_janela * size, y_janela * size))

    # títulos/labels
    ax.set_xlabel('X', fontsize=fator_axis * size)
    ax.set_ylabel('Y', fontsize=fator_axis * size)
    ax.set_title('Caminhos', fontsize=fator_title * size, pad=0.8 * fator_title * size)
    ax.tick_params(axis='both', which='major', labelsize=fator_axis * size)

    # eixos de referência
    if eixos_ref:
        ax.axhline(0, color='gray', linestyle='--', linewidth=1, label='x,y (referência)', zorder=Z_AXES_REF)
        ax.axvline(0, color='gray', linestyle='--', linewidth=1, zorder=Z_AXES_REF)

    # eixos principais (usa propriedades_geometricas)
    if eixos_principais:
        props = propriedades_geometricas(caminhos)
        ax.axis('off')

        x_c, y_c = props[3], props[4]
        ax.axhline(y_c, color='black', linestyle='--', linewidth=1, label='xc,yc (centrais)', zorder=Z_AXES_C)
        ax.axvline(x_c, color='black', linestyle='--', linewidth=1, zorder=Z_AXES_C)

        theta = np.radians(props[12])
        length = (x_max - x_min) * fator_eixos_principais

        u_x = [x_c - length * np.cos(theta), x_c + length * np.cos(theta)]
        u_y = [y_c - length * np.sin(theta), y_c + length * np.sin(theta)]
        v_x = [x_c - length * np.sin(theta), x_c + length * np.sin(theta)]
        v_y = [y_c + length * np.cos(theta), y_c - length * np.cos(theta)]

        ax.plot(u_x, u_y, color='red', linestyle='-.', linewidth=1, label='u,v (principais)', zorder=Z_EIXOS_PRINCIPAIS)
        ax.plot(v_x, v_y, color='red', linestyle='-.', linewidth=1, zorder=Z_EIXOS_PRINCIPAIS)
        ax.scatter(x_c, y_c, s=20, color='black', label='CG', zorder=Z_CG)

        ax.set_title('Eixos', fontsize=fator_title * size, pad=0.8 * fator_title * size)
        ax.legend(bbox_to_anchor=(1, 1), title='Legenda:')
        
    # configurações para o desenho da seção limpa
    if section_clean:
        ax.axis('off')
        ax.set_title(None)

    fig.tight_layout()

    # salvamento
    if st:
        # --- DPI adaptativo para evitar blur em figuras "esbeltas" ---
        # Usa o tamanho em polegadas já definido (respeitando a proporção da seção)
        w_in, h_in = fig.get_size_inches()

        # Definimos metas de pixels para curto/longo lado.
        # Ajuste se quiser arquivos menores/maiores.
        TARGET_LONG_PX  = 1600   # pixels no lado maior
        TARGET_SHORT_PX = 900    # pixels no lado menor

        long_in  = max(w_in, h_in)
        short_in = min(w_in, h_in)

        # DPI necessário para bater as metas nos dois eixos
        dpi_long  = TARGET_LONG_PX  / max(long_in, 1e-6)
        dpi_short = TARGET_SHORT_PX / max(short_in, 1e-6)

        dpi_adapt = max(dpi_long, dpi_short)

        # Limites práticos de DPI (evita arquivos gigantes ou muito leves)
        dpi_adapt = float(np.clip(dpi_adapt, 140, 360))

        # Salva PNG com DPI adaptativo (nítido mesmo em geometrias altas/estreitas)
        fig.savefig("temp_fig.png", dpi=dpi_adapt, bbox_inches='tight')

        # Também salva SVG para download vetorial no Streamlit
        # (não altera nada fora do modo st=True)
        fig.savefig("temp_fig.svg", format='svg', bbox_inches='tight')

    else:
        if savepng or savesvg:
            pasta_figuras = os.path.join(pasta_destino, 'figuras') if pasta_destino else 'figuras'
            os.makedirs(pasta_figuras, exist_ok=True)

            if section_clean:
                nome_da_figura = 'secao'
            elif eixos_principais:
                nome_da_figura = 'eixos_principais'
            else:
                nome_da_figura = 'caminhos'

            if savesvg:
                fig.savefig(os.path.join(pasta_figuras, nome_da_figura + '.svg'),
                            format='svg', bbox_inches='tight')
            if savepng:
                fig.savefig(os.path.join(pasta_figuras, nome_da_figura + '.png'),
                            format='png', bbox_inches='tight')

    if jupyter:
        print()
        plt.show()
        
def choose_color(r, g, b):
    '''
    Converte valores RGB de 0 a 255 para o formato normalizado do matplotlib.

    Parameters
    ----------
    r : int
        Valor da componente vermelha (0–255).
    g : int
        Valor da componente verde (0–255).
    b : int
        Valor da componente azul (0–255).

    Returns
    -------
    tuple of float
        Tupla contendo os valores normalizados (r, g, b), cada um no intervalo [0, 1],
        representados como floats.
    '''
    r = int(float(r))
    g = int(float(g))
    b = int(float(b))
    return (r / 255, g / 255, b / 255)

def calculate_text_offsets(fig, ax, text, fontsize):
    '''
    Função auxiliar para calcular dinamicamente o valor de offsets com base no tamanho de texto.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Objeto da figura onde o texto será desenhado.
    ax : matplotlib.axes.Axes
        Eixo associado ao texto.
    text : str
        Texto cujo tamanho será avaliado.
    fontsize : int 
        Tamanho da fonte em pontos.

    Returns
    -------
    tuple of float
        Metade da largura e da altura do texto em pixels (offset_x, offset_y), 
        representados como floats.
    '''
    # Cria um objeto de texto temporário para calcular o tamanho do texto
    temp_text = ax.text(0, 0, text, fontsize=fontsize)
    renderer = fig.canvas.get_renderer()
    bbox = temp_text.get_window_extent(renderer=renderer)
    temp_text.remove()
    width, height = bbox.width, bbox.height

    return width / 2, height / 2

# ---------------------------------------- #
# --- Funções para imprimir resultados --- #
# ---------------------------------------- #

def format_n(number, sep_dec=',', sep_milhar='.'):
    """
    Formata um número para exibição, ajustando o número de casas decimais, 
    separador decimal e separador de milhar conforme especificado.

    Regras:
    - Usa notação científica para valores muito pequenos ou muito grandes.
    - Adapta dinamicamente o número de casas decimais conforme a magnitude.
    - Remove zeros à direita após a 2ª casa decimal, mantendo no mínimo 2 casas.
    - Aplica separador de milhar quando adequado.
    """
    if round(number, 15) == 0:
        return "0.00".replace(".", sep_dec)

    abs_n = abs(number)

    # Notação científica
    if abs_n < 0.0001 or abs_n > 999999999.99:
        return f"{number:.4e}".replace("e", "E").replace(".", sep_dec)

    # Faixas com precisão variável
    if abs_n < 0.001:
        s = f"{number:.7f}".replace(".", sep_dec)
    elif abs_n < 0.01:
        s = f"{number:.6f}".replace(".", sep_dec)
    elif abs_n < 0.1:
        s = f"{number:.5f}".replace(".", sep_dec)
    elif abs_n < 1:
        s = f"{number:.4f}".replace(".", sep_dec)
    elif abs_n < 10:
        s = f"{number:.3f}".replace(".", sep_dec)        
    elif abs_n < 1000:
        s = f"{number:.2f}".replace(".", sep_dec)
        return s
    else:  # >= 1000
        s = f"{number:,.2f}".replace(",", "M").replace(".", sep_dec).replace("M", sep_milhar)
        return s

    # Garantir no mínimo 2 casas, removendo zeros após a segunda
    if sep_dec in s:
        parte_int, parte_dec = s.split(sep_dec)
        parte_dec = parte_dec[:2] + parte_dec[2:].rstrip('0')
        s = parte_int + sep_dec + parte_dec

    return s

def format_e(number, sep_dec=',', sep_milhar='.', m=2, n=None):
    """
    Formata um número de entrada já interpretado para exibição na tela ou impressão, 
    ajustando o número de casas decimais e separadores decimal e de milhar.
    
    Regras:
    - Nunca usa notação científica;
    - Remove zeros à direita após a mª casa decimal, mantendo no mínimo m casas;
    - Adiciona separadores de milhar se necessário;
    - Se 'n' for fornecido, aplica arredondamento dinâmico antes de formatar.

    Parameters
    ----------
    number : int | float
        Valor numérico a formatar (já interpretado pelo Python).
    sep_dec : str, opcional
        Separador decimal da saída (padrão ',').
    sep_milhar : str, opcional
        Separador de milhar da saída (padrão '.').
    m : int 
        Número mínimo de casas decimais após a vírgula (padrão = 2).
    n : int, opcional
        Se definido, aplica arredondamento dinâmico mantendo pelo menos n dígitos significativos.
        Esse arredondamento é feito com a função 'arred_din', que também zera valores |x| < 1e-16.

    Returns
    -------
    str
        Número em ponto fixo, com ao menos m casas decimais
        e sem zeros desnecessários após a mª casa.
    """
    
    m = max(0, m)  # força m ≥ 0

    # 1. Aplica arredondamento dinâmico se n for fornecido
    x = arred_din(number, n) if n is not None else float(number)

    # 2. Sinal e valor absoluto
    sign = '-' if x < 0 else ''
    ax = abs(x)

    # 3. Determina casas confiáveis para ponto fixo
    if ax == 0:
        casas_seguras = m
    else:
        digitos_int = len(str(int(ax)))  # nº de dígitos antes da vírgula
        casas_seguras = max(m, 15 - digitos_int)  # respeita limite de dígitos seguro de ponto fixo

    # 4. Converte para string em ponto fixo (sem notação científica)
    ax = round(ax, casas_seguras)
    s = f"{ax:.{casas_seguras}f}"

    # 5. Divide parte inteira e decimal
    if '.' in s:
        int_part, dec_part = s.split('.', 1)
    else:
        int_part, dec_part = s, ''
    
    # 6. Limpa zeros à direita da parte decimal
    dec = dec_part.rstrip('0')

    # 7. Aplica separador de milhar, exceto se m == 0 e não houver decimais
    #    Essa condição evita um número com sep. de milhar e sem sep. decimal
    #    Objetivo: evitar erros de leitura (ex.: achar que 1.000 é 1)
    usar_milhar = not (m == 0 and dec == '')
    if usar_milhar:
        rev = int_part[::-1]
        grupos = [rev[i:i+3] for i in range(0, len(rev), 3)]
        int_fmt = sep_milhar.join(grupos)[::-1]
    else:
        int_fmt = int_part

    # 8. Ajusta parte decimal final (mínimo m casas)
    if dec:
        dec_final = dec if len(dec) >= m else dec.ljust(m, '0')
    else:
        dec_final = '0' * m if m > 0 else ''

    # 9. Concatena e retorna
    if dec_final:
        return f"{sign}{int_fmt}{sep_dec}{dec_final}"
    else:
        return f"{sign}{int_fmt}"
    
def arred_din(numero, n=4):
    """
    Arredonda dinamicamente conforme regras:
      - |numero| < 1: mantém n algarismos significativos após os zeros da vírgula
      - |numero| ≥ 1: sempre n casas decimais
      - |numero| < 1e-16: força 0.0 (ruído numérico abaixo da precisão de float)
    """
    if n < 1:
        raise ValueError("n deve ser um inteiro ≥ 1")

    x = float(numero)
    ax = abs(x)

    # tolerância mínima para evitar ruído de float
    if ax < 1e-16:
        return 0.0

    if ax < 1.0:
        zeros = m.ceil(-m.log10(ax)) - 1
        casas = zeros + n
    else:
        casas = n

    return round(x, casas)

def _casas_decimais(val: float) -> int:
    # função auxiliar para determinar a quantidade de casas decimais de um número fornecido
    s = format_e(val, sep_dec='.', sep_milhar='', m=0)
    if '.' in s:
        return len(s.split('.')[1])
    return 0

def tratar_zeros(area, sx, sy, x_c, y_c, ixc, iyc, pxyc, pxy):
    """
    Aproxima para zero propriedades muito próximas de zero, com base em referências geométricas,
    para fins didáticos — eliminando resíduos numéricos e evidenciando simetrias ou nulidades exatas.

    Em particular, centróides, momentos estáticos e produtos de inércia nulos possuem significado físico,
    portanto é importante destacar esses resultados em um contexto didático.

    Parameters
    ----------
    area : float
        Área da seção.
    sx, sy : float
        Momentos estáticos em relação aos eixos de referência.
    x_c, y_c : float
        Coordenadas do centroide.
    ixc, iyc : float
        Momentos de inércia centrais.
    pxyc, pxy : float
        Produtos de inércia central e em relação à origem dos eixos de referência.

    Returns
    -------
    list of float
        Valores ajustados: [sx, sy, x_c, y_c, pxyc, pxy]
    """
    # Raios de giração
    rxc = m.sqrt(ixc / area)
    ryc = m.sqrt(iyc / area)

    # Referências de ordem de grandeza
    ref1 = (rxc + ryc) / 2    # comprimento
    ref3 = ref1 ** 3          # momento estático
    ref4 = ref1 ** 4          # produto de inércia

    # Tolerâncias
    tol_abs = 1e-3   # absoluta
    tol_rel = 1e-6   # relativa

    # Função auxiliar para avaliar se valor deve ser zero
    def avaliar_zero(valor, ref):
        if abs(valor) < tol_abs and abs(valor / ref) < tol_rel:
            return 0
        return valor

    # Aplicação das tolerâncias
    sx   = avaliar_zero(sx,   ref3)
    sy   = avaliar_zero(sy,   ref3)
    x_c  = avaliar_zero(x_c,  ref1)
    y_c  = avaliar_zero(y_c,  ref1)
    pxyc = avaliar_zero(pxyc, ref4)
    pxy  = avaliar_zero(pxy,  ref4)

    return [sx, sy, x_c, y_c, pxyc, pxy]    
    
def imprime_resultados(area, sx, sy, x_c, y_c, ixc, iyc, pxyc, ix, iy, imax, imin, e1, e2, pxy, unidades, sep_dec=',', sep_milhar='.'):
    """
    Imprime os resultados das propriedades geométricas da seção.
    
    Parameters
    ----------
    area : float
        Área da seção transversal.
    sx : float
        Momento estático de primeira ordem em relação ao eixo x de referência.
    sy : float
        Momento estático de primeira ordem em relação ao eixo y de referência.
    x_c : float
        Coordenada x do centróide da seção.
    y_c : float
        Coordenada y do centróide da seção.
    ixc : float
        Momento de inércia em relação ao eixo x que passa pelo centróide.
    iyc : float
        Momento de inércia em relação ao eixo y que passa pelo centróide.
    pxyc : float
        Produto de inércia da seção em relação ao centróide.
    ix : float
        Momento de inércia em relação ao eixo x de referência.
    iy : float
        Momento de inércia em relação ao eixo y de referência.
    imax : float
        Momento de inércia principal máximo da seção.
    imin : float
        Momento de inércia principal mínimo da seção.
    e1 : float
        Ângulo e₁ (em graus) do eixo principal associado a I,máx.
    e2 : float
        Ângulo e₂ (em graus) do eixo principal associado a I,min.
    pxy : float
        Produto de inércia em relação aos eixos de referência.
    unidades : dict
        Dicionário contendo as unidades de medida.
    sep_dec : str, opcional
        Caractere a ser utilizado como separador decimal. O padrão é vírgula ','.
    sep_milhar : str, opcional
        Caractere a ser utilizado como separador de milhar. O padrão é ponto '.'.
    
    Returns
    -------
    None
        A função apenas imprime os resultados, sem retornar valor.
    """
    
    # Tratamento especial de resíduos numéricos de algumas propriedades:
    sx, sy, x_c, y_c, pxyc, pxy = tratar_zeros(area, sx, sy, x_c, y_c, ixc, iyc, pxyc, pxy)
    
    e1 = round(e1,2)
    e2 = round(e2,2)
    
    # Ajusta θ1 e θ2
    # objetivo: manter θ1 com a fórmula padrão e θ2 = θ1 + 90, mas reposicionar texto
    # obs.: e1 está sempre associado com I,max na função propriedades_geometricas
    
    texto_min = '(associado a I,min)'
    texto_max = '(associado a I,max)'
    
    if e1 < e2:
        θ1 = e1
        θ2 = e2
        t1 = texto_max
        t2 = texto_min
    else:
        θ1 = e2
        θ2 = e1
        t1 = texto_min
        t2 = texto_max      
    
    # Imprime os resultados:
    print(f"""
# ------------------------------------------------------------ #
# ------------------------ Resultados ------------------------ #
# ------------------------------------------------------------ #

Área da seção:
A = {format_n(area,sep_dec,sep_milhar)} {unidades[2]}

# ----- Resultados em relação aos eixos de referência:  ------ #

Coordenadas (xc, yc) do centróide:
xc = {format_n(x_c,sep_dec,sep_milhar)} {unidades[1]}
yc = {format_n(y_c,sep_dec,sep_milhar)} {unidades[1]}

Momentos estáticos de 1ª ordem:
Sx = {format_n(sx,sep_dec,sep_milhar)} {unidades[3]}
Sy = {format_n(sy,sep_dec,sep_milhar)} {unidades[3]}

Momentos de inércia de área:
Ix = {format_n(ix,sep_dec,sep_milhar)} {unidades[4]}
Iy = {format_n(iy,sep_dec,sep_milhar)} {unidades[4]}

Produto de inércia:
Pxy = {format_n(pxy,sep_dec,sep_milhar)} {unidades[4]}

# -------- Resultados em relação aos eixos centrais:  -------- #

Momentos de inércia centrais de área:
Ixc = {format_n(ixc,sep_dec,sep_milhar)} {unidades[4]}
Iyc = {format_n(iyc,sep_dec,sep_milhar)} {unidades[4]}

Produto de inércia central:
Pxcyc = {format_n(pxyc,sep_dec,sep_milhar)} {unidades[4]}

Momentos principais centrais de inércia:
I,max = {format_n(imax,sep_dec,sep_milhar)} {unidades[4]}
I,min = {format_n(imin,sep_dec,sep_milhar)} {unidades[4]}

Eixos principais centrais de inércia:
θ1 = {format_n(θ1,sep_dec,sep_milhar)}° {t1}
θ2 = {format_n(θ2,sep_dec,sep_milhar)}° {t2}

""")

def imprime_resultados_parciais(caminhos, n_sup, unidades, sep_dec=',', sep_milhar='.'):
    """
    Imprime os resultados parciais das propriedades geométricas:
    1) Da seção sem furos;
    2) De cada um dos furos isoladamente.
    
    Parameters
    ----------
    caminhos : dict
        Dicionário contendo os objetos Caminho da seção.
    n_sup : list of int
        Lista com o número do caminho final de cada grupo de caminhos:
        - n_sup[0] = número do caminho final do contorno externo
        - n_sup[1] = número do caminho final do furo 1
        - n_sup[2] = número do caminho final do furo 2
        - ...
    unidades : dict
        Dicionário contendo as unidades de medida.
    sep_dec : str, optional
        Separador decimal (padrão: vírgula ',').
    sep_milhar : str, optional
        Separador de milhar (padrão: ponto '.').
    
    Returns
    -------
    None
        A função apenas imprime os resultados, sem retornar valor.
    """
    
    # Número de furos
    nf = len(n_sup) - 1

    # Recebe dicionário com listas de propriedades parciais
    props = propriedades_parciais(caminhos, n_sup)
    area = props['area']
    sx   = props['sx']
    sy   = props['sy']
    x_c  = props['x_c']
    y_c  = props['y_c']
    ixc  = props['ixc']
    iyc  = props['iyc']
    pxyc = props['pxyc']
    ix   = props['ix']
    iy   = props['iy']
    imax = props['imax']
    imin = props['imin']
    e1   = props['e1']
    e2   = props['e2']
    pxy  = props['pxy']
    
    # Tratamento especial de resíduos numéricos de algumas propriedades:
    for i in range(nf + 1): 
        sx[i], sy[i], x_c[i], y_c[i], pxyc[i], pxy[i] = tratar_zeros(
            area[i], sx[i], sy[i], x_c[i], y_c[i], ixc[i], iyc[i], pxyc[i], pxy[i]
        )
    
        e1[i] = round(e1[i],2)
        e2[i] = round(e2[i],2)
    
    # Define títulos e outros textos
    titulo = ["# " + "-"*70 + " #" +
              "\n# ------------- Resultados do contorno externo (sem furos) ------------- #" +
              "\n" + "# " + "-"*70 + " #"]
    
    for i in range(1, nf + 1):
        titulo.append("# " + "-"*70 + " #" +
                      f"\n# ------------------------ Resultados do furo {i} ------------------------ #" +
                      "\n" + "# " + "-"*70 + " #")
        
    # Imprime resultados
    for i in range(nf + 1):
        elemento = "contorno externo" if i == 0 else f"furo {i}"
        indice   = ",c" if i == 0 else f",f{i}"
        if i == 0:
            n_inicial = 1
        else:
            n_inicial = n_sup[i - 1] + 1
        n_final = n_sup[i]
        caminhos_considerados = [f"C{j}" for j in range(n_inicial, n_final + 1)]
        print(f"""
{titulo[i]}

Caminhos: {', '.join(caminhos_considerados)}

Área:
A = {format_n(area[i], sep_dec, sep_milhar)} {unidades[2]}

Resultados em relação aos eixos de referência:

Coordenadas (xc, yc) do centróide:
xc = {format_n(x_c[i], sep_dec, sep_milhar)} {unidades[1]}
yc = {format_n(y_c[i], sep_dec, sep_milhar)} {unidades[1]}

Momentos estáticos de 1ª ordem:
Sx = {format_n(sx[i], sep_dec, sep_milhar)} {unidades[3]}
Sy = {format_n(sy[i], sep_dec, sep_milhar)} {unidades[3]}

Momentos de inércia de área:
Ix = {format_n(ix[i], sep_dec, sep_milhar)} {unidades[4]}
Iy = {format_n(iy[i], sep_dec, sep_milhar)} {unidades[4]}

Produto de inércia:
Pxy = {format_n(pxy[i], sep_dec, sep_milhar)} {unidades[4]}

Resultados em relação aos eixos centrais do {elemento}:

Momentos de inércia centrais de área:
Ixc{indice} = {format_n(ixc[i], sep_dec, sep_milhar)} {unidades[4]}
Iyc{indice} = {format_n(iyc[i], sep_dec, sep_milhar)} {unidades[4]}

Produto de inércia central:
Pxyc{indice} = {format_n(pxyc[i], sep_dec, sep_milhar)} {unidades[4]}

Momentos principais centrais de inércia:
I,max = {format_n(imax[i],sep_dec,sep_milhar)} {unidades[4]}
I,min = {format_n(imin[i],sep_dec,sep_milhar)} {unidades[4]}

Eixos principais centrais de inércia:
θ1 = {format_n(min(e1[i],e2[i]),sep_dec,sep_milhar)}° 
θ2 = {format_n(max(e1[i],e2[i]),sep_dec,sep_milhar)}° 
""")
        # Observações sobre o sinal da área
        if i == 0:
            print("Obs.: A área do contorno externo deve ser positiva."
                  "\n      → Os caminhos devem ser fornecidos no sentido anti-horário.")
            if area[i] < 0:
                print("\n⚠️  Aviso: área negativa — verifique o sentido dos caminhos do contorno.")
        else:
            print(f"Obs.: A área de cada furo deve ser negativa (subtração de área)."
                  "\n      → Os caminhos devem ser fornecidos no sentido horário.")
            if area[i] > 0:
                print(f"\n⚠️  Aviso: área positiva — verifique o sentido dos caminhos do furo {i}.")
        print()

                
def salva_resultados_txt(*args, nome_do_arquivo="resultados_green.txt", **kwargs):
    """
    Salva os resultados impressos pela função "imprime_resultados" em um arquivo de texto.

    Parameters
    ----------
    nome_do_arquivo : str, optional
        Nome do arquivo onde os resultados serão salvos. Padrão é 'resultados_green.txt'.
    *args :
        Argumentos posicionais a serem passados para "imprime_resultados".
        *args esperados:
        --> area, sx, sy, x_c, y_c, ixc, iyc, pxyc, ix, iy, imax, imin, e1, e2, pxy, unidades
        --> para mais informações, ver documentação da função imprime_resultados
    **kwargs :
        Argumentos nomeados a serem passados para `imprime_resultados`.
        **kwargs esperados:
        --> sep_dec=',', sep_milhar='.'
        --> para mais informações, ver documentação da função imprime_resultados 

    Returns
    -------
    None
        Apenas salva os resultados no arquivo.
    """
    original_stdout = sys.stdout  # Guarda o stdout original
    try:
        with open(nome_do_arquivo, 'w', encoding='utf-8') as f:
            sys.stdout = f  # Redireciona prints para o arquivo
            imprime_resultados(*args, **kwargs)
    finally:
        sys.stdout = original_stdout  # Restaura o stdout


def salva_saida_txt(funcao, *args, nome_do_arquivo="saida.txt", pasta_destino=None, **kwargs):
    """
    Redireciona a saída da função fornecida para um arquivo de texto.

    Parameters
    ----------
    funcao : callable
        Função que será chamada e cuja saída (via print) será salva no arquivo.
    *args :
        Argumentos posicionais para a função.
    nome_do_arquivo : str, optional
        Nome do arquivo de saída. Padrão é 'saida.txt'.
    pasta_destino : str, optional
        Caminho da pasta onde o arquivo será salvo. Se None, salva no diretório atual.
    **kwargs :
        Argumentos nomeados para a função.

    Returns
    -------
    None
        Apenas salva o conteúdo da função no arquivo.
    """
    
    if pasta_destino:
        os.makedirs(pasta_destino, exist_ok=True)
        caminho_completo = os.path.join(pasta_destino, nome_do_arquivo)
    else:
        caminho_completo = nome_do_arquivo
    
    original_stdout = sys.stdout
    try:
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            sys.stdout = f
            funcao(*args, **kwargs)
    finally:
        sys.stdout = original_stdout

        
def copia_arquivo_txt(nome_arquivo, pasta_destino):
    """
    Copia um arquivo .txt do diretório atual para uma pasta de destino.

    Parameters
    ----------
    nome_arquivo : str
        Nome do arquivo a ser copiado (ex: 'saida.txt').
    pasta_destino : str
        Caminho da pasta para onde o arquivo será copiado.

    Returns
    -------
    None
    """
    # Verifica se o arquivo existe
    if not os.path.isfile(nome_arquivo):
        raise FileNotFoundError(f"O arquivo '{nome_arquivo}' não foi encontrado no diretório atual.")

    # Cria a pasta de destino, se necessário
    os.makedirs(pasta_destino, exist_ok=True)

    # Caminho completo do arquivo de destino
    caminho_destino = os.path.join(pasta_destino, nome_arquivo)

    # Copia o conteúdo do arquivo
    with open(nome_arquivo, 'r', encoding='utf-8') as origem:
        conteudo = origem.read()

    with open(caminho_destino, 'w', encoding='utf-8') as destino:
        destino.write(conteudo)
        
        
# ---------------------------- #
# --- Definição de classes --- #
# ---------------------------- #

class Caminho:
    """
    Classe que cria os objetos associados aos caminhos do contorno e dos furos.
    
    Esta classe representa os caminhos do contorno utilizados em cálculos de propriedades geométricas,
    podendo ser segmentos retos, arcos de circunferência ou parábolas.

    Os métodos disponíveis permitem, entre outros:
        - Calcular as contribuições do caminho às propriedades geométricas da seção;
        - Determinar coordenadas do centro de arcos e coeficientes de parábolas;
        - Diagnosticar e consolidar dados de arcos de circunferência;
        ...

    Parameters
    ----------
    n : int
        Número identificador do caminho.
    tipo : int, optional
        Tipo do caminho geométrico. Pode ser:
            1 - segmento de reta (valor padrão),
            2 - arco de circunferência,
            3 - parábola do tipo y = f(x),
            4 - parábola do tipo x = f(y).
    xi : float, optional
        Coordenada x do ponto inicial do caminho. Valor padrão é 0.
    xf : float, optional
        Coordenada x do ponto final do caminho. Valor padrão é 0.
    yi : float, optional
        Coordenada y do ponto inicial do caminho. Valor padrão é 0.
    yf : float, optional
        Coordenada y do ponto final do caminho. Valor padrão é 0.
    integral : {'num', 'numpy', 'simb'}, optional
        Tipo de integração a ser utilizada para o cálculo das propriedades geométricas:
            'num'   - integração numérica usando `scipy.integrate.quad`,
            'numpy' - integração numérica usando método dos trapézios,
            'simb'  - cálculo com fórmulas analíticas previamente deduzidas com SymPy (padrão).
    erro : float, optional
        Tolerância de erro absoluto e relativo para integração numérica com SciPy. 
        Usado apenas quando `integral='num'`. Valor padrão é 1e-6.

    Attributes
    ----------
    # Gerais
    xi, yi, xf, yf : float
        Coordenadas dos pontos inicial e final do caminho. Definidas inicialmente ou via setters.
    tipo : int
        Tipo do caminho. Definido inicialmente ou via setter.
    xm, ym : float
        Coordenadas médias do caminho (calculadas).
    
    # Segmentos de reta (tipo=1)
    (não possuem atributos exclusivos além dos gerais)

    # Arcos de circunferência (tipo=2)
    raio : float
        Raio do arco. Definido via setter.
    angulo_i : float
        Ângulo inicial do arco (graus). Definido via setter.
    angulo_f : float
        Ângulo final do arco (graus). Definido via setter.
    xc, yc : float
        Coordenadas do centro do arco. Calculadas via função `avaliar_arco`.
    status_arco : str
        Status do arco após diagnóstico/consolidação. 
        Pode ser:
            - 'ok' → dados consistentes
            - 'pequeno_ajuste' → ajuste sugerido
            - 'ajustado' → ajuste aplicado
            - 'inconsistente' → dados incoerentes
    mensagem_arco : str
        Texto explicativo com o resultado do diagnóstico ou consolidação.
    
    # Parábolas (tipo=3 ou 4)
    xp, yp : float
        Coordenadas de ponto intermediário da parábola. Definidas via setters.
    a, b, c : float
        Coeficientes da parábola.
        Calculados com o método coeficientes().

    # Propriedades geométricas (todos os tipos)
    area, sx, sy, ix, iy, pxy : float
        Contribuições do caminho às propriedades geométricas da seção.
        Calculadas com o método geo_prop().

    Methods
    -------
    coeficientes()
        Calcula os coeficientes a, b, c da parábola que passa pelos três pontos definidos.
    geo_prop()
        Calcula as contribuições do caminho às propriedades geométricas da seção.
    diagnosticar_arco(tol_ang=5.0)
        Avalia consistência dos dados de arco com a função `avaliar_arco` e atualiza 
        `status_arco` e `mensagem_arco`, sem alterar ângulos.
    consolidar_arco(tol_ang=5.0)
        Se o diagnóstico indicar 'pequeno_ajuste', aplica ajustes mínimos nos
        ângulos do arco (`angulo_i`, `angulo_f`) e atualiza `status_arco` e `mensagem_arco`.
    """

    def __init__(self, n, tipo=1, xi=0, xf=0, yi=0, yf=0, integral="simb", erro=1e-6):

        # Dados de todos os caminhos:
        self.n = n          # número do caminho (int)
        self.tipo = tipo    # tipo do caminho   (1, 2, 3 ou 4)
        self.xi = xi        # coordenada x do ponto inicial do caminho (float)
        self.xf = xf        # coordenada x do ponto final do caminho   (float)
        self.yi = yi        # coordenada y do ponto inicial do caminho (float)
        self.yf = yf        # coordenada y do ponto final do caminho   (float)

        # Dados exclusivos de arcos de circunferência:
        self._raio = None            # raio do arco           (float, opcional)
        self._angulo_i = None        # ângulo inicial do arco (float, opcional)
        self._angulo_f = None        # ângulo final do arco   (float, opcional)
        self._angulo_i_user = None   # ângulo inicial digitado pelo usuário
        self._angulo_f_user = None   # ângulo final digitado pelo usuário
        
        # Dados do diagnóstico automático dos dados de arcos
        self._status_arco = None     # status do diagnóstico 
        self._mensagem_arco = None   # mensagem do diagnóstico
        
        # Dados exclusivos de parábolas:
        # coordenada x de ponto intermediário da parábola (float, opcional)
        self._xp = None
        # coordenada y de ponto intermediário da parábola (float, opcional)
        self._yp = None
        
        # Dados da integração:
        self.integral = integral
        self.erro = erro

        # os dados gerais podem ser definidos diretamente ao chamar Caminho(...) ou pelos setters
        # os dados inicializados como None podem ser definidos apenas pelos setters

    # x médio
    @property
    def xm(self):
        return (self.xi + self.xf)/2

    # y médio
    @property
    def ym(self):
        return (self.yi + self.yf)/2

    # Dados complementares de arcos:

    # ângulo inicial em rad
    @property
    def angulo_i_rad(self):
        return self.angulo_i*m.pi/180

    # ângulo final em rad
    @property
    def angulo_f_rad(self):
        return self.angulo_f*m.pi/180

    # xc
    @property
    def xc(self):
        if self.tipo == 2:
            analise = avaliar_arco(self.xi, self.yi, self.xf, self.yf,
                                   self.raio, self._angulo_i, self._angulo_f)
            return analise['xc']
        else:
            return None

    # yc
    @property
    def yc(self):
        if self.tipo == 2:
            analise = avaliar_arco(self.xi, self.yi, self.xf, self.yf,
                                   self.raio, self._angulo_i, self._angulo_f)
            return analise['yc']
        else:
            return None

    # Dados complementares de parábolas:

    # Cálculo de coeficientes [a,b,c] de a.x^2 + b.x + c (se tipo 3) ou de a.y^2 + b.y + c (se tipo 4)
    def coeficientes(self):

        # Reutiliza coeficientes já calculados (se existirem), evitando repetições desnecessárias
        if hasattr(self, '_coeficientes_cache'):
            return self._coeficientes_cache
            # obs: cada vez que um parâmetro é atualizado via setters, o cache é deletado (ver ao final)

        if self.tipo == 3:
            # Parábola do tipo y = a*x^2 + b*x + c
            # Montando o sistema de equações:
            # yi = a*xi^2 + b*xi + c
            # yf = a*xf^2 + b*xf + c
            # yp = a*xp^2 + b*xp + c
            A = np.array([
                [self.xi**2, self.xi, 1],
                [self.xf**2, self.xf, 1],
                [self.xp**2, self.xp, 1]
            ])
            B = np.array([self.yi, self.yf, self.yp])

            # Depois de calcular, armazena os resultados no cache
            # Objetivo: evitar repetição dos cálculos, a menos que parâmetros sejam alterados via setters
            self._coeficientes_cache = np.linalg.solve(A, B)
            return self._coeficientes_cache

        elif self.tipo == 4:
            # Parábola do tipo x = a*y^2 + b*y + c
            # Montando o sistema de equações:
            # xi = a*yi^2 + b*yi + c
            # xf = a*yf^2 + b*yf + c
            # xp = a*yp^2 + b*yp + c
            A = np.array([
                [self.yi**2, self.yi, 1],
                [self.yf**2, self.yf, 1],
                [self.yp**2, self.yp, 1]
            ])
            B = np.array([self.xi, self.xf, self.xp])

            # Depois de calcular, armazena os resultados no cache
            self._coeficientes_cache = np.linalg.solve(A, B)
            return self._coeficientes_cache

        else:
            return [None, None, None]

    # Coeficientes a,b,c separados:
    @property
    def a(self):
        return self.coeficientes()[0]

    @property
    def b(self):
        return self.coeficientes()[1]

    @property
    def c(self):
        return self.coeficientes()[2]

    # Cálculo de propriedades geométricas:
    def geo_prop(self):

        # Reutiliza propriedades já calculadas (se existirem), evitando repetições desnecessárias
        if hasattr(self, '_geo_prop_cache'):
            return self._geo_prop_cache
            # obs: cada vez que um parâmetro é atualizado via setters, o cache é deletado (ver ao final)
        
        # Inicializa variáveis bool que serão usadas para definir forma de integração
        sympy_integration = False
        numpy_integration = False
        scipy_integration = False
        
        # Define como irá realizar a integração:
        if self.integral == 'simb':
            sympy_integration = True
        
        elif self.integral == 'num':
            try:
                from scipy.integrate import quad
                scipy_integration = True
            except ImportError:
                print("Atenção! O pacote 'scipy' não está instalado ou houve problema em sua importação. Será usada a integração numérica pelo método dos trapézios com NumPy.")
                scipy_integration = False
                numpy_integration = True        
        
        elif self.integral == 'numpy':
            numpy_integration = True 
        
        # Se forem utilizadas equações analíticas deduzidas previamente com sympy:
        if sympy_integration:

            # Nesse caso, as integrações já foram realizadas previamente com variáveis simbólicas, via sympy.
            # Aqui já são inseridas as equações fechadas obtidas com esse procedimento.
            # Apesar de o módulo sympy ter sido usado no processo, aqui ele não precisa ser importado.

            if self.tipo == 1:
                # === TIPO 1: Segmento de reta (t ∈ [0,1]) ===
                xi, yi, xf, yf = self.xi, self.yi, self.xf, self.yf

                area = (xf + xi)*(yf - yi)/2
                sx   = (yf - yi)*(2*xf*yf + xf*yi + xi*yf + 2*xi*yi)/6
                sy   = (yf - yi)*(xf**2 + xf*xi + xi**2)/6
                ix   = (yf - yi)*(3*xf*yf**2 + 2*xf*yf*yi + xf*yi**2 + xi*yf**2 + 2*xi*yf*yi + 3*xi*yi**2)/12
                iy   = (xf + xi)*(xf**2 + xi**2)*(yf - yi)/12
                pxy  = (yf - yi)*(3*xf**2*yf + xf**2*yi + 2*xf*xi*yf + 2*xf*xi*yi + xi**2*yf + 3*xi**2*yi)/24

            elif self.tipo == 2:
                # === TIPO 2: Arco de circunferência
                #     x = xc + r*cos(t), y = yc + r*sin(t), t ∈ [ang_i, ang_f], dy = r*cos(t) dt
                from math import sin, cos
                xc, yc, r = self.xc, self.yc, self.raio
                ti, tf    = self.angulo_i_rad, self.angulo_f_rad

                # Primitivas em t (use F(ang_f) - F(ang_i)):
                def FA(t):   # ∫ x dy
                    return r*(2*r*t + r*sin(2*t) + 4*xc*sin(t))/4

                def FSx(t):  # ∫ x*y dy
                    return -r*(
                        3*r**2*cos(t) + r**2*cos(3*t) - 6*r*t*yc
                      + 3*r*xc*cos(2*t) - 3*r*xc - 3*r*yc*sin(2*t)
                      - 12*xc*yc*sin(t)
                    )/12

                def FSy(t):  # ∫ (x**2)/2 dy
                    return -r*(
                        r**2*sin(t)**3 - 3*r**2*sin(t) - 3*r*t*xc
                      - 3*r*xc*sin(t)*cos(t) - 3*xc**2*sin(t)
                    )/6

                def FIx(t):  # ∫ x*(y**2) dy
                    return r*(
                        12*r**3*t - 3*r**3*sin(4*t) + 24*r**2*xc*sin(t)
                      - 8*r**2*xc*sin(3*t) - 48*r**2*yc*cos(t)
                      - 16*r**2*yc*cos(3*t) + 48*r*t*yc**2
                      - 48*r*xc*yc*cos(2*t) + 48*r*xc*yc
                      + 24*r*yc**2*sin(2*t) + 96*xc*yc**2*sin(t)
                    )/96

                def FIy(t):  # ∫ (x**3)/3 dy
                    return r*(
                        12*r**3*t + 8*r**3*sin(2*t) + r**3*sin(4*t)
                      + 72*r**2*xc*sin(t) + 8*r**2*xc*sin(3*t)
                      + 48*r*t*xc**2 + 24*r*xc**2*sin(2*t)
                      + 32*xc**3*sin(t)
                    )/96

                def FPxy(t): # ∫ (x**2*y)/2 dy
                    return -r*(
                        3*r**3*cos(t)**4 + 8*r**2*xc*cos(t)**3
                      - 8*r**2*yc*sin(t)**3 - 12*r**2*yc*sin(t)*cos(t)**2
                      - 12*r*t*xc*yc*sin(t)**2 - 12*r*t*xc*yc*cos(t)**2
                      - 6*r*xc**2*sin(t)**2 - 6*r*xc*yc*sin(2*t)
                      - 12*xc**2*yc*sin(t)
                    )/24

                area = FA(tf)  - FA(ti)
                sx   = FSx(tf) - FSx(ti)
                sy   = FSy(tf) - FSy(ti)
                ix   = FIx(tf) - FIx(ti)
                iy   = FIy(tf) - FIy(ti)
                pxy  = FPxy(tf) - FPxy(ti)

            elif self.tipo == 3:
                # === TIPO 3: Parábola y = f(x) (x: xi → xf) ===
                a, b, c = self.a, self.b, self.c
                xi, xf  = self.xi, self.xf

                # Primitivas em x (use F(xf) - F(xi)):
                def FA(x):   return x**2*(4*a*x + 3*b)/6

                def FSx(x):  return x**2*(
                        24*a**2*x**3 + 45*a*b*x**2 + 40*a*c*x
                      + 20*b**2*x + 30*b*c
                )/60

                def FSy(x):  return x**3*(3*a*x + 2*b)/12

                def FIx(x):  return x**2*(
                        120*a**3*x**5 + 350*a**2*b*x**4 + 336*a**2*c*x**3
                      + 336*a*b**2*x**3 + 630*a*b*c*x**2 + 280*a*c**2*x
                      + 105*b**3*x**2 + 280*b**2*c*x + 210*b*c**2
                )/420

                def FIy(x):  return x**4*(8*a*x + 5*b)/60

                def FPxy(x): return x**3*(
                        20*a**2*x**3 + 36*a*b*x**2 + 30*a*c*x
                      + 15*b**2*x + 20*b*c
                )/120

                area = FA(xf)  - FA(xi)
                sx   = FSx(xf) - FSx(xi)
                sy   = FSy(xf) - FSy(xi)
                ix   = FIx(xf) - FIx(xi)
                iy   = FIy(xf) - FIy(xi)
                pxy  = FPxy(xf) - FPxy(xi)

            elif self.tipo == 4:
                # === TIPO 4: Parábola x = f(y) (y: yi → yf) ===
                a, b, c = self.a, self.b, self.c
                yi, yf  = self.yi, self.yf

                # Primitivas em y (use F(yf) - F(yi)):
                def FA(y):   return y*(2*a*y**2 + 3*b*y + 6*c)/6

                def FSx(y):  return y**2*(3*a*y**2 + 4*b*y + 6*c)/12

                def FSy(y):  return y*(
                        6*a**2*y**4 + 15*a*b*y**3 + 20*a*c*y**2
                      + 10*b**2*y**2 + 30*b*c*y + 30*c**2
                )/60

                def FIx(y):  return y**3*(12*a*y**2 + 15*b*y + 20*c)/60

                def FIy(y):  return y*(
                        20*a**3*y**6 + 70*a**2*b*y**5 + 84*a**2*c*y**4
                      + 84*a*b**2*y**4 + 210*a*b*c*y**3 + 140*a*c**2*y**2
                      + 35*b**3*y**3 + 140*b**2*c*y**2 + 210*b*c**2*y + 140*c**3
                )/420

                def FPxy(y): return y**2*(
                        10*a**2*y**4 + 24*a*b*y**3 + 30*a*c*y**2
                      + 15*b**2*y**2 + 40*b*c*y + 30*c**2
                )/120

                area = FA(yf)  - FA(yi)
                sx   = FSx(yf) - FSx(yi)
                sy   = FSy(yf) - FSy(yi)
                ix   = FIx(yf) - FIx(yi)
                iy   = FIy(yf) - FIy(yi)
                pxy  = FPxy(yf) - FPxy(yi)

        # Se for usada integração numérica com SciPy:
        if scipy_integration:

            if self.tipo == 1:
                # Parametrização do segmento de reta:
                def x(t):
                    return self.xi + t * (self.xf - self.xi)

                def y(t):
                    return self.yi + t * (self.yf - self.yi)

                def dy(t):
                    return self.yf - self.yi  # .dt ocultado

                # Intervalo de integração
                li = 0  # limite inferior de integração
                lf = 1  # limite superior de integração

            elif self.tipo == 2:
                # Parametrização do arco de circunferência:
                def x(t):
                    return self.xc + self.raio * np.cos(t)

                def y(t):
                    return self.yc + self.raio * np.sin(t)

                def dy(t):
                    return self.raio * np.cos(t)  # .dt ocultado

                # Intervalo de integração
                li = self.angulo_i_rad  # limite inferior de integração
                lf = self.angulo_f_rad  # limite superior de integração

            elif self.tipo == 3:
                # Parametrização de parábola tipo y=f(x):
                def x(t):
                    return self.xi + t * (self.xf - self.xi)

                def y(t):
                    return self.a * x(t)**2 + self.b * x(t) + self.c

                def dy(t):
                    # .dt ocultado
                    return 2*self.a*t*(self.xf-self.xi)**2 + (2*self.a*self.xi+self.b)*(self.xf-self.xi)

                # Intervalo de integração
                li = 0  # limite inferior de integração
                lf = 1  # limite superior de integração

            elif self.tipo == 4:
                # Parametrização de parábola tipo x=f(y):
                def y(t):
                    return self.yi + t * (self.yf - self.yi)

                def x(t):
                    return self.a * y(t)**2 + self.b * y(t) + self.c

                def dy(t):
                    return self.yf - self.yi  # .dt ocultado

                # Intervalo de integração
                li = 0  # limite inferior de integração
                lf = 1  # limite superior de integração

            # Realiza as integrações numéricas usando quad do SciPy
            area = quad(lambda t: x(t) * dy(t), li, lf,
                        epsabs=self.erro, epsrel=self.erro)[0]
            sx = quad(lambda t: x(t) * y(t) * dy(t), li, lf,
                      epsabs=self.erro, epsrel=self.erro)[0]
            sy = quad(lambda t: (x(t)**2) * dy(t) / 2, li, lf,
                      epsabs=self.erro, epsrel=self.erro)[0]
            ix = quad(lambda t: x(t) * (y(t)**2) * dy(t), li,
                      lf, epsabs=self.erro, epsrel=self.erro)[0]
            iy = quad(lambda t: (x(t)**3) * dy(t) / 3, li, lf,
                      epsabs=self.erro, epsrel=self.erro)[0]
            pxy = quad(lambda t: (x(t)**2) * y(t) * dy(t) / 2, li,
                       lf, epsabs=self.erro, epsrel=self.erro)[0]
        
        
        # Se integral = 'num' e não conseguir importar o pacote SciPy, integra com o NumPy.
        # Nesse caso, é adotado o método dos trapézios.
        # Pode ocorrer uma pequena imprecisão numérica, provavelmente não relevante.
        if numpy_integration:    
            
            n_pts = 10000 
            
            if self.tipo == 1:
                # Parametrização do segmento de reta:
                t = np.linspace(0, 1, n_pts)
                x = self.xi + t * (self.xf - self.xi)
                y = self.yi + t * (self.yf - self.yi)
                dy_dt = self.yf - self.yi

            elif self.tipo == 2:
                n_pts = n_pts*10
                # Parametrização do arco de circunferência:
                t = np.linspace(self.angulo_i_rad, self.angulo_f_rad, n_pts)
                x = self.xc + self.raio * np.cos(t)
                y = self.yc + self.raio * np.sin(t)
                dy_dt = self.raio * np.cos(t)

            elif self.tipo == 3:
                n_pts = n_pts*10
                # Parametrização de parábola tipo y=f(x):
                t = np.linspace(0, 1, n_pts)
                x_t = self.xi + t * (self.xf - self.xi)
                x = x_t
                y = self.a * x_t**2 + self.b * x_t + self.c
                dy_dt = 2*self.a*t*(self.xf-self.xi)**2 + (2*self.a*self.xi+self.b)*(self.xf-self.xi)

            elif self.tipo == 4:
                n_pts = n_pts*10
                # Parametrização de parábola tipo x=f(y):
                t = np.linspace(0, 1, n_pts)
                y_t = self.yi + t * (self.yf - self.yi)
                y = y_t
                x = self.a * y_t**2 + self.b * y_t + self.c
                dy_dt = self.yf - self.yi

            # Cálculos das integrais usando método dos trapézios (numpy.trapz)
            area = np.trapz(x * dy_dt, t)
            sx = np.trapz(x * y * dy_dt, t)
            sy = np.trapz((x**2) * dy_dt / 2, t)
            ix = np.trapz(x * (y**2) * dy_dt, t)
            iy = np.trapz((x**3) * dy_dt / 3, t)
            pxy = np.trapz((x**2) * y * dy_dt / 2, t)
        
        # Depois de calcular, armazena o resultado no cache
        # Objetivo: evitar repetição dos cálculos, a menos que parâmetros sejam alterados via setters
        self._geo_prop_cache = [area, sx, sy, ix, iy, pxy]
        return self._geo_prop_cache

    # Propriedades geométricas separadas como propriedades do objeto:

    @property
    def area(self):
        return self.geo_prop()[0]

    @property
    def sx(self):
        return self.geo_prop()[1]

    @property
    def sy(self):
        return self.geo_prop()[2]

    @property
    def ix(self):
        return self.geo_prop()[3]

    @property
    def iy(self):
        return self.geo_prop()[4]

    @property
    def pxy(self):
        return self.geo_prop()[5]

    # Métodos internos para limpar cachê
    def _limpar_cache_geo(self):
        """
        Limpa o cache das propriedades geométricas, forçando o recálculo da próxima vez que forem solicitadas.
        Este método é utilizado quando há modificações nos atributos do objeto que afetam as propriedades geométricas.
        """
        if hasattr(self, '_geo_prop_cache'):
            del self._geo_prop_cache
    
    def _limpar_cache_coef(self):
        """
        Limpa o cache dos coeficientes da parábola, forçando o recálculo da próxima vez que forem solicitadas.
        Este método é utilizado quando há modificações nos atributos do objeto que afetam os coeficientes.
        """
        if hasattr(self, '_coeficientes_cache'):
            del self._coeficientes_cache
    
    # Métodos para diagnóstico e pequenos ajustes dos dados dos arcos     
    def diagnosticar_arco(self, tol_ang=5.0):
        """Roda a função avaliar_arco com os ângulos que o usuário digitou e salva status/mensagem."""
        if self.tipo != 2:
            self._status_arco = None
            self._mensagem_arco = None
            return None

        analise = avaliar_arco(
            self.xi, self.yi, self.xf, self.yf, self.raio,
            self._angulo_i_user, self._angulo_f_user,
            tol_ang=tol_ang
        )

        self._status_arco   = analise['status']
        self._mensagem_arco = analise['mensagem']
        return analise


    def consolidar_arco(self, tol_ang=5.0):
        """
        Aplica o ajuste fino nos ângulos efetivos se o diagnóstico (status_arco)
        indicar 'pequeno_ajuste'. Após aplicar, atualiza status/mensagem para
        refletirem a consolidação.
        """
        if self.tipo != 2:
            return None  # não faz nada para outros tipos

        # Se ainda não diagnosticou após as últimas mudanças, faz agora:
        if self._status_arco is None:
            self.diagnosticar_arco(tol_ang=tol_ang)

        # Se não há pequeno ajuste a fazer, encerra silenciosamente
        if self._status_arco != 'pequeno_ajuste':
            return None

        # Reavalia com os ângulos do usuário para obter os alvos de ajuste
        analise = avaliar_arco(
            self.xi, self.yi, self.xf, self.yf, self.raio,
            self._angulo_i_user, self._angulo_f_user,
            tol_ang=tol_ang
        )

        # Diferenças angulares entre o que o usuário digitou e o alvo sugerido
        dif_i = abs(_ang_diff_deg(analise['ang_i'], self._angulo_i_user))
        dif_f = abs(_ang_diff_deg(analise['ang_f'], self._angulo_f_user))
        
        # Separador decimal
        # Se não existir no módulo, cai no padrão brasileiro (',')
        sd = globals().get('separador_decimal', ',')

        # --- Limiar de visbilidade dinâmico ---
        # Regra: usar a precisão digitada pelo usuário (nº de casas decimais),
        # porém nunca tolerar precisão inferior a 0,005 (2 casas decimais).

        casas_i = _casas_decimais(self._angulo_i_user)
        casas_f = _casas_decimais(self._angulo_f_user)
        casas = max(casas_i, casas_f)  # maior precisão fornecida pelo usuário

        precisao_usuario = (10.0 ** (-casas)) if casas > 0 else 1.0
        limiar_base = 5e-3  # 0,005
        limiar = min(limiar_base, precisao_usuario)
        
        casas_fmt_i = max(2, casas_i)
        casas_fmt_f = max(2, casas_f) 
        
        if dif_i >= limiar or dif_f >= limiar:
            msg = (
                "Para garantir a consistência geométrica, foram aplicados pequenos ajustes:\n"
                f"Ângulo inicial: {format(self._angulo_i_user, f'.{casas_fmt_i}f').replace('.', sd)}° → "
                f"{format(analise['ang_i'], f'.{casas_fmt_i}f').replace('.', sd)}°\n"
                f"Ângulo final:   {format(self._angulo_f_user, f'.{casas_fmt_f}f').replace('.', sd)}° → "
                f"{format(analise['ang_f'], f'.{casas_fmt_f}f').replace('.', sd)}°\n"
                "Confirme no gráfico se o arco corresponde ao pretendido."
            )
        else:
            msg = (
                "Dados do arco consistentes após ajuste mínimo de arredondamento.\n"
                "Confirme no gráfico se o arco corresponde ao pretendido."
            )

        # Se de fato é um caso de pequeno ajuste, aplique nos ângulos EFETIVOS:
        if analise['status'] == 'pequeno_ajuste':
            self._angulo_i = analise['ang_i']
            self._angulo_f = analise['ang_f']
            self._limpar_cache_geo()
            # Atualiza o diagnóstico para refletir que os ajustes foram concretizados
            self._status_arco   = 'ajustado'
            self._mensagem_arco = msg

        return analise

    
    # Propriedades de leitura do diagnóstico dos arcos
    @property
    def status_arco(self):
        return self._status_arco

    @property
    def mensagem_arco(self):
        return self._mensagem_arco
    
    # Helper para limpar diagnósticos
    def _limpar_diag_arco(self):
        self._status_arco = None
        self._mensagem_arco = None  
    
    # Getters and setters para dados de entrada
    # tipo, xi, yi, xf, yf, raio, angulo_i, angulo_f, xp, yp
    
    # tipo
    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, new_tipo):
        if new_tipo not in [1, 2, 3, 4]:
            raise ValueError("Tipo tem que ser 1, 2, 3 ou 4")
    
        self._tipo = new_tipo
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # xi
    @property
    def xi(self):
        return self._xi
    
    @xi.setter
    def xi(self, new_xi):
        if not isinstance(new_xi, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._xi = new_xi
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # xf
    @property
    def xf(self):
        return self._xf
    
    @xf.setter
    def xf(self, new_xf):
        if not isinstance(new_xf, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._xf = new_xf
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # yi
    @property
    def yi(self):
        return self._yi
    
    @yi.setter
    def yi(self, new_yi):
        if not isinstance(new_yi, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._yi = new_yi
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # yf
    @property
    def yf(self):
        return self._yf
    
    @yf.setter
    def yf(self, new_yf):
        if not isinstance(new_yf, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._yf = new_yf
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # raio
    @property
    def raio(self):
        return self._raio
    
    @raio.setter
    def raio(self, new_raio):
        if not isinstance(new_raio, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._raio = new_raio
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_diag_arco()   # Limpa o diagnóstico dos dados dos arcos
    
    # angulo_i
    @property
    def angulo_i(self):
        return self._angulo_i
    
    @angulo_i.setter
    def angulo_i(self, new_angulo_i):
        if not isinstance(new_angulo_i, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
            
        self._angulo_i = new_angulo_i
        self._angulo_i_user = new_angulo_i   # Guarda o ângulo que o usuário forneceu
        self._limpar_cache_geo()             # Limpa o cache das propriedades geométricas
        self._limpar_diag_arco()             # Limpa o diagnóstico dos dados dos arcos
    
    # angulo_f
    @property
    def angulo_f(self):
        return self._angulo_f
    
    @angulo_f.setter
    def angulo_f(self, new_angulo_f):
        if not isinstance(new_angulo_f, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._angulo_f = new_angulo_f
        self._angulo_f_user = new_angulo_f   # Guarda o ângulo que o usuário forneceu
        self._limpar_cache_geo()             # Limpa o cache das propriedades geométricas
        self._limpar_diag_arco()             # Limpa o diagnóstico dos dados dos arcos
    
    # xp
    @property
    def xp(self):
        return self._xp
    
    @xp.setter
    def xp(self, new_xp):
        if not isinstance(new_xp, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._xp = new_xp
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas
    
    # yp
    @property
    def yp(self):
        return self._yp
    
    @yp.setter
    def yp(self, new_yp):
        if not isinstance(new_yp, (int, float)):
            raise ValueError("Parâmetro tem que ser um número real.")
    
        self._yp = new_yp
        self._limpar_cache_geo()   # Limpa o cache das propriedades geométricas
        self._limpar_cache_coef()  # Limpa o cache dos coeficientes de parábolas


# ----------------------------------- #
# ------- Funções de cálculo -------- #
# ----------------------------------- #

def propriedades_geometricas(caminhos, n_inicial=None, n_final=None):
    """
    Calcula as propriedades geométricas da seção, considerando as contribuições dos caminhos do contorno e dos furos.

    Parameters
    ----------
    caminhos : dict
        Dicionário contendo os objetos Caminho do contorno e dos furos no formato {i: caminho[i]},
        com `i`, por padrão, variando de 1 até `ntot`. Também é possível fornecer subconjuntos com menos caminhos.
    n_inicial : int, opcional
        Número do primeiro caminho a ser considerado. Padrão é o menor índice presente em 'caminhos' (geralmente 1).
    n_final : int, opcional
        Número do último caminho a ser considerado. Padrão é o maior índice presente em 'caminhos' (geralmente ntot).

    Returns
    -------
    list of float
        Lista contendo as propriedades geométricas da seção:        
        - area : float  
          Área da seção.
        - sx : float  
          Momento estático de 1ª ordem em relação ao eixo x de referência.
        - sy : float  
          Momento estático de 1ª ordem em relação ao eixo y de referência.
        - x_c : float  
          Coordenada x do centróide em relação aos eixos de referência.
        - y_c : float  
          Coordenada y do centróide em relação aos eixos de referência.
        - ixc : float  
          Momento de inércia em relação ao eixo x central.
        - iyc : float  
          Momento de inércia em relação ao eixo y central.
        - pxyc : float  
          Produto de inércia em relação aos eixos centrais x e y.
        - ix : float  
          Momento de inércia em relação ao eixo x de referência.
        - iy : float  
          Momento de inércia em relação ao eixo y de referência.
        - imax : float  
          Momento central principal de inércia (máximo).
        - imin : float  
          Momento central principal de inércia (mínimo).
        - e1 : float  
          Eixo principal de inércia (em graus), associado a Imax.
        - e2 : float  
          Eixo principal de inércia (em graus), associado a Imín.
        - pxy : float  
          Produto de inércia em relação aos eixos de referência x e y.
    """    
    
    # Por padrão, n_inicial é o primeiro e n_final é o último índice do dicionário caminhos (geralmente 1 e ntot)
    if n_inicial is None:
        n_inicial = min(caminhos.keys()) 
    if n_final is None:
        n_final = max(caminhos.keys())
    
    # Inicializa variáveis globais de propriedades geométricas em relação aos eixos x,ref e y,ref
    area, sx, sy, ix, iy, pxy = np.zeros(6)

    # Soma contribuições dos caminhos selecionados
    for i in range(n_inicial, n_final + 1):
        caminho = caminhos[i]
        area += caminho.area
        sx   += caminho.sx
        sy   += caminho.sy
        ix   += caminho.ix
        iy   += caminho.iy
        pxy  += caminho.pxy

    # Calcula coordenadas do centróide
    x_c, y_c = [sy/area, sx/area]

    # Transfere valores para eixos centrais pelo Teorema dos eixos paralelos
    ixc = ix - area*y_c**2
    iyc = iy - area*x_c**2
    pxyc = pxy - area*x_c*y_c

    # Calcula os eixos e momentos principais de inércia

    # Valores círculo de Mohr
    r = m.sqrt(((ixc-iyc)/2)**2 + pxyc**2)
    imed = (ixc + iyc)/2
    
    # Eixos principais de Inércia:
    if abs(r) < 10**(-6)*abs(imed):
        # Trata o caso de raio muito pequeno (quando Círculo de Mohr se aproxima de um ponto)
        e1 = 0
        e2 = 90
    elif abs((ixc - iyc)) < 10**(-5)*abs(2*pxyc):
        # Trata o caso de (ixc - iyc) muito pequeno, para evitar divisão por zero
        e1 = -45
        e2 = 45
    else:
        # Caso geral
        e1 = 0.5*m.atan(-2*pxyc/(ixc - iyc))*180/m.pi
        e2 = e1 + 90        

    # Momentos principais de Inércia:
    imax = imed + r
    imin = imed - r

    # Momentos de inércia associados aos eixos 1 e 2:
    i1 = ((ixc + iyc)/2
        + (ixc - iyc)*m.cos(m.radians(2*e1))/2
        - pxyc*m.sin(m.radians(2*e1)))
    
    i2 = ((ixc + iyc)/2
        - (ixc - iyc)*m.cos(m.radians(2*e1))/2
        + pxyc*m.sin(m.radians(2*e1)))

    # Ajuste para deixar I,max sempre associado a e1
    if i1 < i2 and abs(r/imed) > 10**(-6):
        e1, e2 = e2, e1
        # ojetivo do ajuste: guardar informação de forma simples
        # porém, na função imprime_resultados, altera-se a notação para θ1 e θ2, recuperando a ordem original 
    
    return [area, sx, sy, x_c, y_c, ixc, iyc, pxyc, ix, iy, imax, imin, e1, e2, pxy]

def propriedades_parciais(caminhos, n_sup):
    """
    Calcula as propriedades geométricas parciais para cada grupo de caminhos
    (contorno externo e furos), acumulando os resultados por grupo.

    Parameters
    ----------
    caminhos : dict
        Dicionário de objetos Caminho, no formato {i: caminho[i]}, com i variando de 1 a ntot.
    n_sup : list of int
        Lista com o número do caminho final de cada grupo de caminhos:
        - n_sup[0] = número do último caminho do contorno externo
        - n_sup[1] = número do último caminho do furo 1
        - n_sup[2] = número do último caminho do furo 2
        - ...

    Returns
    -------
    dict of lists
        Cada chave do dicionário representa uma propriedade geométrica
        (como 'area', 'sx', 'ixc', 'e1', etc.), e o valor associado é uma lista
        com os valores correspondentes para cada grupo de caminhos
        (contorno externo e furos).

        As propriedades correspondem àquelas retornadas pela função `propriedades_geometricas`.
    """

    # Nomes das propriedades retornadas pela função propriedades_geometricas
    nomes_props = [
        'area', 'sx', 'sy', 'x_c', 'y_c',
        'ixc', 'iyc', 'pxyc', 'ix', 'iy',
        'imax', 'imin', 'e1', 'e2', 'pxy'
    ]

    # Inicializa um dicionário com listas vazias para cada propriedade
    props_dict = {nome: [] for nome in nomes_props}

    # Percorre cada grupo (contorno externo, furo 1, furo 2, ...)
    for j in range(len(n_sup)):
        
        # Define o número do primeiro e último caminho do grupo atual
        n_inicial = 1 if j == 0 else n_sup[j - 1] + 1
        n_final   = n_sup[j]

        # Calcula todas as propriedades geométricas para esse grupo
        props = propriedades_geometricas(caminhos, n_inicial, n_final)

        # Para cada propriedade calculada, adiciona o valor correspondente
        # na lista associada àquela propriedade no dicionário
        for nome, valor in zip(nomes_props, props):
            props_dict[nome].append(valor)

    return props_dict
    

# ----------------------------------- #
# ------- Chama função main  -------- #
# ----------------------------------- #

"""
O bloco abaixo garante que a função main() será executada apenas se este arquivo
for executado diretamente pelo Python (por exemplo, via linha de comando).
Se este arquivo for importado como um módulo em outro código, a função main()
não será executada automaticamente.
"""
if __name__ == "__main__":
    main()

# ----------------------------------- #
# -------- Funções Jupyter ---------- #
# ----------------------------------- #

def montar_tabela_interativa(nome_arquivo='dados_green.txt'):
    """
    Exibe tabelas interativas no Jupyter para entrada dos caminhos da seção (contorno e furos),
    e salva os dados no formato padrão em um arquivo .txt ao clicar em "Gerar arquivo".

    Parâmetros
    ----------
    nome_arquivo : str
        Nome do arquivo .txt que será gerado com os dados de entrada (padrão: 'dados_green.txt').

    Retorna
    -------
    None
        Exibe as tabelas e salva o arquivo ao final.
    """

    import pandas as pd
    import ipywidgets as widgets
    from IPython.display import display
    from greenpy_functions import teste_leitura_de_dados

    column_names = ['tipo', 'xi', 'yi', 'θ_i', 'θ_f', 'raio', 'xp', 'yp']

    # Widgets iniciais para número de furos
    label_furos = widgets.HTML('<b>Preencha o número de furos:</b>')
    nf_widget = widgets.BoundedIntText(value=1, min=0, max=10, description='Nº furos:', layout=widgets.Layout(width='150px'))
    gerar_inputs_button = widgets.Button(description='Confirmar', button_style='info')
    input_box = widgets.VBox([label_furos, widgets.HBox([nf_widget, gerar_inputs_button])])
    display(input_box)

    inputs_box = widgets.VBox([])
    display(inputs_box)

    tabelas_box = widgets.Output()
    display(tabelas_box)

    def confirmar_num_furos_callback(b):
        inputs_box.children = []
        nf = nf_widget.value

        # Título e widgets para número de caminhos
        label = widgets.HTML('<b>Preencha o número de caminhos:</b>')
        ncc_widget = widgets.BoundedIntText(value=3, min=1, max=100, description='Contorno:', layout=widgets.Layout(width='150px'))
        ncf_widgets = [widgets.BoundedIntText(value=2, min=0, max=100, description=f'Furo {i+1}:', layout=widgets.Layout(width='150px')) for i in range(nf)]

        gerar_tabelas_button = widgets.Button(description='Gerar tabelas', button_style='info', layout=widgets.Layout(width='150px'))

        campos_caminhos = widgets.HBox([ncc_widget] + ncf_widgets, layout=widgets.Layout(flex_wrap='wrap'))
        inputs_box.children = [label, campos_caminhos, gerar_tabelas_button]

        def gerar_tabelas_callback(bt):
            tabelas_box.clear_output()
            linhas_por_grupo = []
            blocos = []
            contador_global = 1  # Controla a numeração C1, C2, C3...
            # Mapeamento com subscritos em HTML
            col_labels_html = {
                'tipo': ' Tipo',
                'xi': ' x<sub>i</sub>',
                'yi': ' y<sub>i</sub>',
                'θ_i': ' θ<sub>i</sub>',
                'θ_f': ' θ<sub>f</sub>',
                'raio': ' Raio',
                'xp': ' x<sub>p</sub>',
                'yp': ' y<sub>p</sub>'
            }
            # Função para criar tabela com widgets de entrada
            def criar_tabela(titulo, num_rows):
                nonlocal contador_global
                linhas = []
                for _ in range(num_rows):
                    linha = [widgets.Text(layout=widgets.Layout(width='70px')) for _ in column_names]
                    linhas.append(linha)
                header = widgets.HBox([
                    widgets.Label("", layout=widgets.Layout(width='50px'))
                ] + [
                    widgets.HTML(value=f"<div style='text-align:center'>{col_labels_html[c]}</div>",
                                 layout=widgets.Layout(width='70px')) for c in column_names
                ])
                corpo = []
                for row in linhas:
                    label = widgets.Label(f"C{contador_global}", layout=widgets.Layout(width='50px'))
                    corpo.append(widgets.HBox([label] + row))
                    contador_global += 1
                box = widgets.VBox([widgets.HTML(f"<b>{titulo}</b>"), header] + corpo)
                return linhas, box

            with tabelas_box:
                
                display(widgets.HTML("<hr>"))  # ← a linha vem primeiro
                
                display(widgets.HTML(
                    "<div style='margin: 2px 0 8px 0'>"
                    "<b>Opções de tipo de caminho:</b><br>"
                    "<div style='margin-left: 12px; line-height: 1.4;'>"
                    "1 – segmento de reta<br>"
                    "2 – arco<br>"
                    "3 – parábola y = f(x)<br>"
                    "4 – parábola x = f(y)"
                    "</div>"
                    "</div>"
                ))
                
                display(widgets.HTML("<b>Preencha os dados nas tabelas abaixo:</b>"))

                # Contorno
                linhas, box = criar_tabela('Caminhos do Contorno', ncc_widget.value)
                linhas_por_grupo.append(linhas)
                blocos.append(box)

                # Furos
                for i, nf_widget_i in enumerate(ncf_widgets):
                    if nf_widget_i.value > 0:
                        linhas, box = criar_tabela(f'Caminhos do Furo {i+1}', nf_widget_i.value)
                        linhas_por_grupo.append(linhas)
                        blocos.append(box)

                btn_salvar = widgets.Button(description='Gerar arquivo de dados', button_style='primary',
                                            layout=widgets.Layout(width='250px'))
                msg = widgets.Output()

                def salvar_callback(b):
                    texto = "# Arquivo de dados gerado por entrada interativa no Jupyter\n"
                    texto += "# Formato: tipo xi yi [θi θf raio | xp yp]\n"

                    def linha_para_texto(row):
                        campos = [w.value.strip() for w in row]
                        if not campos[0]:
                            return "Erro: tipo não preenchido"
                        tipo = campos[0]
                        if tipo == '1':
                            return f"1 {campos[1]} {campos[2]}"
                        elif tipo == '2':
                            return f"2 {campos[1]} {campos[2]} {campos[3]} {campos[4]} {campos[5]}"
                        elif tipo == '3':
                            return f"3 {campos[1]} {campos[2]} {campos[6]} {campos[7]}"
                        elif tipo == '4':
                            return f"4 {campos[1]} {campos[2]} {campos[6]} {campos[7]}"
                        else:
                            return f"Erro: tipo inválido ({tipo})"

                    for grupo in linhas_por_grupo:
                        for row in grupo:
                            linha = linha_para_texto(row)
                            if linha:
                                texto += linha + "\n"
                        texto += "\n"  # separador entre grupos

                    msg.clear_output()
                    with msg:
                        try:
                            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                                f.write(texto)
                        except Exception as e:
                            print(f"❌ Erro ao salvar o arquivo '{nome_arquivo}': {e}")
                        else:
                            if teste_leitura_de_dados(nome_arquivo):
                                print(f"✅ Arquivo '{nome_arquivo}' gerado e validado com sucesso!\n")
                                try:
                                    ntot, ncc, nf, ncf, n_sup, c = leitura_de_dados(nome_arquivo)
                                    desenha_caminhos(ntot, c, size=7, fator_fontsize=1.2, fator_title=1.4, fator_axis=1,
                                                     fator_offset=1, jupyter=True, texto_caminho=True,
                                                     color=choose_color(100, 100, 240), espessura=1, markersize=4,
                                                     grid=True, st=False, savepng=False, savesvg=False)
                                except Exception as e:
                                    print(f"❌ Erro ao tentar gerar a figura: {e}")
                            else:
                                print(f"⚠️ Arquivo '{nome_arquivo}' gerado, mas contém erros de formatação.\n")
                            print(texto)

                btn_salvar.on_click(salvar_callback)

                for box in blocos:
                    display(box)
                display(btn_salvar)
                display(msg)

        gerar_tabelas_button.on_click(gerar_tabelas_callback)

    gerar_inputs_button.on_click(confirmar_num_furos_callback)

    
def conferencia_dados_jupyter(ntot, ncc, nf, ncf, n_sup, c,salvar_figura, 
                              salvar_dados_green, salvar_dados_lidos, tamanho_figura,
                              texto_caminho, tamanho_texto, offset_texto, tamanho_titulo,
                              tamanho_eixos, cor_caminhos, espessura, tamanho_pontos,
                              grade, nome_do_arquivo, nome_da_secao, unidades,
                              separador_decimal, separador_milhar,
                              preenchimento, cor_preenchimento, opacidade):
    """
    Realiza a conferência visual e textual dos dados geométricos da seção,
    incluindo visualização gráfica dos caminhos e impressão dos dados lidos.

    Esta função é voltada para uso interativo em ambiente Jupyter, permitindo ao usuário
    revisar graficamente os caminhos definidos, visualizar os dados numéricos lidos e,
    opcionalmente, salvar figuras e arquivos auxiliares para conferência futura.

    Parameters
    ----------
    ntot : int
        Número total de caminhos lidos (contorno + furos).
    ncc : int
        Número de caminhos do contorno externo.
    nf : int
        Número de furos da seção.
    ncf : list of int
        Lista contendo o número de caminhos de cada furo.
    n_sup : list of int
        Lista com o número do caminho final de cada grupo (contorno e furos).
    c : dict
        Dicionário com os objetos Caminho, no formato `{i: Caminho}`, onde `i` varia de 1 até `ntot`.
    salvar_figura : bool
        Se True, salva as figuras dos caminhos nos formatos `.png` e `.svg` dentro da pasta da seção.
    salvar_dados_green : bool
        Se True, salva uma cópia do arquivo de dados original (`.txt`) na pasta da seção.
    salvar_dados_lidos : bool
        Se True, salva os dados lidos (já processados) em um arquivo `dados_lidos.txt`.
    tamanho_figura : float
        Tamanho da figura gerada (em polegadas). Recomendado entre 3 e 20.
    texto_caminho : bool
        Indica se os rótulos dos caminhos devem ser exibidos na figura.
    tamanho_texto : float
        Fator de escala do tamanho do texto dos rótulos dos caminhos.
    offset_texto : float
        Deslocamento dos rótulos em relação à posição central dos caminhos.
    tamanho_titulo : float
        Fator de escala do título da figura.
    tamanho_eixos : float
        Fator de escala dos rótulos dos eixos x e y.
    cor_caminhos : str or tuple
        Cor utilizada para desenhar os caminhos. Pode ser um nome padrão (ex.: 'blue')
        ou um RGB customizado (ex.: choose_color(100,100,240)).
    espessura : float
        Espessura da linha dos caminhos.
    tamanho_pontos : float
        Tamanho dos marcadores dos pontos de entrada.
    grade : bool
        Se True, exibe uma grade de fundo na figura.
    nome_do_arquivo : str
        Caminho ou nome do arquivo de entrada (`.txt`) com os dados dos caminhos.
    nome_da_secao : str
        Nome da pasta/diretório onde serão salvos os arquivos gerados.
    unidades : dict
        Dicionário com as unidades adotadas.
    separador_decimal : str
        Caractere utilizado como separador decimal nos arquivos de saída (ex.: ',' ou '.').
    separador_milhar : str
        Caractere utilizado como separador de milhar nos arquivos de saída (ex.: '.' ou ',').
    preenchimento : bool
        Se True, preenche interior da seção
    cor_preecnhimento : str or tuple
        Cor utilizada para desenhar os caminhos. Pode ser um nome padrão (ex.: 'blue')
        ou um RGB customizado (ex.: choose_color(100,100,240)).
    opacidade : float
        Opacidade do preenchimento (0.0 a 1.0).

    Returns
    -------
    None
        A função apenas exibe informações e gera arquivos auxiliares conforme as opções fornecidas.
    """
    
    desenha_caminhos(ntot, c, size=tamanho_figura, fator_fontsize=tamanho_texto,
                     fator_title=tamanho_titulo, fator_axis=tamanho_eixos,
                     fator_offset=offset_texto, texto_caminho=texto_caminho,
                     color=cor_caminhos, espessura=espessura, markersize=tamanho_pontos,
                     grid=grade, jupyter=True, st=False, eixos_principais=False,
                     section_clean=False, fator_eixos_principais=2, savepng = salvar_figura,
                     savesvg = salvar_figura, pasta_destino=nome_da_secao,
                     #preenchimento
                     fill_section = preenchimento,
                     outer_fill_color = cor_preenchimento,
                     fill_alpha_main = opacidade,
                     n_sup=n_sup)

    # Imprime dados na tela para conferência:
    imprime_dados(ntot,n_sup,c,sep_dec=separador_decimal,sep_milhar=separador_milhar)  
    
    # Salva uma cópia do arquivo original de dados dentro da pasta do exemplo
    if salvar_dados_green:
        copia_arquivo_txt(nome_do_arquivo, pasta_destino = nome_da_secao)

    # Salva dados de entrada conferidos em arquivo .txt
    if salvar_dados_lidos:
        salva_saida_txt(imprime_dados, ntot, n_sup, c, pasta_destino = nome_da_secao, 
                        nome_do_arquivo="dados_lidos.txt", sep_dec=separador_decimal,
                        sep_milhar=separador_milhar)
        
def resultados_jupyter(ntot, n_sup, c, salvar_fig_inicial, salvar_fig_eixos, salvar_resultados,
                       salvar_resultados_parciais, tamanho_figura_i, cor_figura_i, espessura_figura_i,
                       eixos_ref_figura_i, tamanho_figura_e, cor_figura_e, espessura_figura_e,
                       eixos_ref_figura_e, nome_da_secao, unidades, separador_decimal, separador_milhar,
                       preenchimento_i, cor_preenchimento_i, opacidade_i,
                       preenchimento_e, cor_preenchimento_e, opacidade_e):       
    """
    Gera figuras e resultados das propriedades geométricas da seção.

    Esta função é voltada para uso interativo em ambiente Jupyter, permitindo ao usuário
    visualizar imagens da seção, imprimir os resultados na tela e, se desejado,
    salvar figuras e arquivos de resultados para conferência ou uso posterior.

    Parameters
    ----------
    ntot : int
        Número total de caminhos (contorno + furos).
    n_sup : list of int
        Lista com o número do caminho final de cada grupo de caminhos (contorno e furos).
    c : dict
        Dicionário com os objetos Caminho, no formato `{i: Caminho}`, onde `i` varia de 1 até `ntot`.
    salvar_fig_inicial : bool
        Se True, salva a figura da seção limpa nos formatos `.png` e `.svg`.
    salvar_fig_eixos : bool
        Se True, salva a figura com os eixos principais nos formatos `.png` e `.svg`.
    salvar_resultados : bool
        Se True, salva os resultados globais da seção no arquivo `resultados_green.txt`.
    salvar_resultados_parciais : bool
        Se True, salva os resultados parciais (por contorno e furos) no arquivo `resultados_parciais.txt`.
    tamanho_figura_i : float
        Tamanho da figura inicial (seção limpa), em polegadas.
    cor_figura_i : str or tuple
        Cor utilizada para desenhar os caminhos da figura limpa. Pode ser um nome padrão
        (ex.: 'black') ou RGB customizado via função `choose_color(R,G,B)`.
    espessura_figura_i : float
        Espessura da linha dos caminhos na figura da seção limpa.
    eixos_ref_figura_i : bool
        Se True, exibe os eixos de referência (x,ref e y,ref) na figura da seção limpa.
    tamanho_figura_e : float
        Tamanho da figura com eixos principais, em polegadas.
    cor_figura_e : str or tuple
        Cor utilizada para desenhar os caminhos na figura com eixos principais.
    espessura_figura_e : float
        Espessura da linha dos caminhos na figura com eixos principais.
    eixos_ref_figura_e : bool
        Se True, exibe os eixos de referência (x,ref e y,ref) na figura com eixos principais.
    nome_da_secao : str
        Nome da pasta/diretório onde serão salvos os arquivos gerados.
    unidades : dict
        Dicionário com as unidades adotadas.
    separador_decimal : str
        Caractere utilizado como separador decimal nos arquivos de saída (ex.: ',' ou '.').
    separador_milhar : str
        Caractere utilizado como separador de milhar nos arquivos de saída (ex.: '.' ou ',').
    preenchimento_i ou e : bool
        Se True, preenche interior da seção (i - figura inicial limpa, e - figura com eixos).
    cor_preenchimento_i ou e : str or tuple
        Cor utilizada para desenhar os caminhos. Pode ser um nome padrão (ex.: 'blue')
        ou um RGB customizado (ex.: choose_color(100,100,240)).
    opacidade_i ou e : float
        Opacidade do preenchimento (0.0 a 1.0).

    Returns
    -------
    None
        A função apenas exibe os resultados no Jupyter e gera arquivos conforme as opções fornecidas.
    """
    # Desenha seção limpa
    desenha_caminhos(ntot, c, size=tamanho_figura_i, espessura = espessura_figura_i, color = cor_figura_i,
                     eixos_ref=eixos_ref_figura_i, texto_caminho=False, markersize=0, grid=False,
                     jupyter=True, section_clean=True, pasta_destino = nome_da_secao,
                     savepng = salvar_fig_inicial, savesvg = salvar_fig_inicial,
                     #preenchimento
                     fill_section = preenchimento_i,
                     outer_fill_color = cor_preenchimento_i,
                     fill_alpha_main = opacidade_i,
                     n_sup=n_sup)              

    # Imprime resultados na tela
    imprime_resultados(*propriedades_geometricas(c), unidades,
                       sep_dec=separador_decimal, sep_milhar=separador_milhar)
    if salvar_resultados:
        # Salva resultados em arquivo .txt
        salva_saida_txt(imprime_resultados, *propriedades_geometricas(c), unidades,
                        pasta_destino = nome_da_secao, nome_do_arquivo="resultados_green.txt",
                        sep_dec=separador_decimal, sep_milhar=separador_milhar)                   

    # Desenha seção com eixos
    desenha_caminhos(ntot, c, size=tamanho_figura_e, texto_caminho=False, markersize=0,
                     eixos_ref=eixos_ref_figura_e, jupyter=True, color = cor_figura_e,
                     espessura = espessura_figura_e, eixos_principais=True,
                     fator_eixos_principais=2, pasta_destino = nome_da_secao,
                     savepng = salvar_fig_eixos, savesvg = salvar_fig_eixos,
                     #preenchimento
                     fill_section = preenchimento_e,
                     outer_fill_color = cor_preenchimento_e,
                     fill_alpha_main = opacidade_e,
                     n_sup=n_sup)     
    
    if salvar_resultados_parciais:             
        # Salva resultados parciais (separados em contorno e furos) em arquivo .txt
        salva_saida_txt(imprime_resultados_parciais, c, n_sup, unidades,
                        pasta_destino = nome_da_secao, nome_do_arquivo="resultados_parciais.txt",
                        sep_dec=separador_decimal, sep_milhar=separador_milhar)