# Integrantes do trabalho

- Arthur Vinicius Santos Silva RA:1903665
- Larissa Ionafa RA:1903166
- Lucas da Silva Santos RA:1904201

:information_source: **Se você utilizada Windows, substitua no comando ```python3``` por ```python```**

## Como rodar o projeto:

### 1. Caso deseje utilizar um ambiente virtual, você pode executar o seguinte comando:

```shell
python3 -m venv myenv
```
Neste comando, myenv é o nome do ambiente virtual que você está criando. Você pode escolher um nome que melhor se adapte ao seu projeto.

Para começar a usar este ambiente virtual, você precisa ativá-lo. O comando para ativar o ambiente depende do seu sistema operacional:

No Windows:

```shell
myenv\Scripts\activate
```

No Unix ou MacOS:

```shell
source myenv/bin/activate
```

### 2. Instalar requerimentos

```shell
pip install -r requirements.txt
```

### 3. Comando para executar spider e salvar o retorno:

```shell
# scrapy crawl <<nome-spider>> -O nome-do-arquivo.tipo-arquivo(csv,json,etc...)
cd 3_scripts/scrapy/ac02/ac02
scrapy crawl promocoes-jogos -O ../../../../0_bases_originais/original.csv
```

### 4. Criar Banco de dados da aplicação Streamlit

Após isso, rodar do arquivo: `3_scripts/preparacao_dos_dados_esqueleto_v2.ipynb`

Dentro do script ao fim, haverão os comandos para criar a base de dados usando os dados extraídos tratados.

O tópico relacionado a criação do Banco de Dados é: `AC5 - Salvando dados no Banco de dados SQLite3`

### 5. Rodar o streamlit

```shell
cd ../../../../
streamlit run streamlit_script.py
```

:warning: **É necessário manter o servidor do streamlit executando para os seguintes passos**

### 6. Executar script da aplicação Flask

:information_source: **O banco de usuários é criado automaticamente quando a aplicação Flask é iniciada**


```shell
python3 app.py
```