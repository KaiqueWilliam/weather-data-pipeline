# weather-data-pipeline

Este projeto consiste em um pipeline de dados ETL (Extração, Transformação e Carga) automatizado para coletar, tratar e armazenar dados meteorológicos em tempo real da cidade de São Paulo, utilizando a API do OpenWeatherMap. 

O fluxo é totalmente orquestrado pelo Apache Airflow rodando em ambiente Docker, garantindo que os dados sejam atualizados de forma consistente e escalável.

## 🚀 Tecnologias e Ferramentas

* **Linguagem:** Python 3.11.
* **Orquestração:** Apache Airflow 3.1.7.
* **Manipulação de Dados:** Pandas.
* **Banco de Dados:** PostgreSQL 16.
* **Interface de Banco de Dados:** SQLAlchemy e Psycopg2-binary.
* **Infraestrutura:** Docker e Docker Compose.
* **Gerenciamento de Dependências:** UV / Pyproject.toml.
* **Cache e Mensageria:** Redis 7.2.

## 🏗️ Arquitetura do Pipeline (ETL)

O workflow é definido através de uma DAG (Directed Acyclic Graph) no Airflow com as seguintes etapas:

1.  **Extract (Extração):**
    * Consome dados da API OpenWeatherMap.
    * Salva a resposta bruta em formato JSON em `data/weather_data.json`.
2.  **Transform (Transformação):**
    * Lê o arquivo JSON e utiliza `pd.json_normalize` para estruturar os dados.
    * Realiza o tratamento da coluna aninhada `weather` para extrair ID, descrição e ícone.
    * Converte timestamps Unix (`dt`, `sunrise`, `sunset`) para o fuso horário `America/Sao_Paulo`.
    * Limpa colunas desnecessárias e renomeia os campos para um padrão SQL amigável.
3.  **Load (Carga):**
    * Conecta-se ao banco de dados PostgreSQL via SQLAlchemy.
    * Insere os dados processados na tabela `sp_weather` com estratégia de *append*.

## 📁 Estrutura do Repositório

``text
├── dags/
│   └── weather_dag.py          # Definição das tasks e agendamento do Airflow
├── src/
│   ├── extract_weather_data.py  # Script de requisição à API
│   ├── transform_data.py        # Lógica de limpeza e tratamento (Pandas)
│   └── load_data.py             # Lógica de conexão e carga no banco
├── config/
│   └── .env                    # Variáveis de ambiente (Segurança)
├── data/                       # Arquivos temporários (JSON e Parquet)
├── notebooks/                  # Análise exploratória inicial (Jupyter)
├── docker-compose.yaml         # Configuração de containers e volumes
├── pyproject.toml              # Especificação de dependências
└── LICENSE                     # Informações de licenciamento (MIT)

🔧 Pré-requisitos

Para rodar este projeto, você precisará de:

    Docker e Docker Compose instalados.

    Uma API Key válida do OpenWeatherMap.

    Python 3.11 (caso deseje rodar scripts de teste fora do Docker).

    Conexão com a internet para extração de dados e download de imagens Docker.

🏃 Como Executar
1. Configuração do Arquivo .env

Crie um arquivo chamado .env dentro da pasta config/ (ou na raiz, dependendo da sua preferência de volume) com as seguintes chaves:
Snippet de código

user=seu_usuario_postgres
password=sua_senha_postgres
database=nome_do_seu_banco
API_KEY=sua_chave_da_api_openweathermap

2. Inicialização do Docker

No terminal, na raiz do projeto, execute o comando para subir todos os serviços (Airflow, Postgres, Redis):
Bash

docker-compose up -d

3. Acesso ao Airflow

Abra o navegador e acesse http://localhost:8080.

    Login padrão: airflow / Senha padrão: airflow.

    Ative a DAG weather_pipeline no painel principal.

    O pipeline está configurado para rodar de hora em hora automaticamente.

4. Verificação dos Dados

Os dados transformados estarão disponíveis na tabela sp_weather do banco de dados configurado.
