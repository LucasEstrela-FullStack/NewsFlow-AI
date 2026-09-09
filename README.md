# 🌊 NewFlow

<p align="center">
  <strong>AI-Powered News Aggregator</strong>
</p>

<p align="center">
  Agregação, processamento e personalização inteligente de notícias utilizando Inteligência Artificial.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-API-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Render-Deploy-46E3B7?style=for-the-badge&logo=render&logoColor=black" alt="Render">
</p>

---

## 📖 Sobre o projeto

**NewFlow** é uma plataforma inteligente de agregação de notícias desenvolvida para coletar conteúdos de diferentes fontes, processá-los utilizando Inteligência Artificial e entregar informações relevantes de forma organizada e personalizada.

O projeto combina **coleta automatizada de dados, processamento com LLMs, persistência em PostgreSQL, geração de resumos, classificação de conteúdo e automação de envio de e-mails**.

A aplicação foi desenvolvida com uma abordagem próxima de um ambiente real de produção, utilizando **Docker** para desenvolvimento local e **Render** para implantação.

---

## 🎯 Objetivos

O NewFlow foi criado com os seguintes objetivos:

* Coletar notícias e conteúdos de diferentes fontes.
* Automatizar o processamento das informações.
* Utilizar IA para interpretar e resumir conteúdos.
* Classificar notícias de acordo com seus temas.
* Armazenar os dados de forma estruturada.
* Personalizar conteúdos de acordo com o perfil do usuário.
* Gerar resumos diários.
* Automatizar o envio de informações por e-mail.
* Aplicar conceitos de arquitetura de software e pipelines de dados.
* Disponibilizar a aplicação em um ambiente de produção.

---

## ✨ Funcionalidades

### 📰 Coleta de notícias

O NewFlow pode trabalhar com diferentes fontes de conteúdo, permitindo centralizar informações em uma única aplicação.

Exemplos:

* YouTube
* Sites de notícias
* Feeds
* APIs
* Artigos
* Outras fontes compatíveis com o pipeline

---

### 🤖 Processamento com Inteligência Artificial

Os conteúdos coletados são enviados para processamento utilizando modelos de linguagem.

A IA pode:

* Interpretar o conteúdo.
* Identificar informações relevantes.
* Classificar artigos.
* Gerar resumos.
* Extrair informações importantes.
* Adaptar o conteúdo ao perfil do usuário.

---

### 📝 Resumos automáticos

O sistema transforma conteúdos extensos em informações mais objetivas.

Fluxo:

```text
Artigo original
      ↓
Processamento
      ↓
Análise com IA
      ↓
Extração das informações principais
      ↓
Resumo
      ↓
Armazenamento
```

---

### 👤 Personalização

O NewFlow permite considerar preferências e interesses do usuário para selecionar conteúdos mais relevantes.

Exemplo:

```text
Perfil do usuário

Interesses:
- Inteligência Artificial
- Cloud Computing
- Tecnologia
- Desenvolvimento de Software

            ↓

Conteúdos coletados

            ↓

Classificação com IA

            ↓

Conteúdos relevantes

            ↓

Resumo personalizado
```

---

### 📧 Resumo diário

O sistema pode gerar um **Daily Digest**, reunindo os principais conteúdos selecionados para o usuário.

Exemplo:

```text
🌊 NewFlow Daily

5 notícias relevantes para você

01. Nova tecnologia de IA...
02. AWS anuncia...
03. Novo framework...
04. OpenAI apresenta...
05. Tendências em Cloud...

Resumo gerado por IA.
```

---

## 🧠 Arquitetura

A arquitetura inicial do NewFlow segue um pipeline de processamento:

```text
                  ┌──────────────────────┐
                  │      FONTES          │
                  │                      │
                  │ YouTube / Sites / RSS│
                  │ APIs / Artigos       │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │      COLLECTOR       │
                  │                      │
                  │ Scraping / APIs      │
                  │ Extração de conteúdo │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    AI PROCESSING     │
                  │                      │
                  │ Classificação        │
                  │ Resumo               │
                  │ Extração             │
                  │ Análise              │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     PostgreSQL       │
                  │                      │
                  │ Notícias             │
                  │ Usuários             │
                  │ Perfis               │
                  │ Resumos              │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    AGENT / PIPELINE  │
                  │                      │
                  │ Seleção personalizada│
                  │ Geração do Digest    │
                  └──────────┬───────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
             ┌─────────────┐   ┌─────────────┐
             │   E-MAIL    │   │  APLICAÇÃO  │
             │ Daily Digest│   │   / API     │
             └─────────────┘   └─────────────┘
```

