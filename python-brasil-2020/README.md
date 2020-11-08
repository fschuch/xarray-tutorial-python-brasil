# Xarray, estruturas para dados multidimensionais

Desejo boas-vindas ao tutorial **Xarray**.

Xarray é um pacote Python de código aberto que visa tornar o trabalho com arranjos de dados catalogados uma tarefa simples, eficiente e até mesmo divertida!

Xarray introduz *labels* (mapeamento, rótulo, catálogo) como forma de expressar dimensões, coordenadas e atributos construidos acima de arranjos brutos do tipo [NumPy](https://numpy.org/),
o que permite um fluxo de trabalho e desenvolvimento mais intuitivo, conciso e a prova de erros.
O pacote inclui uma biblioteca grande e crescente de funções aplicadas para análises e visualização com essas estruturas de dados.

Xarray é inspirado e inclusive toma várias funcionalidades emprestadas do [pandas](https://pandas.pydata.org/), o popular pacote para manipulação de dados tabelados.
Também é especialmente adaptado para funcionar com [arquivos netCDF](http://www.unidata.ucar.edu/software/netcdf), que foram a fonte do modelo de dados em Xarray, além de integrar-se perfeitamente com [Dask](http://dask.org/) para computação paralela.

## Configurando o Tutorial

Esse tutorial foi projetado para rodar no [Binder](https://mybinder.org/).
O serviço permite executar totalmente na nuvem, nenhuma instalação extra é necessária.
Para tanto, basta clicar [aqui](https://mybinder.org/v2/gh/fschuch/xarray-tutorial-python-brasil/master?urlpath=lab/python-brasil-2020):
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fschuch/xarray-tutorial-python-brasil/master?urlpath=lab/python-brasil-2020)

Se você prefere instalar o tutorial localmente, siga os seguintes passos:

1. Clone o repositório:

   ```
   git clone https://github.com/fschuch/xarray-tutorial-python-brasil
   ```

1. Instale o ambiente. O repositório inclui um arquivo `environment.yaml` no subdiretório `.binder` que contém uma lista de todos os pacotes necessários para executar esse tutorial.
   Para instalá-los usando conda, use o comando:

   ```
   conda env create -f .binder/environment.yml
   conda activate xarray
   ```

1. Inicie uma seção Jupyter:

   ```
   jupyter lab
   ```

## Material complementar

1. Referências

    - [Documentação](http://xarray.pydata.org/en/stable/)
    - [Overview: Why xarray?](http://xarray.pydata.org/en/stable/why-xarray.html)
    - [Repositório do Xarray](https://github.com/pydata/xarray)

1. Peça ajuda:

    - Use a seção [python-xarray](https://stackoverflow.com/questions/tagged/python-xarray) no StackOverflow
    - [GitHub Issues](https://github.com/pydata/xarray/issues) para reportar bugs e requisitar novas funcionalidades


## Estrutura do Tutorial

O material é composto por múltiplos Jupyter Notebooks. Eles, por sua vez, são compostos por uma mistura de código, texto, visualizações e exercícios.

Se essa é sua primeira experiência com JupyterLab, não se preocupe, ele é bastante simular com o Jupyter Notebook clássico. Se essa é a sua primeira vez com um Notebook, aqui vai uma introdução rápida:

1. Existem células em dois modos: comando e edição;
1. A partir do modo de comando, precione `Enter` para editar uma célular (assim como essa célula em Markdown);
1. Do modo de edição, precione `Esc` para retornar ao modo de comando;
1. Precione `Shift + Enter` para executar a célula e mover o cursor para a célula seguinte;
1. A barra de ferramentas contém botões para executar, converter, criar, quebrar e mesclar células.

O conteúdo abordado será o seguinte:

1. [Introdução + Estruturas para dados Multidimensionais](./01_estruturas_de_dados_e_io.ipynb)
1. [Trabalhando com dados mapeados](./02_trabalhando_com_dados_mapeados.ipynb)
1. [Computação com Xarray](03_calculos_com_xarray.ipynb)
1. [Gráficos e Visualização](04_graficos_e_visualizacao.ipynb)
1. [Introdução ao Dask](05_introducao_ao_dask.ipynb)
1. [Dask e Xarray para computação paralela](06_xarray_e_dask.ipynb)