# Guia técnico de execução local

Este documento descreve como configurar, validar e executar o NewFlow AI em
uma máquina local. O README permanece como apresentação geral do projeto;
este guia concentra os detalhes técnicos e operacionais.

## 1. Pré-requisitos

Instale os itens abaixo antes de iniciar:

- Python 3.11 ou superior;
- Docker Desktop com Docker Compose;
- Git;
- uma conta SMTP com acesso SSL, caso queira enviar o digest real.

Confirme as ferramentas:

```bash
python --version
docker --version
docker compose version
git --version
```

## 2. Clonar e preparar o ambiente Python

```bash
git clone https://github.com/LucasEstrela-FullStack/NewsFlow-AI.git
cd NewsFlow-AI
python -m venv .venv
```

Ative o ambiente virtual e instale também as dependências de teste.

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

```bash
# Linux/macOS
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## 3. Criar a configuração local

Crie `.env` a partir do arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

```bash
cp .env.example .env
```

O `.env` é local e não deve ser enviado ao Git. Escolha uma senha para
`POSTGRES_PASSWORD` e aplique-a também dentro de `DATABASE_URL`.

Exemplo de configuração mínima para iniciar o banco e a aplicação web:

```env
NEWFLOW_ENV=development
NEWFLOW_DEBUG=true
SECRET_KEY=replace-with-a-local-random-value
HOST=127.0.0.1
PORT=5000

POSTGRES_DB=newflow
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<LOCAL_POSTGRES_PASSWORD>
DATABASE_URL=postgresql://postgres:<LOCAL_POSTGRES_PASSWORD>@localhost:5433/newflow
```

Para executar o job diário, acrescente as configurações de envio:

```env
SMTP_HOST=<SMTP_HOST>
SMTP_PORT=465
SMTP_USERNAME=<SMTP_USERNAME>
SMTP_PASSWORD=<SMTP_PASSWORD>
SMTP_SENDER=<SENDER_EMAIL>

DAILY_DIGEST_RECIPIENT=<RECIPIENT_EMAIL>
DAILY_DIGEST_INTERESTS=AI,software engineering,cloud
YOUTUBE_CHANNEL_IDS=
```

`DAILY_DIGEST_INTERESTS` e `YOUTUBE_CHANNEL_IDS` aceitam valores separados por
vírgula. O segundo é opcional. Mantenha os delimitadores entre `<...>` como
referências no exemplo: substitua-os pelos valores locais no arquivo `.env`.

## 4. Iniciar o stack completo com Docker

O Compose inicia a aplicação web e o PostgreSQL:

```bash
docker compose up --build -d
docker compose ps
```

Espere os serviços `app` e `database` aparecerem como saudáveis. A aplicação
fica disponível na porta `5000`; o banco expõe a porta `5433` no computador
local, mapeada para a porta `5432` do container. Dentro do Compose, a aplicação
usa o hostname `database`, sem depender da URL de localhost presente no `.env`.

Se a porta `5000` já estiver ocupada, escolha outra porta sem editar o Compose:

```powershell
$env:WEB_PORT = "5001"
docker compose up --build -d
```

No Linux/macOS, use `WEB_PORT=5001 docker compose up --build -d`.

Para acompanhar o início do banco:

```bash
docker compose logs -f app database
```

Para parar o banco preservando os dados do volume:

```bash
docker compose down
```

## 5. Validar a aplicação web

Valide o endpoint de saúde após o Compose iniciar:

```bash
curl http://127.0.0.1:5000/health
```

Substitua `5000` pelo valor definido em `WEB_PORT` quando usar uma porta
alternativa.

Resultado esperado:

```json
{"service":"newflow","status":"ok"}
```

Esse endpoint confirma que o processo Flask está disponível. Ele não executa
coleta, não envia e-mail e não exige credenciais SMTP.

Para executar a aplicação diretamente pelo Python, sem o container web, mantenha
somente o banco ativo com `docker compose up -d database` e execute:

```bash
python run.py
```

## 6. Executar o digest diário

Antes desta etapa, confirme as variáveis `DATABASE_URL`, `SMTP_*`,
`DAILY_DIGEST_RECIPIENT` e `DAILY_DIGEST_INTERESTS`. Em seguida:

```bash
python -m app.jobs.daily_digest
```

O job realiza as seguintes ações:

1. lê feeds RSS públicos da OpenAI e Anthropic;
2. coleta canais YouTube configurados, se houver;
3. persiste artigos novos no PostgreSQL;
4. ordena artigos de acordo com os interesses definidos;
5. gera o digest em Markdown;
6. reserva a entrega do dia e envia o e-mail via SMTP;
7. registra o resultado como `sent` ou `failed`.

O job acessa rede e SMTP reais. Execute-o somente com credenciais autorizadas.
Uma nova execução no mesmo dia para o mesmo destinatário não reenvia o digest;
uma falha de SMTP fica registrada como `failed` e pode ser tentada novamente.

## 7. Executar os testes e verificações

```bash
python -m pytest
python -m compileall -q app config.py
python -m ruff check .
git diff --check
```

A suíte usa fakes e SQLite nos limites necessários; ela não requer PostgreSQL,
SMTP, feeds RSS ou YouTube ativos. O GitHub Actions executa os testes para pull
requests e alterações na `main`.

## 8. Checklist de pull request

- [ ] `python -m pytest` conclui sem falhas.
- [ ] `python -m compileall -q app config.py` conclui sem erros.
- [ ] `python -m ruff check .` não encontra violações de lint.
- [ ] `git diff --check` não encontra espaços ou quebras inválidas.
- [ ] `.env`, credenciais e URLs com senhas não aparecem no diff.
- [ ] O comportamento documentado corresponde ao código alterado.
- [ ] A alteração está em uma branch dedicada e possui commit convencional.
- [ ] O workflow de CI passou no pull request.

## Diagnóstico rápido

| Sintoma | Verificação inicial |
| --- | --- |
| Aplicação não inicia | Confirme o ambiente virtual e `python -m pip install -r requirements-dev.txt`. |
| Banco indisponível | Execute `docker compose ps` e confira `DATABASE_URL`, porta `5433` e senha. |
| Job recusa configuração | Leia a mensagem: o job informa explicitamente qual variável obrigatória está ausente. |
| Falha de envio | Revise host, porta SSL, usuário, senha e remetente SMTP sem expor valores. |
| Nenhum artigo recente | Verifique conectividade com a internet; os feeds podem não publicar itens na janela de 24 horas. |