---

## 🛠️ Tecnologias

### Backend

* Python
* Flask
* OpenAI API
* Pandas
* Requests
* BeautifulSoup
* PostgreSQL

### Inteligência Artificial

* OpenAI
* Large Language Models
* Prompt Engineering
* Text Classification
* Text Summarization

### Banco de dados

* PostgreSQL
* SQL
* Database migrations

### Infraestrutura

* Docker
* Docker Compose
* Render

### Desenvolvimento

* Git
* GitHub
* Python Virtual Environment
* Environment Variables

---

## 📦 Estrutura do projeto

A estrutura pode ser organizada da seguinte maneira:

```text
newflow/
│
├── app/
│   ├── __init__.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── agents/
│   │   ├── aggregator.py
│   │   └── email_agent.py
│   │
│   ├── scrapers/
│   │   ├── youtube.py
│   │   ├── openai.py
│   │   └── anthropic.py
│   │
│   ├── services/
│   │   ├── pipeline.py
│   │   ├── summarizer.py
│   │   └── classifier.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── migrations/
│   │
│   └── utils/
│       └── helpers.py
│
├── tests/
│
├── scripts/
│   └── seed.py
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

---

# 🚀 Instalação

## Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

* Python 3.11+
* Docker
* Docker Compose
* Git
* Uma API Key da OpenAI
* PostgreSQL, caso não utilize Docker

---

## 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/newflow.git

cd newflow
```

---

## 2. Crie o ambiente virtual

### Windows

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuração das variáveis de ambiente

Crie um arquivo:

```text
.env
```

Utilize o `.env.example` como referência.

Exemplo:

```env
OPENAI_API_KEY=your_openai_api_key

DATABASE_URL=postgresql://postgres:<POSTGRES_PASSWORD>@localhost:5433/newflow

POSTGRES_DB=newflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<choose-a-local-password>

FLASK_ENV=development
FLASK_DEBUG=1

SECRET_KEY=your_secret_key

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_email
SMTP_PASSWORD=your_password
```

> ⚠️ Nunca envie o arquivo `.env` para o GitHub.

---

# 🐳 Executando com Docker

O NewFlow utiliza Docker para facilitar a configuração do ambiente de desenvolvimento.

Execute:

```bash
docker compose up --build
```

Para iniciar somente o PostgreSQL local:

```bash
docker compose up -d database
```

Para executar em segundo plano:

```bash
docker compose up -d --build
```

Verifique os containers:

```bash
docker compose ps
```

Para visualizar os logs:

```bash
docker compose logs -f
```

Para parar os serviços:

```bash
docker compose down
```

---

# 🗄️ Banco de dados

O projeto utiliza PostgreSQL para armazenar as informações processadas.

Exemplo conceitual de entidades:

```text
User
 │
 ├── Profile
 │
 └── Preferences

Article
 │
 ├── Source
 ├── Category
 ├── Summary
 └── ProcessingStatus

Digest
 │
 ├── User
 └── Articles
```

### Principais informações armazenadas

* Usuários
* Fontes
* Artigos
* Conteúdo original
* Resumos
* Categorias
* Preferências
* Histórico de processamento
* Daily Digests

---

# 🔄 Pipeline de processamento

O pipeline é responsável por transformar conteúdos brutos em informações úteis.

```text
1. Coleta
   ↓
2. Validação
   ↓
3. Extração
   ↓
4. Limpeza
   ↓
5. Armazenamento
   ↓
6. Processamento com IA
   ↓
7. Classificação
   ↓
8. Resumo
   ↓
9. Personalização
   ↓
10. Daily Digest
   ↓
11. Envio
```

---

# 📰 Coleta de conteúdo

Cada fonte pode possuir um serviço específico.

Exemplo:

```text
scrapers/
│
├── youtube.py
├── openai.py
└── anthropic.py
```

Cada scraper é responsável por:

