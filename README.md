# NewFlow AI

Agregador de notícias de IA que coleta feeds públicos, prioriza conteúdos por
interesse, registra artigos no PostgreSQL e envia um digest diário por e-mail.

O projeto é aberto para execução local e pode ser adaptado para outros
provedores de banco, agendamento e e-mail sem acoplar as regras de negócio à
infraestrutura.

## Funcionalidades atuais

- Coleta notícias recentes dos feeds RSS da OpenAI e Anthropic.
- Coleta metadados e transcrições de canais do YouTube, quando configurados.
- Persiste artigos sem duplicação no PostgreSQL.
- Ordena artigos pelos interesses do destinatário e gera um digest em Markdown.
- Entrega o digest por SMTP sobre SSL.
- Impede reenvio para o mesmo destinatário no mesmo dia e registra o resultado
  como `sent` ou `failed`.
- Disponibiliza `GET /health` para verificar a disponibilidade do processo web.

## Arquitetura

```text
RSS / YouTube
      |
      v
CollectionPipeline --> PostgreSQL
      |
      v
ArticleAggregator --> DigestService --> SMTP
      |
      v
Digest delivery history
```

As regras de aplicação dependem de portas pequenas; os adaptadores de RSS,
YouTube, SQLAlchemy e SMTP ficam nas bordas. A composição das dependências fica
em `app/jobs/daily_digest.py`.

## Requisitos

- Python 3.11 ou superior
- Docker e Docker Compose (recomendado para o PostgreSQL local)
- Uma conta SMTP que aceite SSL na porta configurada

## Execução local

Clone o repositório e crie o ambiente virtual:

```bash
git clone https://github.com/LucasEstrela-FullStack/NewsFlow-AI.git
cd NewsFlow-AI
python -m venv .venv
```

Ative o ambiente e instale as dependências:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

```bash
# Linux/macOS
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Crie o arquivo de configuração local a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Preencha `POSTGRES_PASSWORD` e use a mesma senha no trecho
`<POSTGRES_PASSWORD>` de `DATABASE_URL`. Para executar o digest, também
preencha as variáveis `SMTP_*`, `DAILY_DIGEST_RECIPIENT` e
`DAILY_DIGEST_INTERESTS`. Nunca versione o arquivo `.env`.

Inicie apenas o banco de dados local:

```bash
docker compose up -d database
```

Inicie a aplicação web e consulte a saúde do processo:

```bash
python run.py
curl http://127.0.0.1:5000/health
```

Resposta esperada:

```json
{"service":"newflow","status":"ok"}
```

## Digest diário

O comando abaixo executa uma coleta e tenta enviar um digest. Ele cria as
tabelas necessárias se ainda não existirem.

```bash
python -m app.jobs.daily_digest
```

`YOUTUBE_CHANNEL_IDS` é opcional e aceita IDs de canal separados por vírgula.
`DAILY_DIGEST_INTERESTS` também aceita valores separados por vírgula. As fontes
RSS e o SMTP são serviços externos: configure credenciais válidas e conexão com
a internet antes de executar o comando.

Se o comando for repetido no mesmo dia para o mesmo destinatário, o histórico
impede um segundo envio. Falhas de SMTP são registradas como `failed`, permitindo
uma nova tentativa posterior.

## Testes e verificações

```bash
python -m pytest
python -m compileall -q app config.py
```

O GitHub Actions executa a suíte automaticamente em pull requests e alterações
na branch `main`.

Consulte [o guia de validação local](docs/LOCAL_RUNBOOK.md) antes de abrir uma
pull request ou publicar uma alteração.

## Configuração

| Variável | Obrigatória para | Descrição |
| --- | --- | --- |
| `DATABASE_URL` | Digest | URL do PostgreSQL local ou remoto. |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Docker local | Credenciais usadas pelo Compose. |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SENDER` | Digest | Configuração de envio SMTP SSL. |
| `DAILY_DIGEST_RECIPIENT` | Digest | E-mail que receberá o digest. |
| `DAILY_DIGEST_INTERESTS` | Digest | Interesses separados por vírgula. |
| `YOUTUBE_CHANNEL_IDS` | Opcional | IDs de canais separados por vírgula. |
| `NEWFLOW_ENV`, `NEWFLOW_DEBUG`, `SECRET_KEY`, `HOST`, `PORT` | Aplicação web | Configuração do processo Flask. |

## Limites atuais e próximos incrementos

Esta primeira versão não possui interface web, autenticação nem painel de
histórico. Ela foi estruturada para que essas entregas possam ser adicionadas
como adaptadores externos, preservando o pipeline e os casos de uso atuais.

## Licença

Distribuído sob a [licença MIT](LICENSE).
