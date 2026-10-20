# GreenPy Section

Software educacional desenvolvido em Python para determinar propriedades geométricas de seções planas por meio do Teorema de Green. Permite analisar seções com contornos compostos por segmentos de reta, arcos de circunferência e parábolas, incluindo seções com furos.

Este repositório disponibiliza temporariamente o código para avaliação de artigo submetido à revista RENOTE, em outubro de 2026. Por razões éticas, a identificação dos autores e das instituições foi omitida nesta versão, a fim de preservar o anonimato durante a avaliação por pares em sistema duplo-cego. A autoria será informada posteriormente, caso o artigo seja aceito para publicação.

## Funcionalidades

- Cálculo da área e dos momentos estáticos de primeira ordem.
- Determinação das coordenadas do centro geométrico.
- Cálculo dos momentos de inércia de área e do produto de inércia em relação aos eixos de referência e centrais.
- Determinação dos momentos e dos eixos centrais principais de inércia.
- Representação gráfica da seção, dos caminhos de seu contorno e dos eixos.
- Exportação de resultados em arquivos de texto e de figuras em PNG e SVG.

## Arquivos do repositório

| Arquivo | Descrição |
| --- | --- |
| `greenpy_functions.py` | Funções de cálculo, representação gráfica e execução pela linha de comando. |
| `greenpy_streamlit.py` | Interface web desenvolvida com Streamlit. |
| `GreenPy.ipynb` | Notebook Jupyter com orientações e parâmetros de configuração. |
| `requirements.txt` | Dependências para execução do programa e de suas interfaces. |

## Acesso à versão web

O software pode ser utilizado diretamente pelo navegador, sem necessidade de instalação no computador, pelo endereço:

[https://greenpy-section-2026.streamlit.app/](https://greenpy-section-2026.streamlit.app/)

## Instalação local

Caso o usuário prefira instalar e utilizar o software localmente, é necessário ter o Python instalado. Baixe os arquivos em **Code → Download ZIP**, descompacte a pasta e abra um terminal nessa pasta para instalar as dependências:

```bash
python -m pip install -r requirements.txt
```

Mantenha os arquivos do programa na mesma pasta.

## Formas de utilização local

### Interface Streamlit

No terminal, dentro da pasta do programa, execute:

```bash
python -m streamlit run greenpy_streamlit.py
```

Escolha uma das abas: **Tabela dinâmica**, **Inserir texto** ou **Enviar arquivo**. Após inserir os dados, clique em **Conferir dados** e em **Calcular resultados**. Os resultados e as figuras podem ser baixados pela interface.

### Linha de comando

Execute:

```bash
python greenpy_functions.py
```

Siga as perguntas no terminal para digitar os dados ou ler um arquivo `.txt`. Os resultados e as figuras são salvos na pasta definida pelo usuário.

### Notebook Jupyter

Abra `GreenPy.ipynb` em um ambiente Jupyter e execute as células na ordem apresentada. Conclua a entrada de dados antes de executar a célula de conferência.

O parâmetro `e` define a forma de entrada:

| Valor | Forma de entrada |
| --- | --- |
| `e = 1` | Leitura de um arquivo `.txt` existente. |
| `e = 2` | Digitação em resposta às perguntas. Opção padrão desta versão. |
| `e = 3` | Preenchimento de tabelas interativas. |

Se necessário, instale e inicie o Jupyter Notebook no mesmo ambiente Python:

```bash
python -m pip install notebook
jupyter notebook
```

## Dados de entrada

Divida o contorno da seção em caminhos simples, utilizando o mesmo sistema de eixos de referência.<br>
↶ Contorno: sentido anti-horário.<br>
↷ Furos: sentido horário.

Tipos de caminhos:<br>
`1 – segmento de reta`<br>
`2 – arco`<br>
`3 – parábola y=f(x)`<br>
`4 – parábola x=f(y)`

Caso se opte pela entrada de dados por arquivo de texto:

Insira uma linha de dados por caminho, no formato:<br>
`tipo xi yi [θi θf raio | xp yp]`

Linhas em branco separam grupos de caminhos (contorno ou furos).<br>
Linhas iniciadas por `#` são comentários e são ignoradas pelo programa.

O arquivo de dados, como `dados_green.txt`, é específico de cada seção e pode ser fornecido pelo usuário ou gerado pelo programa.

### Exemplo

Quadrado de lado 10 com furo circular central de raio 1 e origem dos eixos no vértice inferior esquerdo:

```text
1 0 0
1 10 0
1 10 10
1 0 10

2 6 5 360 0 1
```

Na interface Streamlit, cole o exemplo em **Inserir texto** e clique em **Salvar texto**, **Conferir dados** e **Calcular resultados**.

Mais exemplos podem ser consultados na pasta específica.

## Licença e autoria

O código-fonte do GreenPy Section é disponibilizado sob a licença [Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.pt-br).

São permitidos o uso, a cópia, a modificação e o compartilhamento para fins não comerciais, mediante atribuição de crédito e indicação de eventuais alterações. As adaptações compartilhadas devem ser distribuídas sob a mesma licença.

### Autoria e citação

Durante a submissão à revista RENOTE, a identificação dos autores permanece temporariamente omitida para preservar a avaliação por pares em sistema duplo-cego. Nesse período, a atribuição de crédito deve indicar o nome GreenPy Section e o endereço deste repositório.

Caso o artigo seja aceito para publicação, a autoria será informada neste repositório. A partir dessa divulgação, as novas referências deverão identificar os autores.

Em trabalhos acadêmicos, cite o software e, quando disponível, o artigo correspondente.