1. Acessar a fonte.
2. Encontrar novos conteúdos.
3. Extrair os dados.
4. Normalizar as informações.
5. Retornar os conteúdos para o pipeline.

---

# 🤖 Inteligência Artificial

O NewFlow utiliza LLMs para processar os conteúdos coletados.

Um fluxo simplificado:

```text
Conteúdo
   ↓
Prompt
   ↓
LLM
   ↓
Resposta estruturada
   ↓
Validação
   ↓
Banco de dados
```

A IA pode produzir informações como:

```json
{
  "title": "Título da notícia",
  "category": "Technology",
  "summary": "Resumo gerado pela IA",
  "relevance": 0.92,
  "topics": [
    "Artificial Intelligence",
    "Cloud",
    "Software"
  ]
}
```

---

# 🧩 Agentes

O projeto possui uma arquitetura preparada para agentes especializados.

### Aggregator Agent

Responsável por:

* Analisar os conteúdos disponíveis.
* Selecionar informações relevantes.
* Agrupar conteúdos relacionados.
* Preparar o resumo diário.

### Email Agent

Responsável por:

* Receber o conteúdo processado.
* Montar o Daily Digest.
* Formatar o e-mail.
* Realizar o envio.

Fluxo:

```text
Articles
   ↓
Aggregator Agent
   ↓
Personalized Digest
   ↓
Email Agent
   ↓
User
```

---

# 📊 Personalização

O usuário pode possuir preferências utilizadas pelo sistema para determinar a relevância dos conteúdos.

Exemplo:

```json
{
  "user": "Lucas",
  "interests": [
    "AI",
    "Cloud",
    "Software Engineering",
    "Cybersecurity"
  ]
}
```

O pipeline utiliza essas informações para melhorar a seleção dos conteúdos.

---

# 📧 Daily Digest

O Daily Digest reúne os principais conteúdos identificados pelo sistema.

Exemplo:

```text
┌──────────────────────────────────────┐
│            🌊 NewFlow                │
│          Daily Intelligence          │
├──────────────────────────────────────┤
│                                      │
│ 🤖 Artificial Intelligence            │
│                                      │
│ Nova tecnologia é apresentada...     │
│                                      │
│ ☁️ Cloud                             │
│                                      │
│ Empresa anuncia nova solução...      │
│                                      │
│ 💻 Software                          │
│                                      │
│ Novo framework ganha popularidade... │
│                                      │
└──────────────────────────────────────┘
```

---

# 🧪 Testes

Execute os testes com:

```bash
pytest
```

Para executar com informações detalhadas:

```bash
pytest -v
```

---

# 🔎 Qualidade de código

Durante o desenvolvimento, o projeto busca manter:

* Separação de responsabilidades.
* Código modular.
* Variáveis de ambiente.
* Tratamento de erros.
* Validação de dados.
* Testes automatizados.
* Logs.
* Estrutura preparada para escala.

---

# 🌐 Deploy

O NewFlow pode ser implantado utilizando **Render**.

Arquitetura de produção:

```text
             GitHub
                │
                ▼
             Render
                │
       ┌────────┴────────┐
       ▼                 ▼
   Web Service       PostgreSQL
       │
       ▼
    NewFlow
       │
       ▼
   OpenAI API
```

---

## Deploy com Render

Fluxo básico:

```text
GitHub Repository
       ↓
Create Web Service
       ↓
Configure Environment Variables
       ↓
Configure Build Command
       ↓
Configure Start Command
       ↓
Deploy
```

Variáveis sensíveis devem ser configuradas diretamente no ambiente da aplicação.

### Job diário no Render

O Blueprint também define o Cron Job `newflow-ai-daily-digest`. Ele executa
`python -m app.jobs.daily_digest` uma vez por dia às **12:00 UTC** e encerra
após enviar o digest.

Configure as variáveis abaixo diretamente no serviço de Cron Job no Render:

```text
DATABASE_URL
SMTP_HOST
SMTP_PORT
SMTP_USERNAME
SMTP_PASSWORD
SMTP_SENDER
DAILY_DIGEST_RECIPIENT
DAILY_DIGEST_INTERESTS
YOUTUBE_CHANNEL_IDS
```

`DAILY_DIGEST_INTERESTS` e `YOUTUBE_CHANNEL_IDS` usam valores separados por
vírgula. O segundo é opcional. Para testar uma execução fora do horário, use
**Trigger Run** na página do Cron Job no painel do Render.

---

# 🔒 Segurança

Boas práticas adotadas:

* API Keys armazenadas em variáveis de ambiente.
* `.env` ignorado pelo Git.
* Não armazenar credenciais no código.
* Validação das entradas.
* Tratamento de exceções.
* Controle de acesso ao banco.
* Separação entre desenvolvimento e produção.

---

# 📈 Evoluções planejadas

O NewFlow foi inicialmente desenvolvido como um agregador de notícias, mas sua arquitetura permite evoluções futuras.

### Roadmap

* [x] Coleta de conteúdos
* [x] Pipeline de processamento
* [x] Integração com IA
* [x] PostgreSQL
* [x] Geração de resumos
* [x] Classificação de conteúdos
* [x] Perfil de usuário
* [x] Daily Digest
* [x] Envio de e-mail
* [x] Docker
* [ ] Interface web
* [ ] Autenticação
* [ ] Dashboard
* [ ] Busca inteligente
* [ ] Embeddings
* [ ] RAG
* [ ] PostgreSQL + pgvector
* [ ] Recomendações inteligentes
* [ ] Mais fontes de dados
* [ ] Observabilidade
* [ ] CI/CD
* [ ] Testes de integração
* [ ] Escalabilidade horizontal

---

# 💡 Possíveis evoluções de arquitetura

Em uma segunda fase, o NewFlow poderá evoluir para:

```text
                    ┌───────────────┐
                    │    Sources    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Collector   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ AI Processing │
                    └───────┬───────┘
                            ↓
                 ┌──────────────────────┐
                 │ PostgreSQL + pgvector│
                 └──────────┬───────────┘
                            ↓
                    ┌───────────────┐
                    │   RAG Agent   │
                    └───────┬───────┘
                            ↓
                 ┌──────────┴──────────┐
                 ↓                     ↓
          ┌─────────────┐       ┌─────────────┐
          │  Dashboard  │       │    Email    │
          └─────────────┘       └─────────────┘
```

---

# 📚 Conceitos demonstrados

Este projeto demonstra conhecimentos em:

### Backend

* APIs
* Flask
* Python
* REST
* Modularização
* Integração de serviços

### Inteligência Artificial

* LLMs
* Prompt Engineering
* Classificação
* Sumarização
* Agentes
* Personalização

### Dados

* PostgreSQL
* SQL
* Data Processing
* Pipelines
* Normalização

### DevOps

* Docker
* Docker Compose
* Environment Variables
* Deploy
* Cloud Infrastructure

### Software Engineering

* Arquitetura
* Separação de responsabilidades
* Testes
* Tratamento de erros
* Versionamento
* Código modular

---

# 🗺️ Fluxo completo

```text
                 ┌─────────────┐
                 │   Sources   │
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │  Scrapers   │
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │  Pipeline   │
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │ PostgreSQL  │
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │     LLM     │
                 └──────┬──────┘
                        ↓
              ┌───────────────────┐
              │ Classification    │
              │ + Summarization   │
              └─────────┬─────────┘
                        ↓
                 ┌─────────────┐
                 │ User Profile│
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │ Aggregator  │
                 │    Agent    │
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │ Daily Digest│
                 └──────┬──────┘
                        ↓
                 ┌─────────────┐
                 │ Email Agent │
                 └──────┬──────┘
                        ↓
                      User
```

---

# 📸 Screenshots

> Em desenvolvimento.

Futuramente serão adicionadas imagens da aplicação, incluindo:

* Dashboard
* Notícias
* Resumos
* Perfil do usuário
* Daily Digest
* Monitoramento do pipeline

---

# 🔗 Projeto

**NewFlow — AI News Aggregator**

Status:

> 🚧 Em desenvolvimento

---

# 📄 Licença

Este projeto está licenciado sob a **MIT License**.

Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.

---

# 👨‍💻 Autor

Desenvolvido por **Lucas Estrela**.

<p align="left">
  <a href="https://github.com/LucasEstrela-FullStack">
    <img src="https://img.shields.io/badge/GitHub-LucasEstrela--FullStack-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

---

<p align="center">
  🌊 <strong>NewFlow</strong>
  <br>
  <sub>Transformando informação em inteligência.</sub>
</p>
